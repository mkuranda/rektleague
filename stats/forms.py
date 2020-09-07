from django import forms
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Team, Series, SeriesTeam, Player, TeamPlayer, Role, Summoner, User, UserAccount

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    email = forms.EmailField()
    mainAccount = forms.CharField(label='Main Riot Account Name', max_length=50)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "mainAccount"]

        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            return user

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password1

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        account = UserAccount.objects.create(user=user, name=self.cleaned_data['mainAccount'], isMain=True)
        account.save()
        return user

class AddAccountForm(forms.Form):
    account_name = forms.CharField(max_length=50, required=False)

    def clean_account_name(self):
        account_name = self.cleaned_data['account_name']
        accountsWithSameName = UserAccount.objects.filter(name__iexact=account_name)
        if accountsWithSameName:
            raise forms.ValidationError("Sorry, someone already has an account with that name")
        return account_name

class EditAccountForm(forms.Form):
    account_id = forms.IntegerField()
    account_name = forms.CharField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.fields['account_name'].error_messages.update({
            'required': 'Sorry, we don\'t accept empty account names'
            })

    def clean_account_name(self):
        account_name = self.cleaned_data['account_name']
        accountsWithSameName = UserAccount.objects.filter(name__iexact=account_name)
        if accountsWithSameName:
            raise forms.ValidationError("Sorry, someone already has an account with that name")
        return account_name

class RemoveAccountForm(forms.Form):
    account_id = forms.IntegerField(required=False)

class SetMainForm(forms.Form):
    account_id = forms.IntegerField(required=False)

class UpdateUsernameForm(forms.Form):
    username = forms.CharField(label='Username', min_length=4, max_length=150, required=False)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        #password2 = self.cleaned_data.get('password2')

        #if password1 and not password2:
        #    raise ValidationError("You need to enter both passwords")
        #if password2 and not password1:
        #    raise ValidationError("You need to enter both passwords")

        #if password1 and password2 and password1 != password2:
        #    raise ValidationError("Password don't match")

        return password1

class UpdateEmailForm(forms.Form):
    email = forms.EmailField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if email and r.count():
            raise ValidationError("Email already exists")
        return email

class SeasonSignupForm(forms.Form):
    ROLES = ((1, "TOP"), (2, "JUNGLE"), (3, "MID"), (4, "BOT"), (5, "SUPPORT"))
    ROSTER_CHOICES = ((1, "MAIN ROSTER"), (2, "SUBSTITUTE"))

    mainRole = forms.ChoiceField(choices=ROLES, widget=forms.RadioSelect)
    offRoles = forms.MultipleChoiceField(choices=ROLES, widget=forms.CheckboxSelectMultiple, required=False)
    rosterPosition = forms.MultipleChoiceField(choices=ROSTER_CHOICES, widget=forms.CheckboxSelectMultiple)

    def clean_offRoles(self):
        main_role = self.cleaned_data['mainRole']
        off_roles = self.cleaned_data['offRoles']
        for role in off_roles:
            if role == main_role:
                raise forms.ValidationError("You can't choose a role as both your main role and off role")
        return off_roles

class ConfirmEloForm(forms.Form):
    elo = forms.IntegerField()
    seasonPlayerId = forms.IntegerField()

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

class EditProfileForm(forms.Form):

    new_summoner = forms.CharField(max_length=255)

    def __init__(self, user, *args, **kwargs):
	super(EditProfileForm, self).__init__(*args, **kwargs)
        player = Player.objects.get(user=user)
        self.fields['name'] = forms.CharField(max_length=255, initial=player.name)
        summoners = Summoner.objects.filter(player=player)
        i = 1
        for summoner in summoners:
            self.fields["summoner" + str(i)] = forms.CharField(max_length=255, initial=summoner.name)
            i = i + 1


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
