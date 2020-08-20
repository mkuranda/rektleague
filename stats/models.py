import datetime
import time
import math
import re
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Sum, Q, Case, When, F, Value, ExpressionWrapper
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

class MerchProduct(models.Model):
    name = models.CharField(max_length=100)
    blurb = models.CharField(max_length=1000)
    warning = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    photo = models.ImageField(upload_to='stats/merch_photos', default='')


class Season(models.Model):
    tournament_id = models.IntegerField(default=0)
    team_size = models.IntegerField(default=5)
    pick_type = models.CharField(max_length=30)
    map_type = models.CharField(max_length=30)
    spectator_type = models.CharField(max_length=30)
    playoff_bracket = models.ImageField(upload_to='stats/', default='')
    splash = models.ImageField(upload_to='stats/season_splashes', default='')

    def __str__(self):
        return "SEASON " + str(self.pk)

    def get_weeks(self):
        return Week.objects.filter(season=self).order_by('-number')

    def get_regular_weeks_desc(self):
        return Week.objects.filter(season=self, regular=True).order_by('number')

    def get_playoff_weeks_desc(self):
        return Week.objects.filter(season=self, regular=False).order_by('number')

    def get_weeks_desc(self):
        return Week.objects.filter(season=self).order_by('number')

    def get_top_banned(self):
        num_matches = Match.objects.filter(series__week__season=self).exclude(duration=0).count()
        if num_matches == 0:
            return TeamMatchBan.objects.none()
        return TeamMatchBan.objects.filter(team__season=self).values('champion__name', 'champion__icon', 'champion').annotate(ban_rate=Count('champion') * 100 / num_matches).order_by('-ban_rate')[:20]

    def get_top_picked(self):
        num_matches = Match.objects.filter(series__week__season=self).exclude(duration=0).count()
        if num_matches == 0:
            return PlayerMatch.objects.none()
        return PlayerMatch.objects.filter(match__series__week__season=self).values('champion__name', 'champion__icon', 'champion').annotate(pick_rate=Count('champion') * 100 / num_matches).order_by('-pick_rate')[:20]

    def get_champ_stats(self):
        num_matches = Match.objects.filter(series__week__season=self).exclude(duration=0).count()
        stats = PlayerMatch.objects.filter(match__series__week__season=self)
        win_ids = [o.id for o in stats if o.win()]
        return stats.filter(id__in=win_ids).values('champion__name', 'champion__icon', 'champion').annotate(pick_rate=Count('champion') * 100 / num_matches)

    def get_winner(self):
        return Team.objects.filter(season=self, season_win=True)

    def next_week(self):
        ret = Week.objects.filter(season=self, date__gte=datetime.datetime.now())
        if self.id > 2 and len(ret) > 0:
            return ret[0]
        return self.get_weeks()[0]

    def get_damage_per_minute(self):
        results = []
        players = TeamPlayer.objects.filter(team__season=self, role__isFill=True)
        for player in players:
            damage = 0
            minutes = 0
            player_matches = PlayerMatch.objects.filter(player=player.player, match__series__week__season=self)
            for player_match in player_matches:
                damage = damage + player_match.total_damage_dealt
                minutes = minutes + player_match.match.duration
            if minutes > 0:
                results.append({
                    'name': player.player.name,
                    'dpm': 1.0 * damage / minutes
                    })
        return sorted(results, key = lambda t: -t['dpm'])

    def get_most_first_bloods(self):
        results = []
        players = TeamPlayer.objects.filter(team__season=self, role__isFill=True)
        for player in players:
            first_bloods = 0
            player_matches = PlayerMatch.objects.filter(player=player.player, match__series__week__season=self)
            for player_match in player_matches:
                kill = PlayerMatchKill.objects.filter(killer__match=player_match.match).order_by('timestamp')[0]
                if kill.killer== player:
                    first_bloods = first_bloods + 1
            results.append({
                'name': player.player.name,
                'kills': first_bloods
                })
        return sorted(results, key = lambda t: -t['kills'])

    def get_most_unique_kills(self):
        results = []
        players = TeamPlayer.objects.filter(team__season=self, role__isFill=True)
        for player in players:
            player_kills = PlayerMatchKill.objects.filter(killer__player=player.player, killer__team=player.team, timestamp__lt=910000).aggregate(num_victims=Count('victim__player', distinct=True))
            results.append({
                'name': player.player.name,
                'kills': player_kills['num_victims']
                })
        return sorted(results, key = lambda t: -t['kills'])

    def get_most_blue_wards(self):
        results = []
        teams = Team.objects.filter(season=self)
        for team in teams:
            wards_placed = PlayerMatchWardPlace.objects.filter(playermatch__team=team, ward_type__name="Blue Trinket").count()
            results.append({
                'name': team.name,
                'blue_wards': wards_placed
                })
        return sorted(results, key = lambda t: -t['blue_wards'])

    def get_pct_of_opp_wards_destroyed(self):
        results = []
        teams = Team.objects.filter(season=self)
        for team in teams:
            placed = 0
            destroyed = 0
            teammatches = TeamMatch.objects.filter(team=team)
            for teammatch in teammatches:
                wards_placed = PlayerMatchWardPlace.objects.filter(playermatch__match = teammatch.match).exclude(playermatch__team=team, ward_type__name="Teemo Mushroom").exclude(ward_type__name="Undefined").count()
                wards_destroyed = PlayerMatchWardKill.objects.filter(playermatch__match = teammatch.match, playermatch__team=team).exclude(ward_type__name="Teemo Mushroom").exclude(ward_type__name="Undefined").count()
            results.append({
                'name': team.name,
                'pct': 100.0 * wards_destroyed / wards_placed
                })
        return sorted(results, key = lambda t: -t['pct'])

    def get_2_drag_win_pct(self):
        wins = 0
        losses = 0
        matches = Match.objects.filter(series__week__season=self)
        for match in matches:
            monster_kills = PlayerMatchEliteMonsterKill.objects.filter(playermatch__match=match, monster_type__riot_name="DRAGON").order_by('timestamp')
            if monster_kills.count() > 1:
                if monster_kills[0].playermatch.team == monster_kills[1].playermatch.team:
                    if match.get_winner().team == monster_kills[0].playermatch.team:
                        wins = wins + 1
                    else:
                        losses = losses + 1
        return 100.0 * wins / (wins + losses)

    def get_2_rift_win_pct(self):
        wins = 0
        losses = 0
        matches = Match.objects.filter(series__week__season=self)
        for match in matches:
            monster_kills = PlayerMatchEliteMonsterKill.objects.filter(playermatch__match=match, monster_type__name="Rift Herald").order_by('timestamp')
            if monster_kills.count() > 1:
                if monster_kills[0].playermatch.team == monster_kills[1].playermatch.team:
                    if match.get_winner().team == monster_kills[0].playermatch.team:
                        wins = wins + 1
                    else:
                        losses = losses + 1
        return 100.0 * wins / (wins + losses)

    def get_highest_first_tower_assists(self):
        results = []
        teams = Team.objects.filter(season=self)
        for team in teams:
            first_towers = 0
            assists = 0
            matches = TeamMatch.objects.filter(team=team)
            for match in matches:
                first_tower = PlayerMatchBuildingKill.objects.filter(playermatch__match=match.match).order_by('timestamp')[0]
                if first_tower.playermatch.team == team:
                    first_towers = first_towers + 1
                    assists = assists + PlayerMatchBuildingAssist.objects.filter(kill=first_tower).count()
            results.append({
                'name': team.name,
                'assists': 1 + (1.0 * assists / first_towers)
                })
        return sorted(results, key = lambda t: -t['assists'])


    def get_best_kp_pre_15(self):
        results = []
        players = TeamPlayer.objects.filter(team__season=self, role__isFill=True)
        for player in players:
            if player.get_num_matches() > 0:
                playermatches = PlayerMatch.objects.filter(player=player.player, team=player.team)
                player_kills = 0
                total_kills = 0
                for playermatch in playermatches:
                    player_kills = player_kills + PlayerMatchKill.objects.filter(killer__player=player.player, killer__match=playermatch.match, timestamp__lt=910000).count()
                    player_kills = player_kills + PlayerMatchAssist.objects.filter(playermatch__player=player.player, playermatch__match=playermatch.match, kill__timestamp__lt=910000).count()
                    total_kills = total_kills + PlayerMatchKill.objects.filter(killer__team=player.team, killer__match=playermatch.match, timestamp__lt=910000).count()
                results.append({
                    'name': player.player.name,
                    'pct': 100.0 * player_kills / total_kills
                    })
        return sorted(results, key = lambda t: -t['pct'])
    
    def get_top_counterjunglers(self):
        results = []
        players = TeamPlayer.objects.filter(team__season=self, role__name="JUNGLE")
        for teamplayer in players:
            playermatches = teamplayer.get_player_matches()
            if playermatches:
                team_cs_total = 0
                enemy_cs_total = 0
                for playermatch in playermatches:
                    team_cs_total += playermatch.neutral_minions_killed_team_jungle
                    enemy_cs_total += playermatch.neutral_minions_killed_enemy_jungle
                results.append({
                    'name': teamplayer.player.name,
                    'counterjungle_percent': 100.0 * enemy_cs_total / (team_cs_total + enemy_cs_total),
                    'total_games': playermatches.count()
                    })
        return sorted(results, key = lambda t: -t['counterjungle_percent'])

    def get_most_solo_kills(self):
        results = []
        players = TeamPlayer.objects.filter(team__season=self, role__isFill=True)
        for teamplayer in players:
            solo_kills = 0
            total_kills = 0
            playermatches = teamplayer.get_player_matches()
            for playermatch in playermatches:
                kills = PlayerMatchKill.objects.filter(killer=playermatch)
                for kill in kills:
                    if not PlayerMatchAssist.objects.filter(kill=kill):
                        solo_kills = solo_kills + 1
                    total_kills = total_kills + 1
            if total_kills > 0 and playermatches.count() > 2:
                results.append({
                    'name': teamplayer.player.name,
                    'solo_kills': 100.0 * solo_kills / total_kills
                    })
        return sorted(results, key = lambda t: -t['solo_kills'])

    def get_cs_diff_below_elo(self):
        results = []
        players = TeamPlayer.objects.filter(team__season=self, role__isFill=True)
        for player in players:
            total = 0
            num_matches = 0
            playermatches = PlayerMatch.objects.filter(player=player.player, team=player.team).exclude(role__name="SUPPORT").exclude(role__name="JUNGLE").exclude(role__name="BOT")
            for playermatch in playermatches:
                timeline = PlayerMatchTimeline.objects.filter(playermatch=playermatch, timestamp__lt=910000).values('timestamp', 'minions_killed', 'monsters_killed', 'playermatch').annotate(cs=F('minions_killed')+F('monsters_killed')).order_by('-timestamp')[0]
                enemy_timeline = PlayerMatchTimeline.objects.filter(playermatch__match=playermatch.match, playermatch__role=playermatch.role, timestamp__lt=910000).exclude(playermatch__team=playermatch.team).values('timestamp', 'minions_killed', 'monsters_killed', 'playermatch').annotate(cs=F('minions_killed')+F('monsters_killed')).order_by('-timestamp')[0]
                if player.player.elo_value + 4 < playermatch.get_opponent().player.elo_value:
                    total = total + timeline['cs'] - enemy_timeline['cs']
                    num_matches = num_matches + 1
            if num_matches > 2:
                results.append({
                    'name': player.player.name,
                    'total': 1.0 * total / num_matches
                    })
        return sorted(results, key = lambda t: -t['total'])
      

    def get_most_percent_control_ward_gold(self):
        results = []
        players = TeamPlayer.objects.filter(team__season=self, role__isFill=True)
        for teamplayer in players:
            if teamplayer.get_num_matches() > 0:
                results.append({
                    'name': teamplayer.player.name,
                    'percent': teamplayer.get_percent_control_ward_gold()
                    })
        return sorted(results, key = lambda t: -t['percent'])

    def lane_first_tower_pct(self):
        results = []
        matches = Match.objects.filter(series__week__season=self, duration__gt=5)
        top = 0
        mid = 0
        bot = 0
        total = 0
        for match in matches:
            first_tower = PlayerMatchBuildingKill.objects.filter(playermatch__match=match).order_by('timestamp')[0]
            if first_tower.building_type.lane.name == "Top":
                top = top + 1
                total = total + 1
            if first_tower.building_type.lane.name == "Mid":
                mid = mid + 1
                total = total + 1
            if first_tower.building_type.lane.name == "Bot":
                bot = bot + 1
                total = total + 1
        results = [{ 
                'name': 'Top', 
                'pct': 100.0 * top / total
            },
            {
                'name': 'Mid',
                'pct': 100.0 * mid / total
            },
            {   
                'name': 'Bot',
                'pct': 100.0 * bot / total
            }]
        return results


    def lane_first_inhib_pct(self):
        results = []
        matches = Match.objects.filter(series__week__season=self, duration__gt=5)
        top = 0
        mid = 0
        bot = 0
        total = 0
        for match in matches:
            first_inhib = PlayerMatchBuildingKill.objects.filter(playermatch__match=match, building_type__name="Inhibitor").order_by('timestamp')
            if first_inhib:
                first_inhib = first_inhib[0]
                if first_inhib.building_type.lane.name == "Top":
                    top = top + 1
                    total = total + 1
                if first_inhib.building_type.lane.name == "Mid":
                    mid = mid + 1
                    total = total + 1
                if first_inhib.building_type.lane.name == "Bot":
                    bot = bot + 1
                    total = total + 1
        results = [{ 
                'name': 'Top', 
                'pct': 100.0 * top / total
            },
            {
                'name': 'Mid',
                'pct': 100.0 * mid / total
            },
            {   
                'name': 'Bot',
                'pct': 100.0 * bot / total
            }]
        return results

    def dragon_map_pct(self):
        results = []
        matches = Match.objects.filter(series__week__season=self, duration__gt=5)
        cloud = 0
        infernal = 0
        ocean = 0
        mountain = 0
        total = 0
        for match in matches:
            dragon = PlayerMatchEliteMonsterKill.objects.filter(playermatch__match=match, monster_type__riot_name="DRAGON").order_by('timestamp')
            dragon = dragon[2]
            if dragon.monster_type.name == "Air Drake":
                cloud = cloud + 1
                total = total + 1
            if dragon.monster_type.name == "Infernal Drake":
                infernal = infernal + 1
                total = total + 1
            if dragon.monster_type.name == "Ocean Drake":
                ocean = ocean + 1
                total = total + 1
            if dragon.monster_type.name == "Mountain Drake":
                mountain = mountain + 1
                total = total + 1
        results = [{ 
                'name': 'Air', 
                'pct': 100.0 * cloud / total
            },
            {
                'name': 'Infernal',
                'pct': 100.0 * infernal / total
            },
            {
                'name': 'Ocean',
                'pct': 100.0 * ocean / total
            },
            {   
                'name': 'Mountain',
                'pct': 100.0 * mountain / total
            }]
        return results
          
    def dragon_soul_pct(self):
        results = []
        matches = Match.objects.filter(series__week__season=self, duration__gt=5)
        cloud = 0
        infernal = 0
        ocean = 0
        mountain = 0
        total = 0
        for match in matches:
            teammatches = TeamMatch.objects.filter(match=match)
            for teammatch in teammatches:
                dragon = PlayerMatchEliteMonsterKill.objects.filter(playermatch__match=teammatch.match, playermatch__team=teammatch.team, monster_type__riot_name="DRAGON").exclude(monster_type__name="Elder Dragon").order_by('timestamp')
                if dragon.count() > 3:
                    dragon = dragon[3]
                    if dragon.monster_type.name == "Air Drake":
                        cloud = cloud + 1
                        total = total + 1
                    if dragon.monster_type.name == "Infernal Drake":
                        infernal = infernal + 1
                        total = total + 1
                    if dragon.monster_type.name == "Ocean Drake":
                        ocean = ocean + 1
                        total = total + 1
                    if dragon.monster_type.name == "Mountain Drake":
                        mountain = mountain + 1
                        total = total + 1
        results = [{ 
                'name': 'Air', 
                'pct': 100.0 * cloud / total
            },
            {
                'name': 'Infernal',
                'pct': 100.0 * infernal / total
            },
            {
                'name': 'Ocean',
                'pct': 100.0 * ocean / total
            },
            {   
                'name': 'Mountain',
                'pct': 100.0 * mountain / total
            }]
        return results
   
    def get_earliest_avg_kill(self):
        results = []
        players = TeamPlayer.objects.filter(team__season=self, role__isFill=True)
        for teamplayer in players:
            playermatches = teamplayer.get_player_matches()
            if playermatches:
                kill_timestamp_total = 0
                num_matches = 0
                for playermatch in playermatches:
                    kill = PlayerMatchKill.objects.filter(killer=playermatch).order_by('timestamp')
                    if kill:
                        kill_timestamp_total += kill[0].timestamp
                        num_matches += 1
                if num_matches > 0:
                    results.append({
                        'name': teamplayer.player.name,
                        'kill_timestamp': 1.0 * kill_timestamp_total / num_matches,
                        'total_games': num_matches
                        })
        return sorted(results, key = lambda t: t['kill_timestamp'])
     
    def get_baron_prox_kill_percent(self):
        results = []
        teams = Team.objects.filter(season=self)
        for team in teams:
            playermatches = team.get_player_matches()
            if playermatches:
                kill_count = 0
                total_kills = 0
                for playermatch in playermatches:
                    kills = PlayerMatchKill.objects.filter(killer=playermatch)
                    for kill in kills:
                        if kill and kill.position_x > 3300 and kill.position_x < 6500 and kill.position_y > 8700 and kill.position_y < 11800:
                            kill_count += 1
                        if kill:
                            total_kills += 1
                if total_kills > 0:
                    results.append({
                        'name': team.name,
                        'kill_percent': 1.0 * kill_count / total_kills
                        })
        return sorted(results, key = lambda t: t['kill_percent'])

    def get_dragon_prox_kill_percent(self):
        results = []
        teams = Team.objects.filter(season=self)
        for team in teams:
            playermatches = team.get_player_matches()
            if playermatches:
                kill_count = 0
                total_kills = 0
                for playermatch in playermatches:
                    kills = PlayerMatchKill.objects.filter(killer=playermatch)
                    for kill in kills:
                        if kill and kill.position_y > 3300 and kill.position_y < 6500 and kill.position_x > 8700 and kill.position_x < 11800:
                            kill_count += 1
                        if kill:
                            total_kills += 1
                if total_kills > 0:
                    results.append({
                        'name': team.name,
                        'kill_percent': 1.0 * kill_count / total_kills
                        })
        return sorted(results, key = lambda t: t['kill_percent'])

    def get_wards_placed_before_barons(self):
        results = []
        teams = Team.objects.filter(season=self)
        for team in teams:
            playermatches = team.get_player_matches()
            if playermatches:
                total_kills = 0
                wards_placed = 0
                wards_killed = 0
                for playermatch in playermatches:
                    kills = PlayerMatchEliteMonsterKill.objects.filter(playermatch=playermatch, monster_type__name="Baron Nashor")
                    for kill in kills:
                        ward_kills = PlayerMatchWardKill.objects.filter(playermatch__team=playermatch.team, playermatch__match=playermatch.match, timestamp__lt=kill.timestamp, timestamp__gt=kill.timestamp - 60000)
                        ward_placed = PlayerMatchWardPlace.objects.filter(playermatch__team=playermatch.team, playermatch__match=playermatch.match, timestamp__lt=kill.timestamp, timestamp__gt=kill.timestamp - 60000)
                        wards_killed += ward_kills.count()
                        wards_placed += ward_placed.count()
                        total_kills += 1
                if total_kills > 0:
                    results.append({
                        'name': team.name,
                        'total_kills': total_kills,
                        'wards_placed': 1.0 * wards_placed / total_kills,
                        'wards_killed': 1.0 * wards_killed / total_kills
                        })
        return sorted(results, key = lambda t: t['wards_killed'])

    def get_wards_placed_before_dragons(self):
        results = []
        teams = Team.objects.filter(season=self)
        for team in teams:
            playermatches = team.get_player_matches()
            if playermatches:
                total_kills = 0
                wards_placed = 0
                wards_killed = 0
                for playermatch in playermatches:
                    kills = PlayerMatchEliteMonsterKill.objects.filter(playermatch=playermatch).exclude(monster_type__name="Baron Nashor").exclude(monster_type__name="Rift Herald")
                    for kill in kills:
                        ward_kills = PlayerMatchWardKill.objects.filter(playermatch__team=playermatch.team, playermatch__match=playermatch.match, timestamp__lt=kill.timestamp, timestamp__gt=kill.timestamp - 30000)
                        ward_placed = PlayerMatchWardPlace.objects.filter(playermatch__team=playermatch.team, playermatch__match=playermatch.match, timestamp__lt=kill.timestamp, timestamp__gt=kill.timestamp - 30000)
                        wards_killed += ward_kills.count()
                        wards_placed += ward_placed.count()
                        total_kills += 1
                if total_kills > 0:
                    results.append({
                        'name': team.name,
                        'total_kills': total_kills,
                        'wards_placed': 1.0 * wards_placed / total_kills,
                        'wards_killed': 1.0 * wards_killed / total_kills
                        })
        return sorted(results, key = lambda t: t['wards_killed'])

    def get_jungler_lane_kill_percent(self):
        results = []
        teamplayers = TeamPlayer.objects.filter(team__season=self, role__name="Jungle")
        for teamplayer in teamplayers:
            playermatches = teamplayer.get_player_matches()
            if playermatches:
                top_count = 0
                mid_count = 0
                bot_count = 0
                total_kills = 0
                for playermatch in playermatches:
                    kills = PlayerMatchKill.objects.filter(killer=playermatch, timestamp__lt=910000)
                    assists = PlayerMatchAssist.objects.filter(playermatch=playermatch, kill__timestamp__lt=910000)
                    for kill in kills:
#                        if kill.position_x < 5000 and kill.position_y > 9500:
                        if math.hypot(kill.position_x - 1800, kill.position_y - 13000) < 2500:
                            top_count += 1
                        if math.hypot(kill.position_x - 7500, kill.position_y - 7500) < 2500:
                        #if kill.position_x > 5000 and kill.position_x < 10500 and kill.position_y < 9500 and kill.position_x > 4800:
                            mid_count += 1
                        if math.hypot(kill.position_x - 13000, kill.position_y - 1800) < 2500:
                        #if kill.position_x > 10500 and kill.position_y < 4800:
                            bot_count += 1
                        total_kills += 1
                    for assist in assists:
                        #if assist.kill.position_x < 5000 and assist.kill.position_y > 9500:
                        if math.hypot(assist.kill.position_x - 1800, assist.kill.position_y - 13000) < 2500:
                            top_count += 1
                        if math.hypot(assist.kill.position_x - 7500, assist.kill.position_y - 7500) < 2500:
                        #if assist.kill.position_x > 5000 and assist.kill.position_x < 10500 and assist.kill.position_y < 9500 and assist.kill.position_x > 4800:
                            mid_count += 1
                        if math.hypot(assist.kill.position_x - 13000, assist.kill.position_y - 1800) < 2500:
                        #if assist.kill.position_x > 10500 and assist.kill.position_y < 4800:
                            bot_count += 1
                        total_kills += 1
                if total_kills > 0:
                    results.append({
                        'name': teamplayer.player.name,
                        'top_percent': 1.0 * top_count / total_kills,
                        'mid_percent': 1.0 * mid_count / total_kills,
                        'bot_percent': 1.0 * bot_count / total_kills,
                        'laneless_percent': 1.0 * (total_kills - top_count - mid_count - bot_count) / total_kills
                        })
        return sorted(results, key = lambda t: t['mid_percent'])

class Week(models.Model):
    season = models.ForeignKey(Season)
    number = models.IntegerField(default=1)
    regular = models.BooleanField(default=True)
    title = models.CharField(max_length=50, default="")
    date = models.DateTimeField(null=True, blank=True)

    def name_w_title(self):
        if self.title != "" and self.title != " ":
            return "WEEK " + str(self.number) + " - " + self.title
        return "WEEK " + str(self.number)

    def __str__(self):
        if self.title != "" and self.title != " ":
            return str(self.season) + ": " + self.title
        return str(self.season) + ": WEEK " + str(self.number)

class Role(models.Model):
    name = models.CharField(max_length=15)
    icon = models.ImageField(upload_to='stats/role/icon', default='')
    isFill = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Champion(models.Model):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    icon = models.ImageField(upload_to='stats/champion/icon', default='')
    seasons = models.ManyToManyField(Season, through='SeasonChampion')

    def __str__(self):
        return self.name

class SeasonChampion(models.Model):
    season = models.ForeignKey(Season)
    champion = models.ForeignKey(Champion)

    def get_matches(self):
        matches = PlayerMatch.objects.filter(champion=self.champion, match__series__week__season=self.season).exclude(match__duration=0)
        return matches.count()

    def get_bans(self):
        matches = TeamMatchBan.objects.filter(champion=self.champion, team__season=self.season)
        return matches.count()

    def get_winrate(self):
        matches = PlayerMatch.objects.filter(champion=self.champion, match__series__week__season=self.season).exclude(match__duration=0)
        win_ids = [o.id for o in matches if o.win()]
        num_matches = matches.count()
        if num_matches == 0:
            return 0.0
        num_wins = PlayerMatch.objects.filter(id__in=win_ids).count()
        return float(num_wins) * 100 / num_matches

    def get_most_picked_player(self):
        return PlayerMatch.objects.filter(match__series__week__season=self.season, champion=self.champion).values('player', 'team__name', 'team__icon', 'player__name').annotate(player_count=Count('player')).order_by('-player_count')[:1]
        
    def get_most_banned_by(self):
        return TeamMatchBan.objects.filter(match__series__week__season=self.season, champion=self.champion).values('team__name', 'team__icon', 'team__id').annotate(ban_count=Count('team__name')).order_by('-ban_count')[:1]
 

class Series(models.Model):
    twitch_vod_num = models.IntegerField(default=0)
    youtube_link = models.CharField(max_length=100, null=True, blank=True)
    week = models.ForeignKey(Week)
    splash = models.ImageField(upload_to='stats/champion/matchup_splashes', null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def get_series_team_1(self):
	teamSeries = SeriesTeam.objects.filter(series=self)
	return teamSeries[0]

    def get_series_team_2(self):
	teamSeries = SeriesTeam.objects.filter(series=self)
	return teamSeries[1]

    def get_team_1(self):
	teamSeries = SeriesTeam.objects.filter(series=self)
	return teamSeries[0].team

    def get_team_2(self):
	teamSeries = SeriesTeam.objects.filter(series=self)
	return teamSeries[1].team

    def get_team_1_cast_players(self):
        return SeriesCastPlayer.objects.filter(series=self, team=self.get_team_1)

    def get_team_2_cast_players(self):
        return SeriesCastPlayer.objects.filter(series=self, team=self.get_team_2)

    def get_team_1_players(self):
        return SeriesPlayer.objects.filter(series=self, team=self.get_team_1())

    def get_team_2_players(self):
        return SeriesPlayer.objects.filter(series=self, team=self.get_team_2())

    def get_team_1_wins(self):
	return TeamMatch.objects.filter(team=self.get_team_1(), win=True, match__series=self).count()

    def get_team_2_wins(self):
	return TeamMatch.objects.filter(team=self.get_team_2(), win=True, match__series=self).count()

    def get_team_1_roster_submitted(self):
        if not self.get_team_1_players() or self.get_team_1_players().count() < 5:
            return False
        return True

    def get_team_2_roster_submitted(self):
        if not self.get_team_2_players() or self.get_team_2_players().count() < 5:
            return False
        return True

    def rosters_submitted(self):
        return self.get_team_1_roster_submitted() and self.get_team_2_roster_submitted()

    def deadline(self):
        if self.week.date is None:
            return None
        return self.week.date - datetime.timedelta(days=4)

    def past_deadline(self):
        now = datetime.datetime.now()
        if self.deadline() is not None and self.deadline() + datetime.timedelta(hours=5) < now:
            return True
        return False

    def __str__(self):
	return str(self.week) + ": " + str(self.get_team_1()) + " v " + str(self.get_team_2())


class Match(models.Model):
    id = models.BigIntegerField(primary_key=True)
    series = models.ForeignKey(Series)
    riot_id = models.BigIntegerField(default=0)
    game_num = models.IntegerField(default=1)
    tournament_code = models.CharField(max_length=100, blank=True)
    duration = models.IntegerField(default=0)

    def get_winner(self):
	return TeamMatch.objects.get(match=self, win=True)

    def get_loser(self):
	return TeamMatch.objects.get(match=self, win=False)

    def get_blue_team(self):
	return TeamMatch.objects.get(match=self, side="Blue")

    def get_red_team(self):
	return TeamMatch.objects.get(match=self, side="Red")

    def get_max_timeline_minute(self):
        if self.series.week.season.id > 2:
            playermatchtimelines = PlayerMatchTimeline.objects.filter(playermatch__match=self).annotate(minute=F('timestamp') / 1000 / 60).order_by('-minute')
            if playermatchtimelines:
                return playermatchtimelines[0].minute
            return 0
        else:
            return 0

    def duration_str(self):
        return time.strftime("%M:%S", time.gmtime(self.duration))

    def __str__(self):
        seriesTeams = SeriesTeam.objects.filter(series=self.series)
        return str(seriesTeams[0].team) + " v " + str(seriesTeams[1].team) + " (" + str(self.series.week) + " game " + str(self.game_num) + ")"

    def get_timeline_diffs(self):
        return self.get_blue_team().get_timeline_diffs()

@python_2_unicode_compatible
class Player(models.Model):
    name = models.CharField(max_length=40)
    user = models.ForeignKey(User, default=0)
    riot_id = models.IntegerField(default=0)
    matches = models.ManyToManyField(Match, through='PlayerMatch')
    photo = models.ImageField(upload_to='stats/player_photos', blank=True, null=True)
    elo_value = models.IntegerField(default=100)

    def team_players(self):
        return TeamPlayer.objects.filter(player=self)

    def teams(self):
        return Team.objects.filter(pk__in=self.team_players())

    def seasons(self):
        return Season.objects.filter(pk__in=self.teams())

    def total_deaths(self):
        player_matches = PlayerMatch.objects.filter(player=self).aggregate(sum_deaths=Sum('deaths'))
        if player_matches['sum_deaths'] == None:
            return 0
        return player_matches['sum_deaths']

    def total_assists(self):
        player_matches = PlayerMatch.objects.filter(player=self).aggregate(sum_assists=Sum('assists'))
        if player_matches['sum_assists'] == None:
            return 0
        return player_matches['sum_assists']

    def total_kills(self):
        player_matches = PlayerMatch.objects.filter(player=self).aggregate(sum_kills=Sum('kills'))
        if player_matches['sum_kills'] == None:
            return 0
        return player_matches['sum_kills']

    def __str__(self):
        return self.name + " (" + str(self.elo_value) + ")"

@python_2_unicode_compatible
class Summoner(models.Model):
    player = models.ForeignKey(Player)
    name = models.CharField(max_length=75)
    link = models.CharField(max_length=80)

    def __str__(self):
        return self.name + " (" + unicode(self.player) + ")"

class TeamMedia(models.Model):
    name = models.CharField(max_length=40)
    icon = models.ImageField(upload_to='stats')
    splash = models.ImageField(upload_to='stats/team_splashes', default='')
    banner = models.ImageField(upload_to='stats/team_banners')
    left_splash = models.ImageField(upload_to='stats/team_splashes')
    right_splash = models.ImageField(upload_to='stats/team_splashes')
    home_splash = models.ImageField(upload_to='stats/homepageSplash', default='')
    blurb = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=40)
    user = models.ForeignKey(User, default=0)
    players = models.ManyToManyField(Player, through='TeamPlayer')
    matches = models.ManyToManyField(Match, through='TeamMatch')
    season = models.ForeignKey(Season)
    media = models.ForeignKey(TeamMedia)
    icon = models.ImageField(upload_to='stats')
    splash = models.ImageField(upload_to='stats/team_splashes', default='')
    banner = models.ImageField(upload_to='stats/team_banners', blank=True, null=True)
    left_splash = models.ImageField(upload_to='stats/team_splashes', blank=True, null=True)
    right_splash = models.ImageField(upload_to='stats/team_splashes', blank=True, null=True)
    season_win = models.BooleanField(default=False)

    def get_players(self):
        return TeamPlayer.objects.filter(team=self, role__isFill=True)

    def get_average_match_duration(self):
        return TeamMatch.objects.filter(team=self).aggregate(Avg('match__duration'))['match__duration__avg']

    def get_average_match_duration_str(self):
        return time.strftime('%M:%S', time.gmtime(TeamMatch.objects.filter(team=self).aggregate(Avg('match__duration'))['match__duration__avg']))

    def get_average_win_duration(self):
        return TeamMatch.objects.filter(team=self, win=True, match__duration__gte=5).aggregate(Avg('match__duration'))['match__duration__avg']

    def get_average_win_duration_str(self):
        if TeamMatch.objects.filter(team=self, win=True, match__duration__gte=5):
            return time.strftime('%M:%S', time.gmtime(TeamMatch.objects.filter(team=self, win=True, match__duration__gte=5).aggregate(Avg('match__duration'))['match__duration__avg']))
        return "N/A"

    def get_kill_timelines(self):
        return TeamTimeline.objects.filter(team=self)

    def get_overall_timelines(self):
        return SeasonTimeline.objects.filter(season=self.season)

#    def get_kill_timelines(self):
#        team_timelines = TeamTimeline.objects.filter(team=self)
#        results = []
#        for team_timeline in team_timelines:
#            results.append({
#                'minute' : team_timeline.minute,
#                'kills' : team_timeline.kills,
#                'building_kills' : team_timeline.building_kills,
#                'wards_placed' : team_timeline.wards_placed,
#                'wards_killed' : team_timeline.wards_killed
#                })
#        return results
#
#    def get_killed_timelines(self):
#        team_timelines = TeamTimeline.objects.filter(team=self)
#        results = []
#        for team_timeline in team_timelines:
#            results.append({
#                'minute' : team_timeline.minute,
#                'kills' : team_timeline.enemy_kills,
#                'building_kills' : team_timeline.enemy_building_kills,
#                'wards_placed' : team_timeline.enemy_wards_placed,
#                'wards_killed' : team_timeline.enemy_wards_killed
#                })
#        return results
#
#    def get_overall_timelines(self):
#        team_timelines = SeasonTimeline.objects.filter(season=self.season)
#        results = []
#        for team_timeline in team_timelines:
#            results.append({
#                'minute' : team_timeline.minute,
#                'kills' : team_timeline.kills,
#                'building_kills' : team_timeline.building_kills,
#                'wards_placed' : team_timeline.wards_placed,
#                'wards_killed' : team_timeline.wards_killed
#                })
#        return results

    def generate_kill_timelines(self):
        max_minute = self.get_max_timeline_minute()
        building_kills = PlayerMatchBuildingKill.objects.filter(playermatch__team=self)
        kills = PlayerMatchKill.objects.filter(killer__team=self)
        wards_placed = PlayerMatchWardPlace.objects.filter(playermatch__team=self).exclude(ward_type=Ward.objects.get(name='Undefined'))
        wards_killed = PlayerMatchWardKill.objects.filter(playermatch__team=self).exclude(ward_type=Ward.objects.get(name='Undefined'))
        results = []
        for i in range(0, max_minute):
            timestamp = i * 60000
            if self.get_num_matches() > 0:
                results.append({
                    'minute': i, 
                    'kills': 1.0 * kills.filter(timestamp__lt = timestamp).count() / self.get_num_matches(),
                    'building_kills': 1.0 *building_kills.filter(timestamp__lt = timestamp).count() / self.get_num_matches(),
                    'wards_placed': 1.0 * wards_placed.filter(timestamp__lt = timestamp).count() / self.get_num_matches(),
                    'wards_killed': 1.0 * wards_killed.filter(timestamp__lt = timestamp).count() / self.get_num_matches()
                    })

        return results

    def get_player_matches(self):
        return PlayerMatch.objects.filter(team=self)

    def get_enemy_player_matches(self):
        results = []
        for player_match in PlayerMatch.objects.filter(team=self):
            results.append(player_match.get_opponent())
        return results

    def generate_killed_timelines(self):
        max_minute = self.get_max_timeline_minute()
        building_kills = PlayerMatchBuildingKill.objects.filter(playermatch__in=self.get_enemy_player_matches())
        kills = PlayerMatchKill.objects.filter(victim__team=self)
        wards_placed = PlayerMatchWardPlace.objects.filter(playermatch__in=self.get_enemy_player_matches()).exclude(ward_type=Ward.objects.get(name='Undefined'))
        wards_killed = PlayerMatchWardKill.objects.filter(playermatch__in=self.get_enemy_player_matches()).exclude(ward_type=Ward.objects.get(name='Undefined'))
        results = []
        for i in range(0, max_minute):
            timestamp = i * 60000
            if self.get_num_matches() > 0:
                results.append({
                    'minute': i, 
                    'kills': 1.0 * kills.filter(timestamp__lt = timestamp).count() / self.get_num_matches(), 
                    'building_kills': 1.0 * building_kills.filter(timestamp__lt = timestamp).count() / self.get_num_matches(),
                    'wards_placed': 1.0 * wards_placed.filter(timestamp__lt = timestamp).count() / self.get_num_matches(),
                    'wards_killed': 1.0 * wards_killed.filter(timestamp__lt = timestamp).count() / self.get_num_matches()
                    })
        return results

    def generate_overall_timelines(self):
        max_minute = self.get_max_timeline_minute()
        building_kills = PlayerMatchBuildingKill.objects.filter(playermatch__team__season=self.season)
        kills = PlayerMatchKill.objects.filter(killer__team__season=self.season)
        wards_placed = PlayerMatchWardPlace.objects.filter(playermatch__team__season=self.season).exclude(ward_type=Ward.objects.get(name='Undefined'))
        wards_killed = PlayerMatchWardKill.objects.filter(playermatch__team__season=self.season).exclude(ward_type=Ward.objects.get(name='Undefined'))
        num_matches = Match.objects.filter(series__week__season=self.season).exclude(duration=0).count() * 2
        results = []
        for i in range(0, max_minute):
            timestamp = i * 60000
            if num_matches > 0:
                results.append({
                    'minute': i, 
                    'kills': 1.0 * kills.filter(timestamp__lt = timestamp).count() / num_matches, 
                    'building_kills': 1.0 * building_kills.filter(timestamp__lt = timestamp).count() / num_matches,
                    'wards_placed': 1.0 * wards_placed.filter(timestamp__lt = timestamp).count() / num_matches,
                    'wards_killed': 1.0 * wards_killed.filter(timestamp__lt = timestamp).count() / num_matches 
                    })
        return results

    def get_max_timeline_minute(self):
        if self.season.id > 2:
            ret = PlayerMatchTimeline.objects.filter(playermatch__player__team=self).annotate(minute=F('timestamp') / 1000 / 60).order_by('-minute')
            if len(ret) > 0:
                return ret[0].minute
        else:
            return 0
        return 0

    def get_record(self):
	wins = TeamMatch.objects.filter(team=self, win=True, match__series__week__regular=True).count()
	losses = TeamMatch.objects.filter(team=self, win=False, match__series__week__regular=True).exclude(match__duration=0).count()
	return str(wins) + "-" + str(losses)

    def get_sort_record(self):
	wins = TeamMatch.objects.filter(team=self, win=True, match__series__week__regular=True).exclude(match__duration=0).count()
	losses = TeamMatch.objects.filter(team=self, win=False, match__series__week__regular=True).exclude(match__duration=0).count()
        return losses - wins

    def get_top_banned(self):
        num_matches = TeamMatch.objects.filter(team=self).exclude(match__duration=0).count()
        return TeamMatchBan.objects.filter(match__teammatch__team=self).exclude(team=self).exclude(match__duration=0).values('champion', 'champion__name', 'champion__icon').annotate(ban_rate=Count('champion') * 100 / num_matches).order_by('-ban_rate')[:6]

    def get_num_matches(self):
        return TeamMatch.objects.filter(team=self).exclude(match__duration=0).count()

    def get_wins(self):
        return TeamMatch.objects.filter(team=self, win=True).exclude(match__duration=0).count()

    def get_losses(self):
        return TeamMatch.objects.filter(team=self, win=False).exclude(match__duration=0).count()

    def get_regular_wins(self):
        return TeamMatch.objects.filter(team=self, win=True, match__series__week__regular=True).exclude(match__duration=0).count()

    def get_regular_losses(self):
        return TeamMatch.objects.filter(team=self, win=False, match__series__week__regular=True).exclude(match__duration=0).count()

    def get_first_blood_percent(self):
        first_bloods = TeamMatch.objects.filter(team=self, first_blood=True).exclude(match__duration=0).count()
        games = TeamMatch.objects.filter(team=self).exclude(match__duration=0).count()
        if games == 0:
            return 0
        return float(first_bloods) * 100 / games

    def get_first_tower_percent(self):
        first_towers = TeamMatch.objects.filter(team=self, first_tower=True).exclude(match__duration=0).count()
        games = TeamMatch.objects.filter(team=self).exclude(match__duration=0).count()
        if games == 0:
            return 0 
        return float(first_towers) * 100 / games

    def get_tower_kills(self):
        return TeamMatch.objects.filter(team=self).aggregate(Sum('tower_kills'))

    def get_baron_kills(self):
        return TeamMatch.objects.filter(team=self).aggregate(Sum('baron_kills'))

    def __str__(self):
        return self.media.name + " (" + str(self.season) + ")"

class SeasonTimeline(models.Model):
    season = models.ForeignKey(Season)
    minute = models.IntegerField()
    kills = models.FloatField(default=0)
    building_kills = models.FloatField(default=0)
    wards_placed = models.FloatField(default=0)
    wards_killed = models.FloatField(default=0)

    def __str__(self):
        return str(self.season) + " " + str(self.minute) + " minute timeline"

class TeamPlayerTimeline(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    role = models.ForeignKey(Role)
    minute = models.IntegerField()
    gold = models.IntegerField(default=0)
    enemy_gold = models.IntegerField(default=0)
    gold_diff = models.IntegerField(default=0)
    wards_placed = models.IntegerField(default=0)
    wards_killed = models.IntegerField(default=0)

class TeamTimeline(models.Model):
    team = models.ForeignKey(Team)
    minute = models.IntegerField()
    kills = models.FloatField(default=0)
    building_kills = models.FloatField(default=0)
    wards_placed = models.FloatField(default=0)
    wards_killed = models.FloatField(default=0)
    enemy_kills = models.FloatField(default=0)
    enemy_building_kills = models.FloatField(default=0)
    enemy_wards_placed = models.FloatField(default=0)
    enemy_wards_killed = models.FloatField(default=0)

    def __str__(self):
        return self.team.name + " " + str(self.minute) + " minute timeline"

class TeamRole(models.Model):
    team = models.ForeignKey(Team)
    role = models.ForeignKey(Role)

    class Meta:
        unique_together = (("team", "role"))

    def get_team_players(self):
        return TeamPlayer.objects.filter(team=self.team, role=self.role)

class SeriesTeam(models.Model):
    team = models.ForeignKey(Team)
    series = models.ForeignKey(Series)

    class Meta:
        unique_together = (("team", "series"))
    
    def get_wins(self):
	return TeamMatch.objects.filter(team=self.team, win=True, match__series=self.series).exclude(match__duration=0).count()    

    def get_wins_before(self):
	return TeamMatch.objects.filter(team=self.team, win=True, match__series__week__regular=True, match__series__week__number__lt=self.series.week.number).count()
   
    def get_losses_before(self):
	return TeamMatch.objects.filter(team=self.team, win=False, match__series__week__regular=True, match__series__week__number__lt=self.series.week.number).exclude(match__duration=0).count()

    def get_record_before(self):
	wins = TeamMatch.objects.filter(team=self.team, win=True, match__series__week__regular=True, match__series__week__number__lt=self.series.week.number).count()
	losses = TeamMatch.objects.filter(team=self.team, win=False, match__series__week__regular=True, match__series__week__number__lt=self.series.week.number).exclude(match__duration=0).count()
	return str(wins) + "-" + str(losses)

    def get_players(self):
        return SeriesPlayer.objects.filter(team=self.team, series=self.series).order_by('role')



class PlayerRole(models.Model):
    player = models.ForeignKey(Player)
    role = models.ForeignKey(Role)
    priority = models.IntegerField(default=10)

    class Meta:
        unique_together = (("player", "role"))

class SeriesCastTeam(models.Model):
    series = models.ForeignKey(Series)
    team = models.ForeignKey(Team)

class SeriesCastPlayer(models.Model):
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
    role = models.ForeignKey(Role)
    series = models.ForeignKey(Series)

class SeriesPlayer(models.Model):
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
    role = models.ForeignKey(Role)
    series = models.ForeignKey(Series)

class PlayerMatch(models.Model):
    player = models.ForeignKey(Player)
    match = models.ForeignKey(Match)
    role = models.ForeignKey(Role, default=0)
    team = models.ForeignKey(Team)
    participant_id = models.IntegerField(default=0)
    champion = models.ForeignKey(Champion, default=0)
    participant_id = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    physical_damage_dealt = models.IntegerField(default=0)
    neutral_minions_killed_team_jungle = models.IntegerField(default=0)
    magic_damage_dealt = models.IntegerField(default=0)
    neutral_minions_killed_enemy_jungle = models.IntegerField(default=0)
    largest_critical_strike = models.IntegerField(default=0)
    total_damage_dealt = models.IntegerField(default=0)
    magic_damage_dealt_to_champions = models.IntegerField(default=0)
    vision_wards_bought_in_game = models.IntegerField(default=0)
    damage_dealt_to_objectives = models.IntegerField(default=0)
    largest_killing_spree = models.IntegerField(default=0)
    double_kills = models.IntegerField(default=0)
    triple_kills = models.IntegerField(default=0)
    quadra_kills = models.IntegerField(default=0)
    penta_kills = models.IntegerField(default=0)
    total_time_crowd_control_dealt = models.IntegerField(default=0)
    longest_time_spent_living = models.IntegerField(default=0)
    wards_killed = models.IntegerField(default=0)
    first_tower_assist = models.BooleanField(default=False)
    first_tower_kill = models.BooleanField(default=False)
    first_blood_assist = models.BooleanField(default=False)
    vision_score = models.IntegerField(default=0)
    wards_placed = models.IntegerField(default=0)
    turret_kills = models.IntegerField(default=0)
    damage_self_mitigated = models.IntegerField(default=0)
    champ_level = models.IntegerField(default=0)
    first_inhibitor_kill = models.BooleanField(default=False)
    gold_earned = models.IntegerField(default=0)
    magical_damage_taken = models.IntegerField(default=0)
    true_damage_taken = models.IntegerField(default=0)
    first_inhibitor_assist = models.BooleanField(default=False)
    neutral_minions_killed = models.IntegerField(default=0)
    damage_dealt_to_turrets = models.IntegerField(default=0)
    physical_damage_dealt_to_champions = models.IntegerField(default=0)
    gold_spent = models.IntegerField(default=0)
    true_damage_dealt = models.IntegerField(default=0)
    true_damage_dealt_to_champions = models.IntegerField(default=0)
    total_heal = models.IntegerField(default=0)
    total_minions_killed = models.IntegerField(default=0)
    first_blood_kill = models.BooleanField(default=False)
    sight_wards_bought_in_game = models.IntegerField(default=0)
    total_damage_dealt_to_champions = models.IntegerField(default=0)
    inhibitor_kills = models.IntegerField(default=0)
    total_damage_taken = models.IntegerField(default=0)
    killing_sprees = models.IntegerField(default=0)
    time_ccing_others = models.IntegerField(default=0)
    physical_damage_taken = models.IntegerField(default=0)

    class Meta:
        unique_together = (("player", "match"))

    def win(self):
        return self.match.get_winner().team == self.team

    def get_cs(self):
        return self.neutral_minions_killed + self.total_minions_killed

    def get_timelines(self):
        return PlayerMatchTimeline.objects.filter(playermatch=self).annotate(minute=F('timestamp') / 1000 / 60)

    def get_opponent(self):
        return PlayerMatch.objects.filter(match=self.match, role=self.role).exclude(team=self.team)[0]

class TeamPlayer(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player)
    role = models.ForeignKey(Role)
    isLeader = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    csDiffAt15 = models.FloatField(default=0)
    csPerMin = models.FloatField(default=0)
    killParticipation = models.FloatField(default=0)
    teamDamagePercent = models.FloatField(default=0)

    def get_player(self):
        return Playerercent .objects.filter(pk=self.player)

    def get_team(self):
        return Team.objects.filter(pk=self.team)
    
    def get_proximity_timeline(self):
        all_timelines = PlayerMatchTimeline.objects.filter(playermatch__player=self.player, playermatch__role=self.role, playermatch__team=self.team).annotate(minute=F('timestamp') / 1000 / 60).order_by('minute')
        num_games = self.get_player_matches().count()
        results = []
        for i in range(0, 25):
            timelines = all_timelines.filter(minute=i)
            topSum = 0
            midSum = 0
            botSum = 0
            for timeline in timelines:
                #if math.hypot(timeline.position_x - 1800, timeline.position_y - 13000) < 6500:
                if timeline.position_x < 5000 and timeline.position_y > 9500:
#                    topSum = topSum + ((6000 - math.hypot(timeline.position_x - 1800, timeline.position_y - 13000)) ** 2) / 10000
                    topSum = topSum + (6500 - math.hypot(timeline.position_x - 1800, timeline.position_y - 13000)) / num_games
                if timeline.position_x > 5000 and timeline.position_x < 10500 and timeline.position_y > 4800 and timeline.position_y < 9500:
                #if math.hypot(timeline.position_x - 7500, timeline.position_y - 7500) < 5000:
#                    midSum = midSum + ((6000 - math.hypot(timeline.position_x - 7500, timeline.position_y - 7500)) ** 2) / 10000
                    midSum = midSum + (6500 - math.hypot(timeline.position_x - 7500, timeline.position_y - 7500)) / num_games
                #if math.hypot(timeline.position_x - 13000, timeline.position_y - 1800) < 6500:

                if timeline.position_x > 10500 and timeline.position_y < 4800:
#                    botSum = botSum + ((6000 - math.hypot(timeline.position_x - 13000, timeline.position_y - 1800)) ** 2) / 10000
                    botSum = botSum + (6500 - math.hypot(timeline.position_x - 13000, timeline.position_y - 1800)) / num_games
            results.append({
                'minute': i,
                'top': topSum,
                'mid': midSum,
                'bot': botSum
            })
        return results

    def get_proximity_timeline_max(self):
        timelines = self.get_proximity_timeline()

        result = 0
        for timeline in timelines:
            if max(timeline['top'], timeline['mid'], timeline['bot']) > result:
                result = max(timeline['top'], timeline['mid'], timeline['bot'])

        return result

    def get_num_matches(self):
        if self.role.isFill == True:
            return PlayerMatch.objects.filter(team=self.team, player=self.player).count()
        return PlayerMatch.objects.filter(team=self.team, player=self.player, role=self.role).count()

    def get_percent_teams_control_wards(self):
        if self.role.isFill == True:
            matches = Match.objects.filter(playermatch__player=self.player)
            match_ids = [o.id for o in matches]
    
            total_control_wards = PlayerMatch.objects.filter(match__id__in=match_ids, team=self.team).aggregate(control_wards=Sum('vision_wards_bought_in_game'))['control_wards']
            player_control_wards= PlayerMatch.objects.select_related().filter(player=self.player, team=self.team).aggregate(control_wards=Sum('vision_wards_bought_in_game'))['control_wards']
        else:
            matches = Match.objects.filter(playermatch__player=self.player, playermatch__role=self.role)
            match_ids = [o.id for o in matches]
    
            total_control_wards = PlayerMatch.objects.filter(match__id__in=match_ids, team=self.team).aggregate(control_wards=Sum('vision_wards_bought_in_game'))['control_wards']
            player_control_wards = PlayerMatch.objects.select_related().filter(player=self.player, team=self.team, role=self.role).aggregate(control_wards=Sum('vision_wards_bought_in_game'))['control_wards']

        if total_control_wards == None:
            return 0
        return 100.0 * player_control_wards / total_control_wards

    def get_percent_control_ward_gold(self):
        playermatches = self.get_player_matches().aggregate(total_gold_earned=Sum('gold_earned'), control_wards=Sum('vision_wards_bought_in_game'))
        return 100.0 * playermatches['control_wards'] * 75.0 / playermatches['total_gold_earned']

    def get_vision_timeline(self):
        results = []
        if self.get_num_matches() == 0:
            return results
        max_minute = self.team.get_max_timeline_minute()
        wards_placed = PlayerMatchWardPlace.objects.filter(playermatch__team=self.team, playermatch__player=self.player, playermatch__role=self.role, ward_type__in=(Ward.objects.filter(name='Control Ward')|Ward.objects.filter(name='Yellow Trinket Ward')|Ward.objects.filter(name='Sight Ward')|Ward.objects.filter(name='Blue Trinket')))
        wards_killed = PlayerMatchWardKill.objects.filter(playermatch__team=self.team, playermatch__player=self.player, playermatch__role=self.role, ward_type__in=(Ward.objects.filter(name='Control Ward')|Ward.objects.filter(name='Yellow Trinket Ward')|Ward.objects.filter(name='Sight Ward')|Ward.objects.filter(name='Blue Trinket')))
        for i in range(0, max_minute):
            timestamp = i * 60000
            results.append({
                'minute': i, 
                'wards_placed': 1.0 * wards_placed.filter(timestamp__lt = timestamp).count() / self.get_num_matches(),
                'wards_killed': 1.0 * wards_killed.filter(timestamp__lt = timestamp).count() / self.get_num_matches()
                })

        return results

#    def get_gold_timeline(self):
#        team_player_timelines = TeamPlayerTimeline.objects.filter(player=self.player, team=self.team, role=self.role)
#        return team_player_timelines

    def get_gold_timeline(self):
        max_minute = self.team.get_max_timeline_minute()
        timelines = self.get_timelines()
        enemy_timelines = self.get_enemy_timelines()
        player_matches = self.get_player_matches()
        enemy_player_matches = self.get_enemy_player_matches()
        results = []
        total_matches = Match.objects.filter(series__week__season=self.team.season).exclude(duration=0).count() * 2

        if player_matches.count() == 0:
            return results
        for i in range(0, max_minute):
            timestamp = i * 60000
            goldSum = 0
            for player_match in player_matches:
                goldSum += PlayerMatchTimeline.objects.filter(playermatch=player_match, timestamp__lte=timestamp).order_by('-timestamp')[0].totalGold
            enemyGoldSum = 0
            for player_match in enemy_player_matches:
                enemyGoldSum += PlayerMatchTimeline.objects.filter(playermatch=player_match, timestamp__lte=timestamp).order_by('-timestamp')[0].totalGold
            goldSum /= player_matches.count()
            enemyGoldSum /= player_matches.count()
            results.append({
                'minute': i, 
                'avgGold': 1.0 * goldSum,
                'avgOppGold': 1.0 * enemyGoldSum,
                'goldDiff': 1.0 * goldSum - enemyGoldSum
                })
        return results


    def get_timelines(self):
        if self.role.isFill == True:
            timelines = PlayerMatchTimeline.objects.filter(playermatch__player=self.player, playermatch__team=self.team).annotate(minute=F('timestamp') / 1000 / 60)
        else: 
            timelines = PlayerMatchTimeline.objects.filter(playermatch__player=self.player, playermatch__team=self.team, playermatch__role=self.role).annotate(minute=F('timestamp') / 1000 / 60)
        if timelines == None:
            return None

        timelines = timelines.values('minute').annotate(avgGold=Avg('totalGold'))
        return timelines

    def get_enemy_timelines(self):
        timelines = PlayerMatchTimeline.objects.filter(playermatch__in=self.get_enemy_player_matches()).annotate(minute=F('timestamp') / 1000 / 60)

        timelines = timelines.values('minute').annotate(avgGold=Avg('totalGold'))
        return timelines

    def get_avg_vision(self):
        if self.role.isFill == True:
            avg_vision = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(avg_vision=Avg('playermatch__vision_score'))['avg_vision']
        else: 
            avg_vision = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team, playermatch__role=self.role).aggregate(avg_vision=Avg('playermatch__vision_score'))['avg_vision']
        if avg_vision == None:
            return 0
        return avg_vision

    def get_avg_kills(self):
        if self.role.isFill == True:
            avg_kills = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(avg_kills=Avg('playermatch__kills'))['avg_kills']
        else: 
            avg_kills = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team, playermatch__role=self.role).aggregate(avg_kills=Avg('playermatch__kills'))['avg_kills']
        if avg_kills == None:
            return 0
        return avg_kills

    def get_avg_deaths(self):
        if self.role.isFill == True:
            avg_deaths = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(avg_deaths=Avg('playermatch__deaths'))['avg_deaths']
        else:
            avg_deaths = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team, playermatch__role=self.role).aggregate(avg_deaths=Avg('playermatch__deaths'))['avg_deaths']
        if avg_deaths == None:
            return 0
        return avg_deaths

    def get_avg_assists(self):
        if self.role.isFill == True:
            avg_assists = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(avg_assists=Avg('playermatch__assists'))['avg_assists']
        else:
            avg_assists = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team, playermatch__role=self.role).aggregate(avg_assists=Avg('playermatch__assists'))['avg_assists']
        if avg_assists == None:
            return 0
        return avg_assists

    def get_kda(self):
        if self.role.isFill == True:
            kills = PlayerMatch.objects.filter(player=self.player, team=self.team).aggregate(sum_kills=Sum('kills'))['sum_kills']
            deaths = PlayerMatch.objects.filter(player=self.player, team=self.team).aggregate(sum_deaths=Sum('deaths'))['sum_deaths']
            assists = PlayerMatch.objects.filter(player=self.player, team=self.team).aggregate(sum_assists=Sum('assists'))['sum_assists']
        else:
            kills = PlayerMatch.objects.filter(player=self.player, team=self.team, role=self.role).aggregate(sum_kills=Sum('kills'))['sum_kills']
            deaths = PlayerMatch.objects.filter(player=self.player, team=self.team, role=self.role).aggregate(sum_deaths=Sum('deaths'))['sum_deaths']
            assists = PlayerMatch.objects.filter(player=self.player, team=self.team, role=self.role).aggregate(sum_assists=Sum('assists'))['sum_assists']

        if deaths == None:
            return 0
        if deaths == 0:
            return 1000000
        return (float(kills) + assists) / deaths

    def get_cs_per_min(self):
        return self.csPerMin

    def generate_cs_per_min(self):
        if self.role.isFill == True:
            cs = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(cs=Avg((F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed')) * 60.0 / F('duration')))['cs']
        else:
            cs = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team, playermatch__role=self.role).aggregate(cs=Avg((F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed')) * 60.0 / F('duration')))['cs']
        if cs == None or cs > 100:
            return 0
        return cs 

    def get_cs_per_game(self):
        if self.role.isFill == True:
            cs = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(cs=Avg((F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed'))))['cs']
        else:
            cs = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team, playermatch__role=self.role).aggregate(cs=Avg((F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed'))))['cs']
        if cs == None:
            return 0
        return cs 
    
    def get_distinct_champs_played(self):
        if self.role.isFill == True:
            return PlayerMatch.objects.filter(player=self.player, team=self.team).values('champion').aggregate(num_champs=Count('champion', distinct=True))['num_champs']
        else: 
            return PlayerMatch.objects.filter(player=self.player, team=self.team, role=self.role).values('champion').aggregate(num_champs=Count('champion', distinct=True))['num_champs']

    def get_percent_team_damage(self):
        return self.teamDamagePercent

    def generate_percent_team_damage(self):
        if self.role.isFill == True:
            matches = Match.objects.filter(playermatch__player=self.player)
            match_ids = [o.id for o in matches]
    
            total_dmg_to_champs = PlayerMatch.objects.filter(match__id__in=match_ids, team=self.team).aggregate(dmg__sum=Sum('total_damage_dealt_to_champions'))['dmg__sum']
            player_dmg_to_champs = PlayerMatch.objects.select_related().filter(player=self.player, team=self.team).aggregate(dmg__sum=Sum('total_damage_dealt_to_champions'))['dmg__sum']
        else:
            matches = Match.objects.filter(playermatch__player=self.player, playermatch__role=self.role)
            match_ids = [o.id for o in matches]
    
            total_dmg_to_champs = PlayerMatch.objects.filter(match__id__in=match_ids, team=self.team).aggregate(dmg__sum=Sum('total_damage_dealt_to_champions'))['dmg__sum']
            player_dmg_to_champs = PlayerMatch.objects.select_related().filter(player=self.player, team=self.team, role=self.role).aggregate(dmg__sum=Sum('total_damage_dealt_to_champions'))['dmg__sum']

        if total_dmg_to_champs == None:
            return 0
        return 100.0 * player_dmg_to_champs / total_dmg_to_champs 

    def get_kill_participation(self):
        return self.killParticipation

    def generate_kill_participation(self):
        if self.role.isFill == True:
            matches = Match.objects.filter(playermatch__player=self.player)
            match_ids = [o.id for o in matches]
    
            total_kills = PlayerMatch.objects.filter(match__id__in=match_ids, team=self.team).aggregate(kills__sum=Sum('kills'))['kills__sum']
            player_kills_assists = PlayerMatch.objects.select_related().filter(player=self.player, team=self.team).aggregate(kills__sum=Sum(F('kills') + F('assists')))['kills__sum']
        else:
            matches = Match.objects.filter(playermatch__player=self.player, playermatch__role=self.role)
            match_ids = [o.id for o in matches]
    
            total_kills = PlayerMatch.objects.filter(match__id__in=match_ids, team=self.team).aggregate(kills__sum=Sum('kills'))['kills__sum']
            player_kills_assists = PlayerMatch.objects.select_related().filter(player=self.player, team=self.team, role=self.role).aggregate(kills__sum=Sum(F('kills') + F('assists')))['kills__sum']
        if player_kills_assists == None:
            return 0
        return 100.0 * player_kills_assists / total_kills

    def get_played_champion_list(self):
        if self.role.isFill == True:
            return Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).values('playermatch__champion', 'playermatch__champion__name', 'playermatch__champion__icon').annotate(champion_count=Count('playermatch__champion'), average_vision_score=Avg('playermatch__vision_score'), avg_kills=Avg('playermatch__kills'), avg_deaths=Avg('playermatch__deaths'), avg_assists=Avg('playermatch__assists'), winrate=Avg(F('teammatch__win') * 100), cs_per_min=Avg((F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed')) * 60.0 / F('duration')), average_cs=Avg(F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed'))).order_by('-champion_count')
        else:
            return Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team, playermatch__role=self.role).values('playermatch__champion', 'playermatch__champion__name', 'playermatch__champion__icon').annotate(champion_count=Count('playermatch__champion'), average_vision_score=Avg('playermatch__vision_score'), avg_kills=Avg('playermatch__kills'), avg_deaths=Avg('playermatch__deaths'), avg_assists=Avg('playermatch__assists'), winrate=Avg(F('teammatch__win') * 100), cs_per_min=Avg((F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed')) * 60.0 / F('duration')), average_cs=Avg(F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed')), wins=Sum('teammatch__win'), losses=ExpressionWrapper(Count('playermatch__champion') - Sum('teammatch__win'), output_field=models.IntegerField())).order_by('-champion_count')

    def get_player_matches(self):
        if self.role.isFill == True:
            return PlayerMatch.objects.filter(player=self.player, team=self.team)
        else:
            return PlayerMatch.objects.filter(player=self.player, team=self.team, role=self.role)

    def get_enemy_player_matches(self):
        results = []
        for player_match in self.get_player_matches():
            results.append(player_match.get_opponent())
        return results

    def get_cs_diff_at_15(self):
        return self.csDiffAt15

    def generate_cs_diff_at_15(self):
        if self.team.season.id < 3:
            return 0
        player_matches = self.get_player_matches()
        result = 0
        for playermatch in player_matches:
            timeline = PlayerMatchTimeline.objects.filter(playermatch=playermatch, timestamp__lt=910000).values('timestamp', 'minions_killed', 'monsters_killed', 'playermatch').annotate(cs=F('minions_killed')+F('monsters_killed')).order_by('-timestamp')[0]
            enemy_timeline = PlayerMatchTimeline.objects.filter(playermatch__match=playermatch.match, playermatch__role=playermatch.role, timestamp__lt=910000).exclude(playermatch__team=playermatch.team).values('timestamp', 'minions_killed', 'monsters_killed', 'playermatch').annotate(cs=F('minions_killed')+F('monsters_killed')).order_by('-timestamp')[0]
            result = result + timeline['cs'] - enemy_timeline['cs']
        if player_matches.count() == 0:
            return 0.0
        return 1.0 * result / player_matches.count()

class TeamMatch(models.Model):
    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    side = models.CharField(max_length=5)
    win = models.BooleanField(default=False)
    first_dragon = models.BooleanField(default=False)
    first_inhibitor = models.BooleanField(default=False)
    baron_kills = models.IntegerField(default=0)
    first_rift_herald = models.BooleanField(default=False)
    first_blood = models.BooleanField(default=False)
    first_tower = models.BooleanField(default=False)
    inhibitor_kills = models.IntegerField(default=0)
    tower_kills = models.IntegerField(default=0)

    class Meta:
        unique_together = (("team", "match"))

    def get_player_matches(self):
        return PlayerMatch.objects.filter(match=self.match, team=self.team)

    def get_team_bans(self):
        return TeamMatchBan.objects.filter(match=self.match, team=self.team).order_by('-pickTurn')

    def get_timelines(self):
        return PlayerMatchTimeline.objects.filter(playermatch__match=self.match, playermatch__team=self.team).annotate(minute=F('timestamp') / 1000 / 60).values('minute').annotate(sumGold=Sum('totalGold'))

    def get_enemy_timelines(self):
        return PlayerMatchTimeline.objects.filter(playermatch__match=self.match).exclude(playermatch__team=self.team).annotate(minute=F('timestamp') / 1000 / 60).values('minute').annotate(sumGold=Sum('totalGold'))

    def get_timeline_diffs(self):
        enemy_timelines = self.get_enemy_timelines()
        gold_diff_timelines = []
        for timeline in self.get_timelines():
            gold_diff_timelines.append({'minute': timeline['minute'], 'sumGold': timeline['sumGold'] - enemy_timelines.get(minute=timeline['minute'])['sumGold']})
        return gold_diff_timelines





class TeamMatchBan(models.Model):
    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    champion = models.ForeignKey(Champion)
    pickTurn = models.IntegerField(default=0)

    class Meta:
        ordering = ["champion"]

class Item(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=5000)
    icon = models.ImageField(upload_to='stats/item/icon', default='')

class PlayerMatchItem(models.Model):
    playermatch = models.ForeignKey(PlayerMatch)
    item = models.ForeignKey(Item)

class Lane(models.Model):
    name = models.CharField(max_length=10)
    riot_name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Ward(models.Model):
    name = models.CharField(max_length=25)
    riot_name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Building(models.Model):
    lane = models.ForeignKey(Lane)
    name = models.CharField(max_length=25)
    riot_name = models.CharField(max_length=25)
    riot_subname = models.CharField(max_length=25, default="")
    
    def __str__(self):
        return str(self.lane) + ' ' + self.name

class EliteMonster(models.Model):
    name = models.CharField(max_length=25)
    riot_name = models.CharField(max_length=25)
    riot_subname = models.CharField(max_length=25, default="")

    def __str__(self):
        return self.name

class PlayerMatchKill(models.Model):
    killer = models.ForeignKey(PlayerMatch)
    victim = models.ForeignKey(PlayerMatch, related_name="victim")
    timestamp = models.IntegerField()
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)

class PlayerMatchAssist(models.Model):
    kill = models.ForeignKey(PlayerMatchKill)
    playermatch = models.ForeignKey(PlayerMatch)

class PlayerMatchWardPlace(models.Model):
    playermatch = models.ForeignKey(PlayerMatch)
    ward_type = models.ForeignKey(Ward)
    timestamp = models.IntegerField()

class PlayerMatchWardKill(models.Model):
    playermatch = models.ForeignKey(PlayerMatch)
    ward_type = models.ForeignKey(Ward)
    timestamp = models.IntegerField()

class PlayerMatchBuildingKill(models.Model):
    playermatch = models.ForeignKey(PlayerMatch)
    building_type = models.ForeignKey(Building)
    timestamp = models.IntegerField()

class PlayerMatchBuildingAssist(models.Model):
    kill = models.ForeignKey(PlayerMatchBuildingKill)
    playermatch = models.ForeignKey(PlayerMatch)

class PlayerMatchEliteMonsterKill(models.Model):
    playermatch = models.ForeignKey(PlayerMatch)
    monster_type = models.ForeignKey(EliteMonster)
    timestamp = models.IntegerField()

class PlayerMatchTimeline(models.Model):
    playermatch = models.ForeignKey(PlayerMatch)
    timestamp = models.IntegerField()
    level = models.IntegerField(default=1)
    gold = models.IntegerField(default=0)
    totalGold = models.IntegerField(default=0)
    minions_killed = models.IntegerField(default=0)
    monsters_killed = models.IntegerField(default=0)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)

class HypeVideo(models.Model):
    season = models.ForeignKey(Season)
    creator = models.ForeignKey(Player)
    youtube_link = models.CharField(max_length=100, default='')


class TeamInvite(models.Model):
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)

class PlayerPhotoRequest(models.Model):
    player = models.ForeignKey(Player)
    photo = models.ImageField(upload_to='stats/player_photos')

class SeasonPlayer(models.Model):
    season = models.ForeignKey(Season)
    player = models.ForeignKey(Player)
    elo_value = models.IntegerField(default=100)

class SeasonPlayerRole(models.Model):
    season = models.ForeignKey(Season)
    player = models.ForeignKey(Player)
    role = models.ForeignKey(Role)
    isMain = models.BooleanField(default=False)

class UserAccount(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    isMain = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ": " + self.name
