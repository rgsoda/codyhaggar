from django.conf.urls.defaults import *

urlpatterns = patterns('cody.views',
        url(r'^$', 'index', name="index"),
        url(r'^add$', 'challenge', name="add-challenge"),
        url(r'^edit/(?P<challenge_id>\d+)$', 'challenge', name="edit-challenge"),
        url(r'^solve/(?P<challenge_id>\d+)$', 'solve', name="solve-challenge"),
        url(r'^challenge/(?P<challenge_id>\d+)$', 'display_challenge', \
            name="display-challenge"),
        url(r'^lurk/(?P<challenge_id>\d+)$', 'lurk', name="lurk-challenge"),
)
