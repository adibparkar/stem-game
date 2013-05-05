from django.conf.urls import patterns, include, url
from WebGame.views import loginPage, startPage, createPlayer, createTeam, logoutUser, mapPage
from WebGame.views import deleteTeam, uploadPage, upVoteContent, downVoteContent, undoVoteContent, verifyContent, deleteContent
from WebGame.views import viewTeamApprovalList, viewModeratorApprovalList, approveTeam, approveModerator, rejectModerator
from WebGame.views import seedContent, getJSONForMap, leaderboard

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', loginPage),
    (r'^welcome/$', startPage),
    (r'^signup/$', createPlayer),
    (r'^createTeam/$', createTeam),
    (r'^map/', mapPage),
    (r'^upVoteContent/', upVoteContent),
    (r'^downVoteContent/', downVoteContent),
    (r'^undoVoteContent/', undoVoteContent),
    (r'^verifyContent/', verifyContent),
    (r'^deleteContent/', deleteContent),
    (r'^uploadContent/', uploadPage),
    (r'^approveTeamList/', viewTeamApprovalList),
    (r'^approveModeratorList/', viewModeratorApprovalList),
    (r'^approveTeam/', approveTeam),
    (r'^deleteTeam/', deleteTeam),
    (r'^approveModerator/', approveModerator),
    (r'^rejectModerator/', rejectModerator),
    (r'^seedContent/', seedContent),
    (r'^jsonMap/$', getJSONForMap),
    (r'^leaderboard/$', leaderboard),
    (r'^logout/$', logoutUser),
    # Examples:
    # url(r'^$', 'StemGame.views.home', name='home'),
    # url(r'^StemGame/', include('StemGame.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
