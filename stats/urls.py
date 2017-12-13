from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^season/(?P<season_id>[0-9]+)/$', views.season_detail, name='season'),
    url(r'^player/(?P<player_id>[0-9]+)/$', views.player_detail, name='player_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/team/(?P<team_id>[0-9]+)/$', views.team_detail, name='team_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/load_match/$', views.load_match, name='load_match'),
    url(r'^season/(?P<season_id>[0-9]+)/load_match/results/(?P<match_id>[0-9]+)/$', views.match_data_results, name='match_data_results')
]
