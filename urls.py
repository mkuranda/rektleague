from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^stats/', include('stats.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
