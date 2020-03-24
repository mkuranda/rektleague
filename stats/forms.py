from django import forms
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import Team, Series, SeriesTeam, Player, TeamPlayer, Role

class CreateRosterForm(forms.Form):

    top = forms.ModelChoiceField(queryset=Team.objects.none())
    jun = forms.ModelChoiceField(queryset=Team.objects.none())
    mid = forms.ModelChoiceField(queryset=Team.objects.none())
    bot = forms.ModelChoiceField(queryset=Team.objects.none())
    sup = forms.ModelChoiceField(queryset=Team.objects.none())
    sub = forms.ModelChoiceField(queryset=Team.objects.none(), required=False)

    def clean(self):
        cleaned_data = super(CreateRosterForm, self).clean()
        s = set()
        top = cleaned_data.get('top')
        jun = cleaned_data.get('jun')
        mid = cleaned_data.get('mid')
        bot = cleaned_data.get('bot')
        sup = cleaned_data.get('sup')
        sub = cleaned_data.get('sub')

        failed = False
        s.add(top)
        if jun in s: 
            failed=True
        s.add(jun)
        if mid in s: 
            failed=True
        s.add(mid)
        if bot in s: 
            failed=True
        s.add(bot)
        if sup in s: 
            failed=True
        s.add(sup)
        if sub in s: 
            failed=True
        s.add(sub)

        if failed:
            raise forms.ValidationError("You can only assign a player to one role at a time")

        total_elo = cleaned_data.get('top').elo_value + cleaned_data.get('jun').elo_value + cleaned_data.get('mid').elo_value + cleaned_data.get('bot').elo_value + cleaned_data.get('sup').elo_value
        if total_elo > 0:
            raise forms.ValidationError("Submitted roster is above the elo limit at +" + str(total_elo))
 

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

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


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
