from django import forms
from django.db.models import Q
from .models import Team, Series, SeriesTeam, Player, TeamPlayer, Role

class CreateRosterForm(forms.Form):

    top = forms.ModelChoiceField(queryset=Team.objects.none())
    jun = forms.ModelChoiceField(queryset=Team.objects.none())
    mid = forms.ModelChoiceField(queryset=Team.objects.none())
    bot = forms.ModelChoiceField(queryset=Team.objects.none())
    sup = forms.ModelChoiceField(queryset=Team.objects.none())
    sub = forms.ModelChoiceField(queryset=Team.objects.none())

    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id')
        series_id = kwargs.pop('series_id')
	super(CreateRosterForm, self).__init__(*args, **kwargs)
        top_role = Role.objects.get(name="Top")
        jun_role = Role.objects.get(name="Jungle")
        mid_role = Role.objects.get(name="Mid")
        bot_role = Role.objects.get(name="Bot")
        sup_role = Role.objects.get(name="Support")
        sub_role = Role.objects.get(name="Substitute")
        self.fields["top"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=top_role)
        self.fields["jun"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=jun_role)
        self.fields["mid"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=mid_role)
        self.fields["bot"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=bot_role)
        self.fields["sup"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=sup_role)
        self.fields["sub"].queryset = Player.objects.filter(teamplayer__team=team_id, teamplayer__role=sub_role)


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
