from django import forms
from .models import Team

class TournamentCodeForm(forms.Form):
    team_1 = forms.ModelChoiceField(queryset=Team.objects.all())
    team_2 = forms.ModelChoiceField(queryset=Team.objects.all())
    tournament_code = forms.CharField(label='Tournament Code', max_length=50)
