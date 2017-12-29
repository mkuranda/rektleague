from django import forms
from .models import Team, Series, SeriesTeam

class TournamentCodeForm(forms.Form):
    series_id = 3

    def __init__(self, *args, **kwargs):
	self.series_id = kwargs.pop('series_id')
	super(TournamentCodeForm, self).__init__(*args, **kwargs)
	
    series_teams = SeriesTeam.objects.filter(series=series_id)
    team_1 = forms.ModelChoiceField(queryset=Team.objects.filter(seriesteam__series=series_id))
    team_2 = forms.ModelChoiceField(queryset=Team.objects.filter(seriesteam__series=series_id))
    tournament_code = forms.CharField(label='Tournament Code', max_length=50)
