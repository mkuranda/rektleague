from riot_request import *
import urllib, shutil
import math
from .models import Item, Champion, Match, Team, TeamMatch, Role, TeamPlayer, PlayerMatch, Week, Series, SeriesTeam, TeamMatchBan, SeriesPlayer
from .models import PlayerMatchKill, PlayerMatchAssist, PlayerMatchWardPlace, PlayerMatchWardKill, PlayerMatchBuildingKill, PlayerMatchBuildingAssist, PlayerMatchEliteMonsterKill, PlayerMatchTimeline
from .models import Lane, Ward, Building, EliteMonster, Season, SeasonChampion, TeamTimeline, SeasonTimeline, TeamPlayerTimeline

class ObjectNotFound(Exception) :
    """Raised when we can't find an object in db or from riot API"""
    pass

def get_all_summoner_spells(riot_id):
    requester = RiotRequester('/lol/static-data/v3/summoner-spells/')
    requester.add_tag("image")
    try:
        total_ss_data = requester.request("")
    except RiotNotFound:
        raise ObjectNotFound("Summoner Spells")

    for ss_id in total_ss_data["data"]:
        ss_data = total_ss_data["data"][ss_id]
        ss_exists = True
        try:
            ss = SummonerSpell.objects.get(id=ss_id)
        except SummonerSpell.DoesNotExist:
            ss_exists = False

        if ss_exists == False or ss.name == "" or ss.description == "" or ss.icon == "":
            if ss_exists == False:
                ss = SummonerSpell.objects.create(id=ss_id)
            ss.name = ""
            if "name" in ss_data:
                ss.name = ss_data["name"]
            r = requests.get("http://ddragon.leagueoflegends.com/cdn/10.6.1/img/item/" + ss_data["image"]["full"], stream=True)
            if r.status_code == 200:
                with open("media/stats/summoner-spell/icon/" + ss_data["image"]["full"], 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
	    ss.icon = "stats/summoner-spell/icon/" + ss_data["image"]["full"]
            ss.save()


def get_all_items(riot_id):
    requester = RiotRequester('/lol/static-data/v3/items/')
    requester.add_tag("image")
    try:
        total_item_data = requester.request("")
    except RiotNotFound:
        raise ObjectNotFound("Items")

    for item_id in total_item_data["data"]:
        item_data = total_item_data["data"][item_id]
        item_exists = True
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            item_exists = False

        if item_exists == False or item.name == "" or item.description == "" or item.icon == "":
            if item_exists == False:
                item = Item.objects.create(id=item_id)
            item.name = ""
            if "name" in item_data:
                item.name = item_data["name"]
            item.description = ""
            if "description" in item_data:
                item.description = item_data["description"]
            r = requests.get("http://ddragon.leagueoflegends.com/cdn/10.6.1/img/item/" + item_data["image"]["full"], stream=True)
            if r.status_code == 200:
                with open("media/stats/item/icon/" + item_data["image"]["full"], 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
#	    else:
#	        raise ObjectNotFound("Item Image " + item_data["image"]["full"])

	    item.icon = "stats/item/icon/" + item_data["image"]["full"]
            item.save()


def get_item(riot_id):
    try:
        item = Item.objects.get(id=riot_id)
    except Item.DoesNotExist:
        requester = RiotRequester('/lol/static-data/v3/items/')
        try:
            item_data = requester.request(str(riot_id))
        except RiotNotFound:
            raise ObjectNotFound("Item " + str(riot_id))
        item = Item.objects.create(riot_id)
        item.name = item_data["name"]
	r = requests.get("http://ddragon.leagueoflegends.com/cdn/10.6.1/img/item/" + item_data["image"]["full"], stream=True)
        if r.status_code == 200:
            with open("media/stats/item/icon" + item_data["image"]["full"], 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
	else:
	    raise ObjectNotFound("Item Image " + item_data["image"]["full"])
        item.description = item_data["description"]
        item.save()
    return item

def get_champions():
    url = 'http://ddragon.leagueoflegends.com/cdn/10.6.1/data/en_US/champion.json'
    r = requests.get(url).json()
    for champion_name in r['data']:
        champion_data = r['data'][champion_name]
        name = champion_data['name']
        key = champion_data['key']
        title = champion_data['title']
        try:
            champion = Champion.objects.get(id=key)
        except Champion.DoesNotExist:
            champion = Champion.objects.create(id=key, name=name, title=title)
        champion.name = name
        champion.title = title
	result = requests.get("http://ddragon.leagueoflegends.com/cdn/10.6.1/img/champion/" + champion_data["image"]["full"], stream=True)
        with open("media/stats/champion/icon/" + champion_data["image"]["full"], 'wb') as f:
            result.raw.decode_content = True
            shutil.copyfileobj(result.raw, f)
	champion.icon = "stats/champion/icon/" + champion_data["image"]["full"]
        champion.save()
        seasons = Season.objects.all()
        for season in seasons:
            try:
                champion_season = SeasonChampion.objects.get(season=season, champion=champion)
            except SeasonChampion.DoesNotExist:
                champion_season = SeasonChampion.objects.create(season=season, champion=champion)
                champion_season.save()
    return r

def get_champion(riot_id):
    champion_exists = True
    try:
        champion = Champion.objects.get(id=riot_id)
    except Champion.DoesNotExist:
        champion_exists = False

    url = 'http://ddragon.leagueoflegends.com/cdn/10.6.1/data/en_US/champion.json'
    r = requests.get(url).json()
    if champion_exists == False or champion.name == "" or champion.title == "" or champion.icon == "":
        for champion_name in r['data']:
            champion_data = r['data'][champion_name]
            name = champion_data['name']
            key = champion_data['key']
            title = champion_data['title']
            if key == riot_id:
                try:
                    champion = Champion.objects.get(id=key)
                except Champion.DoesNotExist:
                    champion = Champion.objects.create(id=key, name=name, title=title)
                champion.name = name
                champion.title = title
                result = requests.get("http://ddragon.leagueoflegends.com/cdn/10.6.1/img/champion/" + champion_data["image"]["full"], stream=True)
                with open("media/stats/champion/icon/" + champion_data["image"]["full"], 'wb') as f:
                    result.raw.decode_content = True
                    shutil.copyfileobj(result.raw, f)
                champion.icon = "stats/champion/icon/" + champion_data["image"]["full"]
                champion.save()
                seasons = Season.objects.all()
                for season in seasons:
                    try:
                        champion_season = SeasonChampion.objects.get(season=season, champion=champion)
                    except SeasonChampion.DoesNotExist:
                        champion_season = SeasonChampion.objects.create(season=season, champion=champion)
                        champion_season.save()
    return champion

def get_ward_type(riot_ward_type):
    if riot_ward_type == "YELLOW_TRINKET":
        return "Yellow Trinket Ward"
    elif riot_ward_type == "CONTROL_WARD":
        return "Control Ward"
    elif riot_ward_type == "SIGHT_WARD":
        return "Sight Ward"
    return ""

def get_building_type(riot_building_type, riot_building_subtype):
    if riot_building_type == "TOWER_BUILDING" and riot_building_subtype == "OUTER_TURRET":
        return "Outer Turret"
    elif riot_building_type == "TOWER_BUILDING" and riot_building_subtype == "INNER_TURRET":
        return "Inner Turret"
    elif riot_building_type == "TOWER_BUILDING" and riot_building_subtype == "BASE_TURRET":
        return "Base Turret"
    elif riot_building_type == "TOWER_BUILDING" and riot_building_subtype == "NEXUS_TURRET":
        return "Nexus Turret"
    elif riot_building_type == "INHIBITOR_BUILDING":
        return "Inhibitor"
    return ""

def get_elite_monster_type(riot_monster_type, riot_monster_subtype):
    if riot_monster_type == "DRAGON" and riot_monster_subtype == "FIRE_DRAGON":
        return "Infernal Dragon"
    if riot_monster_type == "DRAGON" and riot_monster_subtype == "EARTH_DRAGON":
        return "Mountain Dragon"
    if riot_monster_type == "DRAGON" and riot_monster_subtype == "AIR_DRAGON":
        return "Air Dragon"
    if riot_monster_type == "DRAGON" and riot_monster_subtype == "WATER_DRAGON":
        return "Ocean Dragon"
    if riot_monster_type == "DRAGON" and riot_monster_subtype == "ELDER_DRAGON":
        return "Elder Dragon"
    if riot_monster_type == "RIFTHERALD":
        return "Rift Herald"
    if riot_monster_type == "BARON":
        return "Baron"
    return ""

def get_lane_type(riot_lane_type):
    if riot_lane_type == "TOP_LANE":
        return "Top"
    elif riot_lane_type == "MID_LANE":
        return "Mid"
    elif riot_lane_type == "BOT_LANE":
        return "Bot"
    return ""

def get_match_timeline(match_id):
    try:
        match = Match.objects.get(id=match_id)
    except:
        raise ObjectNotFound("Match " + str(match_id))
    
    match_timeline_requester = RiotRequester('/lol/match/v4/timelines/by-match/')
    match_timeline_data = match_timeline_requester.request(str(match.riot_id))

    participants = PlayerMatch.objects.filter(match=match).order_by('participant_id')

    frame_data = match_timeline_data['frames']
    for frame in frame_data:
        timestamp = frame['timestamp']
        for participant in participants:
            a = participant.participant_id
            data = frame['participantFrames'][str(participant.participant_id)]
            timeline = PlayerMatchTimeline.objects.create(playermatch=participant, timestamp = timestamp)
            timeline.level = data['level']
            timeline.gold = data['currentGold']
            timeline.totalGold = data['totalGold']
            timeline.minions_killed = data['minionsKilled']
            timeline.monsters_killed = data['jungleMinionsKilled']
            if 'position' in data:
                timeline.position_x = data['position']['x']
                timeline.position_y = data['position']['y']
            timeline.xp = data['xp']
            timeline.save()
        for event_data in frame['events']:
            if event_data['type'] == 'CHAMPION_KILL':
                if event_data['killerId'] > 0 and event_data['victimId'] > 0:
                    killer = participants[event_data['killerId'] - 1]
                    victim = participants[event_data['victimId'] - 1]
                    event = PlayerMatchKill.objects.create(killer=killer, victim=victim, timestamp=event_data['timestamp'])
                    if 'position' in event_data:
                        event.position_x = event_data['position']['x']
                        event.position_y = event_data['position']['y']
                    event.save()
                    for assist_id in event_data['assistingParticipantIds']:
                        assist = PlayerMatchAssist.objects.create(kill=event, playermatch=participants[assist_id - 1])
                        assist.save()
            elif event_data['type'] == 'WARD_PLACED':
                if event_data['creatorId'] > 0:
                    ward_type = Ward.objects.get(riot_name=event_data['wardType'])
                    event = PlayerMatchWardPlace.objects.create(playermatch=participants[event_data['creatorId'] - 1], timestamp=event_data['timestamp'], ward_type=ward_type)
                    event.save()
            elif event_data['type'] == 'WARD_KILL':
                if event_data['killerId'] > 0:
                    ward_type = Ward.objects.get(riot_name=event_data['wardType'])
                    event = PlayerMatchWardKill.objects.create(playermatch=participants[event_data['killerId'] - 1], timestamp=event_data['timestamp'], ward_type=ward_type)
                    event.save()
            elif event_data['type'] == 'BUILDING_KILL':
                if event_data['killerId'] > 0:
                    killer = participants[event_data['killerId'] - 1]
                    buildingSubtype = " "
                    if 'laneType' in event_data and 'towerType' in event_data:
                        building_type = Building.objects.get(riot_name=event_data['buildingType'], riot_subname=event_data['towerType'], lane__riot_name=event_data['laneType'])
                    elif 'towerType' in event_data:
                        building_type = Building.objects.get(riot_name=event_data['buildingType'], riot_subname=event_data['towerType'])
                    elif 'laneType' in event_data:
                        building_type = Building.objects.get(riot_name=event_data['buildingType'], lane__name=event_data['laneType'])
                    else:
                        building_type = Building.objects.get(riot_name=event_data['buildingType'])

                    event = PlayerMatchBuildingKill.objects.create(playermatch=killer, timestamp=event_data['timestamp'], building_type=building_type)
                    event.save()
                    for assist_id in event_data['assistingParticipantIds']:
                        assist = PlayerMatchBuildingAssist.objects.create(kill=event, playermatch=participants[assist_id - 1])
                        assist.save()
            elif event_data['type'] == 'ELITE_MONSTER_KILL':
                if event_data['killerId'] > 0:
                    playermatch = participants[event_data['killerId'] - 1]
                    if 'monsterSubType' in event_data:
                        monster_type = EliteMonster.objects.get(riot_name=event_data['monsterType'], riot_subname=event_data['monsterSubType'])
                    else: 
                        monster_type = EliteMonster.objects.get(riot_name=event_data['monsterType'])

                    event = PlayerMatchEliteMonsterKill.objects.create(playermatch=playermatch, timestamp=event_data['timestamp'], monster_type=monster_type)
                    event.save()

def update_playermatchkills():
    matches = Match.objects.filter(series__week__season__id=4)

    for match in matches:
        playermatchkills = PlayerMatchKill.objects.filter(killer__match=match)
        count = 0
        for playermatchkill in playermatchkills:
            if playermatchkill.position_x == 0:
                count += 1
#        if count > 0:
#            a = 5/0
#    for match in matches:
#
#            PlayerMatchTimeline.objects.filter(playermatch__match=match).delete()
#            PlayerMatchKill.objects.filter(killer__match=match).delete()
#            PlayerMatchAssist.objects.filter(playermatch__match=match).delete()
#            PlayerMatchWardPlace.objects.filter(playermatch__match=match).delete()
#            PlayerMatchWardKill.objects.filter(playermatch__match=match).delete()
#            PlayerMatchBuildingKill.objects.filter(playermatch__match=match).delete()
#            PlayerMatchBuildingAssist.objects.filter(playermatch__match=match).delete()
#            PlayerMatchEliteMonsterKill.objects.filter(playermatch__match=match).delete()
#        
#            get_match_timeline(match.id)

def update_season_timelines(season_id):
    season = Season.objects.get(id=season_id)
    for team in season.team_set.all():
        team_kill_timelines = team.generate_overall_timelines()

        for team_kill_timeline in team_kill_timelines:
            team_timeline = SeasonTimeline.objects.filter(season=season, minute=team_kill_timeline['minute'])
            if team_timeline:
                team_timeline = team_timeline[0]
            else:
                team_timeline = SeasonTimeline.objects.create(season=season, minute=team_kill_timeline['minute'])
            team_timeline.kills = team_kill_timeline['kills']
            team_timeline.building_kills = team_kill_timeline['building_kills']
            team_timeline.wards_placed = team_kill_timeline['wards_placed']
            team_timeline.wards_killed = team_kill_timeline['wards_killed']
            team_timeline.save()
   
def update_team_timelines(team_id):
    team = Team.objects.get(id=team_id)
    team_kill_timelines = team.generate_kill_timelines()
    enemy_kill_timelines = team.generate_killed_timelines()

    for team_kill_timeline, enemy_kill_timeline in zip(team_kill_timelines, enemy_kill_timelines):
        team_timeline = TeamTimeline.objects.filter(team=team, minute=team_kill_timeline['minute'])
        if team_timeline:
            team_timeline = team_timeline[0]
        else:
            team_timeline = TeamTimeline.objects.create(team=team, minute=team_kill_timeline['minute'])
        team_timeline.kills = team_kill_timeline['kills']
        team_timeline.building_kills = team_kill_timeline['building_kills']
        team_timeline.wards_placed = team_kill_timeline['wards_placed']
        team_timeline.wards_killed = team_kill_timeline['wards_killed']
        team_timeline.enemy_kills = enemy_kill_timeline['kills']
        team_timeline.enemy_building_kills = enemy_kill_timeline['building_kills']
        team_timeline.enemy_wards_placed = enemy_kill_timeline['wards_placed']
        team_timeline.enemy_wards_killed = enemy_kill_timeline['wards_killed']
        team_timeline.save()

def update_team_player_timelines(team_id, player_id, role_id):
    team_player = TeamPlayer.objects.get(team=team_id, player=player_id, role=role_id)
    team_player.csDiffAt15 = team_player.generate_cs_diff_at_15()
    team_player.csPerMin = team_player.generate_cs_per_min()
    team_player.killParticipation = team_player.generate_kill_participation()
    team_player.teamDamagePercent = team_player.generate_percent_team_damage()
    team_player.save()
#    vision_timelines = team_player.generate_vision_timeline()
#    gold_timelines = team_player.generate_gold_timeline()
#    for vision_timeline, gold_timeline in zip(vision_timelines, gold_timelines):
#        timeline = TeamPlayerTimeline.objects.filter(team=team_player.team, player=team_player.player, role=team_player.role, minute=gold_timeline['minute'])
#        if timeline:
#            timeline = timeline[0]
#        else:
#            timeline = TeamPlayerTimeline.objects.create(team=team_player.team, player=team_player.player, role=team_player.role, minute=gold_timeline['minute'])
#        timeline.gold = gold_timeline['avgGold']
#        timeline.enemy_gold = gold_timeline['avgOppGold']
#        timeline.gold_diff = gold_timeline['goldDiff']
#        timeline.wards_placed = vision_timeline['wards_placed']
#        timeline.wards_killed = vision_timeline['wards_killed']
#        timeline.save()

def get_match(match_id):
    try:
        match = Match.objects.get(id=match_id)
    except:
        raise ObjectNotFound("Match " + str(match_id))

    if match.riot_id == 0:
        match_id_requester = RiotRequester('/lol/match/v4/matches/by-tournament-code/')
        match.riot_id = match_id_requester.request(match.tournament_code + '/ids')[0]
        match.save()

    # find teams
    try:
        teammatch_1 = TeamMatch.objects.get(match=match_id, side="Blue")
        team_1 = Team.objects.get(id=teammatch_1.team.id)
    except Team.DoesNotExist:
        raise ObjectNotFound("Team 1")
    try:
        teammatch_2 = TeamMatch.objects.get(match=match_id, side="Red")
        team_2 = Team.objects.get(id=teammatch_2.team.id)
    except Team.DoesNotExist:
        raise ObjectNotFound("Team 2")

    try:
	series = Series.objects.filter(id=match.series.id)
    except Series.DoesNotExist:
	raise ObjectNotFound("Series")

    series.youtube_link = " "
    requester = RiotRequester('/lol/match/v4/matches/')
    try:
        match_data = requester.request(str(match.riot_id))
    except RiotNotFound:
        raise ObjectNotFound("Match " + str(match.riot_id))

    for team_data in match_data['teams']:
        if team_data['teamId'] == 100:
            team = team_1
            side = "Blue"
        if team_data['teamId'] == 200:
            team = team_2
            side = "Red"
        try:
            team_match = TeamMatch.objects.get(match=match, team=team)
        except TeamMatch.DoesNotExist:
            team_match = TeamMatch.objects.create(match=match, team=team)
	for ban_data in team_data['bans']:
            team_ban = TeamMatchBan.objects.create(team=team, match=match, champion=get_champion(ban_data['championId']), pickTurn=ban_data['pickTurn'])
	    team_ban.save()
        team_match.side = side
        team_match.match = match
        team_match.first_dragon = team_data['firstDragon']
        team_match.first_inhibitor = team_data['firstInhibitor']
        team_match.baron_kills = team_data['baronKills']
        team_match.first_rift_herald = team_data['firstRiftHerald']
        team_match.first_blood = team_data['firstBlood']
        team_match.first_tower = team_data['firstTower']
        team_match.inhibitor_kills = team_data['inhibitorKills']
        team_match.tower_kills = team_data['towerKills']
        if team_data['win'] == "Win":
            team_match.win = True
        team_match.dragon_kills = team_data['dragonKills']
        team_match.save()

    i = 0
    roles = Role.objects.all()
    for participant_data in match_data['participants']:
        participant_stats = participant_data['stats']
        role = Role.objects.get(id = ((participant_stats['participantId']-1) % 5)+1)
        if math.floor((participant_data['participantId']-1)/5)+1 == 1:
            team = team_1
        else:
            team = team_2
        series_player = SeriesPlayer.objects.filter(series=match.series, role=role, team=team)[0]
        champion = get_champion(participant_data['championId'])
        try:
            player_match = PlayerMatch.objects.get(player=series_player.player, team=series_player.team, match=match)
            player_match.champion=champion
        except PlayerMatch.DoesNotExist:
            player_match = PlayerMatch.objects.create(player=series_player.player, team=series_player.team, match=match, champion=champion)
        player_match.participant_id=participant_data['participantId']
        player_match.role = roles[i % 5]
        i=i+1
        player_match.kills = participant_stats['kills']
        player_match.deaths = participant_stats['deaths']
        player_match.assists = participant_stats['assists']
        player_match.assists = participant_stats['assists']
        player_match.physical_damage_dealt = participant_stats['physicalDamageDealt']
        player_match.neutral_minions_killed_team_jungle = participant_stats['neutralMinionsKilledTeamJungle']
        player_match.magic_damage_dealt = participant_stats['magicDamageDealt']
        player_match.total_player_score = participant_stats['totalPlayerScore']
        player_match.neutral_minions_killed_enemy_jungle = participant_stats['neutralMinionsKilledEnemyJungle']
        player_match.largest_critical_strike = participant_stats['largestCriticalStrike']
        player_match.total_damage_dealt = participant_stats['totalDamageDealt']
        player_match.magic_damage_dealt_to_champions = participant_stats['magicDamageDealtToChampions']
        player_match.vision_wards_bought_in_game = participant_stats['visionWardsBoughtInGame']
        player_match.damage_dealt_to_objectives = participant_stats['damageDealtToObjectives']
        player_match.largest_killing_spree = participant_stats['largestKillingSpree']
        player_match.double_kills = participant_stats['doubleKills']
        player_match.triple_kills = participant_stats['tripleKills']
        player_match.quadra_kills = participant_stats['quadraKills']
        player_match.penta_kills = participant_stats['pentaKills']
        player_match.total_time_crowd_control_dealt = participant_stats['totalTimeCrowdControlDealt']
        player_match.longest_time_spent_living = participant_stats['longestTimeSpentLiving']
        player_match.wards_killed = participant_stats['wardsKilled']
        player_match.first_tower_assist = participant_stats['firstTowerAssist']
        player_match.first_tower_kill = participant_stats['firstTowerKill']
        player_match.first_blood_assist = participant_stats['firstBloodAssist']
        player_match.vision_score = participant_stats['visionScore']
        player_match.wards_placed = participant_stats['wardsPlaced']
        player_match.turret_kills = participant_stats['turretKills']
        player_match.damage_self_mitigated = participant_stats['damageSelfMitigated']
        player_match.champ_level = participant_stats['champLevel']
        player_match.first_inhibitor_kill = participant_stats['firstInhibitorKill']
        player_match.gold_earned = participant_stats['goldEarned']
        player_match.magical_damage_taken = participant_stats['magicalDamageTaken']
        player_match.true_damage_taken = participant_stats['trueDamageTaken']
        player_match.first_inhibitor_assist = participant_stats['firstInhibitorAssist']
        player_match.neutral_minions_killed = participant_stats['neutralMinionsKilled']
        player_match.objective_player_score = participant_stats['objectivePlayerScore']
        player_match.combat_player_score = participant_stats['combatPlayerScore']
        player_match.damage_dealt_to_turrets = participant_stats['damageDealtToTurrets']
        player_match.physical_damage_dealt_to_champions = participant_stats['physicalDamageDealtToChampions']
        player_match.gold_spent = participant_stats['goldSpent']
        player_match.true_damage_dealt = participant_stats['trueDamageDealt']
        player_match.true_damage_dealt_to_champions = participant_stats['trueDamageDealtToChampions']
        player_match.total_heal = participant_stats['totalHeal']
        player_match.total_minions_killed = participant_stats['totalMinionsKilled']
        player_match.first_blood_kill = participant_stats['firstBloodKill']
        player_match.sight_wards_bought_in_game = participant_stats['sightWardsBoughtInGame']
        player_match.total_damage_dealt_to_champions = participant_stats['totalDamageDealtToChampions']
        player_match.inhibitor_kills = participant_stats['inhibitorKills']
        player_match.total_score_rank = participant_stats['totalScoreRank']
        player_match.total_damage_taken = participant_stats['totalDamageTaken']
        player_match.killing_sprees = participant_stats['killingSprees']
        player_match.time_ccing_others = participant_stats['timeCCingOthers']
        player_match.physical_damage_taken = participant_stats['physicalDamageTaken']
        player_match.save()


    match.duration = match_data['gameDuration']
    match.save()
    get_match_timeline(match_id)

    update_team_timelines(team_1.id)
    update_team_timelines(team_2.id)

    update_season_timelines(team_1.season.id)

    players_1 = TeamPlayer.objects.filter(team=team_1)
    for player in players_1:
        update_team_player_timelines(player.team.id, player.player.id, player.role.id)
   
    players_2 = TeamPlayer.objects.filter(team=team_2)
    for player in players_2:
        update_team_player_timelines(player.team.id, player.player.id, player.role.id)

    update_playermatchkills()
    return match

