from django import forms
from django.db.models import Q
from .models import Team, Series, SeriesTeam, Player, TeamPlayer, Role

class CreateRosterForm(forms.Form):

    top = forms.ModelChoiceField(queryset=Team.objects.none())
    jun = forms.ModelChoiceField(queryset=Team.objects.none())
    mid = forms.ModelChoiceField(queryset=Team.objects.none())
    bot = forms.ModelChoiceField(queryset=Team.objects.none())
    sup = forms.ModelChoiceField(queryset=Team.objects.none())
    sub = forms.ModelChoiceField(queryset=Team.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id')
        series_id = kwargs.pop('series_id')
	super(CreateRosterForm, self).__init__(*args, **kwargs)
        top_role = Role.objects.get(name="TOP")
        jun_role = Role.objects.get(name="JUNGLE")
        mid_role = Role.objects.get(name="MID")
        bot_role = Role.objects.get(name="BOT")
        sup_role = Role.objects.get(name="SUPPORT")
        sub_role = Role.objects.get(name="SUBSTITUTE")
        self.fields["top"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=top_role)
        self.fields["jun"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=jun_role)
        self.fields["mid"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=mid_role)
        self.fields["bot"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=bot_role)
        self.fields["sup"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=sup_role)
        self.fields["sub"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=sub_role)


class CasterLineupForm(forms.Form):
    blue_top = forms.ModelChoiceField(queryset=Team.objects.none())
    blue_jun = forms.ModelChoiceField(queryset=Team.objects.none())
    blue_mid = forms.ModelChoiceField(queryset=Team.objects.none())
    blue_bot = forms.ModelChoiceField(queryset=Team.objects.none())
    blue_sup = forms.ModelChoiceField(queryset=Team.objects.none())

    red_top = forms.ModelChoiceField(queryset=Team.objects.none())
    red_jun = forms.ModelChoiceField(queryset=Team.objects.none())
    red_mid = forms.ModelChoiceField(queryset=Team.objects.none())
    red_bot = forms.ModelChoiceField(queryset=Team.objects.none())
    red_sup = forms.ModelChoiceField(queryset=Team.objects.none())

    def __init__(self, *args, **kwargs):
        series_id = kwargs.pop('series_id')
	super(CasterLineupForm, self).__init__(*args, **kwargs)
        top_role = Role.objects.get(name="TOP")
        jun_role = Role.objects.get(name="JUNGLE")
        mid_role = Role.objects.get(name="MID")
        bot_role = Role.objects.get(name="BOT")
        sup_role = Role.objects.get(name="SUPPORT")

        blue_team = SeriesCastTeam.objects.get(series=series_id, side='Blue')
        red_team = SeriesCastTeam.objects.get(series=series_id, side='Red')

        self.fields["blue_top"].queryset = Player.objects.filter(teamplayer__team=blue_team.team, teamplayer__role=top_role)
        self.fields["blue_jun"].queryset = Player.objects.filter(teamplayer__team=blue_team.team, teamplayer__role=jun_role)
        self.fields["blue_mid"].queryset = Player.objects.filter(teamplayer__team=blue_team.team, teamplayer__role=mid_role)
        self.fields["blue_bot"].queryset = Player.objects.filter(teamplayer__team=blue_team.team, teamplayer__role=bot_role)
        self.fields["blue_sup"].queryset = Player.objects.filter(teamplayer__team=blue_team.team, teamplayer__role=sup_role)

        self.fields["red_top"].queryset = Player.objects.filter(teamplayer__team=red_team.team, teamplayer__role=top_role)
        self.fields["red_jun"].queryset = Player.objects.filter(teamplayer__team=red_team.team, teamplayer__role=jun_role)
        self.fields["red_mid"].queryset = Player.objects.filter(teamplayer__team=red_team.team, teamplayer__role=mid_role)
        self.fields["red_bot"].queryset = Player.objects.filter(teamplayer__team=red_team.team, teamplayer__role=bot_role)
        self.fields["red_sup"].queryset = Player.objects.filter(teamplayer__team=red_team.team, teamplayer__role=sup_role)



class TournamentCodeForm(forms.Form):

    team_1 = forms.ModelChoiceField(queryset=Team.objects.none())
    team_2 = forms.ModelChoiceField(queryset=Team.objects.none())
    tournament_code = forms.CharField(label='Tournament Code', max_length=50)

    def __init__(self, *args, **kwargs):
	series_id = kwargs.pop('series_id')
	super(TournamentCodeForm, self).__init__(*args, **kwargs)
        self.fields["team_1"].queryset = Team.objects.filter(seriesteam__series=series_id)
        self.fields["team_2"].queryset = Team.objects.filter(seriesteam__series=series_id)


class InitializeMatchForm(forms.Form):

    blue_team = forms.ModelChoiceField(queryset=Team.objects.none())
    red_team = forms.ModelChoiceField(queryset=Team.objects.none())
    casters = forms.ModelMultipleChoiceField(queryset=Player.objects.none())

    def __init__(self, *args, **kwargs):
	series_id = kwargs.pop('series_id')
	super(InitializeMatchForm, self).__init__(*args, **kwargs)
        self.fields["blue_team"].queryset = Team.objects.filter(seriesteam__series=series_id)
        self.fields["red_team"].queryset = Team.objects.filter(seriesteam__series=series_id)
        players = Player.objects.all()
        for team in Team.objects.filter(seriesteam__series=series_id):
            players = players.exclude(Q(teamplayer__team=team))
        self.fields["casters"].queryset = players
