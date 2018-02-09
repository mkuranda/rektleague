from django import forms
from django.db.models import Q
from .models import Team, Series, SeriesTeam, Player

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
