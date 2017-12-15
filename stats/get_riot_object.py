from riot_request import *
from .models import Item, Champion, Match, Team, TeamMatch, Role, TeamPlayer, PlayerMatch

class ObjectNotFound(Exception) :
    """Raised when we can't find an object in db or from riot API"""
    pass

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
        item.description = item_data["description"]
        item.save()
    return item

def get_champion(riot_id):
    try:
        champion = Champion.objects.get(id=riot_id)
    except Champion.DoesNotExist:
        requester = RiotRequester('/lol/static-data/v3/champions/')
        try:
            champion_data = requester.request(str(riot_id))
        except RiotNotFound:
            raise ObjectNotFound("Champion " + str(riot_id))
        champion = Champion.objects.create(id=riot_id)
        champion.name = champion_data["name"]
        champion.title = champion_data["title"]
        champion.save()
    return champion

def get_match(team_1_id, team_2_id, riot_id):
    try:
        match = Match.objects.get(id=riot_id)
    except Match.DoesNotExist:
        requester = RiotRequester('/lol/match/v3/matches/')
        try:
            match_data = requester.request(str(riot_id))
        except RiotNotFound:
            raise ObjectNotFound("Match " + str(riot_id))

        # find teams
        try:
            team_1 = Team.objects.get(id=team_1_id)
        except Team.DoesNotExist:
            raise ObjectNotFound("Team " + str(team_1_id))
        try:
            team_2 = Team.objects.get(id=team_2_id)
        except Team.DoesNotExist:
            raise ObjectNotFound("Team " + str(team_2_id))

        match = Match.objects.create(id=riot_id)
        for team_data in match_data['teams']:
            if team_data['teamId'] == 100:
                team = team_1
                side = "Blue"
            if team_data['teamId'] == 200:
                team = team_2
                side = "Red"
            team_match = TeamMatch.objects.create(match=match, team=team)
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

        for participant_data in match_data['participants']:
            participant_stats = participant_data['stats']
            role = Role.objects.get(id = ((participant_stats['participantId']-1) % 5)+1)
            team = Team.objects.get(id = int(participant_data['participantId']/5)+1)
            team_player = TeamPlayer.objects.get(role=role, team=team)
            champion = get_champion(participant_data['championId'])
            try:
                player_match = PlayerMatch.objects.get(player=team_player.player, match=match)
                player_match.champion=champion
            except PlayerMatch.DoesNotExist:
                player_match = PlayerMatch.objects.create(player=team_player.player, match=match, champion=champion)
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

        match.save()
    return match

