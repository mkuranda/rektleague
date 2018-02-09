from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^news/', views.news, name='news'),
    url(r'^about/', views.about, name='about'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^get_items/', views.get_items, name='get_items'),
    url(r'^season/(?P<season_id>[0-9]+)/$', views.season_detail, name='season'),
    url(r'^player/(?P<player_id>[0-9]+)/$', views.player_detail, name='player_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/team/(?P<team_id>[0-9]+)/$', views.team_detail, name='team_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/$', views.series_detail, name='series_detail'),
    url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/load_match/$', views.load_match, name='load_match'),
    url(r'^season/(?P<season_id>[0-9]+)/series/(?P<series_id>[0-9]+)/load_match/results/(?P<team_1_id>[0-9]+)/(?P<team_2_id>[0-9]+)/(?P<match_id>[0-9]+)/$', views.match_data_results, name='match_data_results'),
    url(r'^champion/(?P<champion_id>[0-9]+)/$', views.champion_detail, name='champion_detail'),
    url(r'^create_code/(?P<match_id>[0-9]+)/$', views.create_code, name='create_code'),
]
