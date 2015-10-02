"""points URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from pointset.views import IndexView, CreatePointSetView, LeaderBoardView, HistoryView


urlpatterns = [

    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="logout"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^history$', HistoryView.as_view(), name="history"),
    url(r'^leaderboard/$', LeaderBoardView.as_view(), name="leaderboard"),
    url(r'^give-points/$', CreatePointSetView.as_view(), name="give-points"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
]
