from django import forms

class TournamentCodeForm(forms.Form):
    tournament_code = forms.CharField(label='Tournament Code', max_length=50)
