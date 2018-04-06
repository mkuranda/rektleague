from riot_request import *
import urllib, shutil
import math
from .models import Item, Champion, Match, Team, TeamMatch, Role, TeamPlayer, PlayerMatch, Week, Series, SeriesTeam, TeamMatchBan

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
            r = requests.get("http://ddragon.leagueoflegends.com/cdn/7.5.2/img/item/" + ss_data["image"]["full"], stream=True)
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
            r = requests.get("http://ddragon.leagueoflegends.com/cdn/7.5.2/img/item/" + item_data["image"]["full"], stream=True)
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
	r = requests.get("http://ddragon.leagueoflegends.com/cdn/8.6.1/img/item/" + item_data["image"]["full"], stream=True)
        if r.status_code == 200:
            with open("media/stats/item/icon" + item_data["image"]["full"], 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
	else:
	    raise ObjectNotFound("Item Image " + item_data["image"]["full"])
        item.description = item_data["description"]
        item.save()
    return item

def get_champion(riot_id):
    champion_exists = True
    try:
        champion = Champion.objects.get(id=riot_id)
    except Champion.DoesNotExist:
        champion_exists = False

    if champion_exists == False or champion.name == "" or champion.title == "" or champion.icon == "":
        requester = RiotRequester('/lol/static-data/v3/champions/')
	requester.add_tag("image")
        try:
            champion_data = requester.request(str(riot_id))
        except RiotNotFound:
            raise ObjectNotFound("Champion " + str(riot_id))
        if champion_exists == False:
            champion = Champion.objects.create(id=riot_id)
        champion.name = champion_data["name"]
        champion.title = champion_data["title"]
	r = requests.get("http://ddragon.leagueoflegends.com/cdn/8.6.1/img/champion/" + champion_data["image"]["full"], stream=True)
        if r.status_code == 200:
            with open("media/stats/champion/icon/" + champion_data["image"]["full"], 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
	else:
	    raise ObjectNotFound("Champion Image " + champion_data["image"]["full"])
#	urllib.urlretrieve(, "media/stats/" + champion_data["image"]["full"])
	champion.icon = "stats/champion/icon/" + champion_data["image"]["full"]
        champion.save()
    return champion

def get_match(match_id):
    try:
        match = Match.objects.get(id=match_id)
    except:
        raise ObjectNotFound("Match " + str(match_id))

    if match.riot_id == 0:
        match_id_requester = RiotRequester('/lol/match/v3/matches/by-tournament-code/')
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

    requester = RiotRequester('/lol/match/v3/matches/')
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

    for participant_data in match_data['participants']:
        participant_stats = participant_data['stats']
        role = Role.objects.get(id = ((participant_stats['participantId']-1) % 5)+1)
        if math.floor((participant_data['participantId']-1)/5)+1 == 1:
            team = team_1
        else:
            team = team_2
        team_player = TeamPlayer.objects.filter(role=role, team=team)[0]
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

    match.duration = 1
    match.save()
    return match

