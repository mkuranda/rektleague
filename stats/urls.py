from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^email-signup/$', views.email_signup, name='email_signup'),
    url(r'^signin/$', views.loginpage, name='loginpage'),
    url(r'^schedule/$', views.latest_schedule, name='latest_schedule'),
    url(r'^standings/$', views.latest_standings, name='latest_standings'),
    url(r'^players/$', views.latest_season_players, name='latest_season_players'),
    url(r'^season/(?P<season_id>[0-9]+)/schedule/$', views.schedule, name='schedule'),
    url(r'^season/(?P<season_id>[0-9]+)/standings/$', views.standings, name='standings'),
    url(r'^season/(?P<season_id>[0-9]+)/players/$', views.season_players, name='season_players'),
    url(r'^season/(?P<season_id>[0-9]+)/team/(?P<team_id>[0-9]+)/$', views.team_detail, name='team_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/team/(?P<team_id>[0-9]+)/player/(?P<player_id>[0-9]+)/$', views.team_player_detail, name='team_player_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/team/(?P<team_id>[0-9]+)/player/(?P<player_id>[0-9]+)/role/(?P<role_id>[0-9]+)/$', views.team_player_role_detail, name='team_player_role_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/$', views.series_detail, name='series_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/lockin/(?P<team_id>[0-9]+)/$', views.series_lockin_detail, name='series_lockin_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/load/(?P<game_num>[0-9]+)/$', views.load_match, name='load_match'),
    #url(r'^profile/$', views.profile, name='profile'),

    #url(r'^season/(?P<season_id>[0-9]+)/$', views.season_detail, name='season'),
    #url(r'^season/(?P<season_id>[0-9]+)/questions$', views.questions, name='questions'),
    #url(r'^season/(?P<season_id>[0-9]+)/teams/$', views.season_teams_detail, name='season_teams'),
    #url(r'^season/(?P<season_id>[0-9]+)/champions/$', views.season_champions_detail, name='season_champions'),
    #url(r'^season/(?P<season_id>[0-9]+)/graphs/$', views.season_graphs_empty_detail, name='season_graphs_empty'),
    #url(r'^season/(?P<season_id>[0-9]+)/graphs/(?P<graph_type>[a-z_]+)/(?P<selected_player_id_str>[0-9_]+)/$', views.season_graphs_detail, name='season_graphs'),
    #url(r'^player/(?P<player_id>[0-9]+)/$', views.player_detail, name='player_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/team/(?P<team_id>[0-9]+)/recache_stats/$', views.team_recache, name='team_recache'),
    #url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/$', views.series_detail, name='series_detail'),
    #url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/caster_tools/$', views.series_caster_tools, name='series_caster_tools'),
    #url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/create_roster/(?P<team_id>[0-9]+)/$', views.create_roster, name='create_roster'),
    #url(r'^season/(?P<season_id>[0-9]+)/match/(?P<match_id>[0-9]+)/load_match/$', views.load_match, name='load_match'),
    #url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/load_match/results/(?P<team_1_id>[0-9]+)/(?P<team_2_id>[0-9]+)/(?P<match_id>[0-9]+)/$', views.match_data_results, name='match_data_results'),
    #url(r'^create_code/(?P<match_id>[0-9]+)/$', views.create_code, name='create_code'),
    url(r'^champion/(?P<champion_id>[0-9]+)/$', views.champion_detail, name='champion_detail'),
    url(r'^caster_tools/player_matchup/(?P<blue_player_id>[0-9]+)/(?P<red_player_id>[0-9]+)/team/(?P<blue_team_id>[0-9]+)/(?P<red_team_id>[0-9]+)/role/(?P<role_id>[0-9]+)/$', views.player_matchup, name='player_matchup'),
    url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/head_to_head/$', views.series_head_to_head, name='series_head_to_head'),
    url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/head_to_head_2/$', views.series_head_to_head_2, name='series_head_to_head_2'),
    url(r'^match_complete/$', views.match_complete, name='match_complete'),
    url(r'^propagate_teams/$', views.propagate_teams, name='propagate_teams')
]
