# Create your views here.

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from models import Team, Player, Content
from django.utils.timezone import utc
from datetime import datetime
import os.path
import seed

epsilon = 1e-6
startLatitude = 34.01841
startLongitude = -118.29130
endLatitude = 34.02540
endLongitude = -118.28022

# startLatitude = 34.01105
# startLongitude = -118.30010
# endLatitude = 34.03463
# endLongitude = -118.27201


def loginPage(request):
    if request.method == 'POST':
        data = dict()
        data['username'] = request.POST.get('username', None)
        data['password'] = request.POST.get('password', None)
        if data['username'] and data['password']:
            user = authenticate(username=data['username'], password=data['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/map/?mode=player')
        return render_to_response('login.html', RequestContext(request, {'errorText': 'Invalid username or password.'}))
    return render_to_response('login.html', RequestContext(request, {}))


def getUserData(request):
    data = dict()
    data['loggedIn'] = True
    data['playerName'] = request.user.username
    data['isAdmin'] = request.user.is_superuser
    data['player'] = None
    data['isPlayer'] = False
    data['isModerator'] = False
    player = Player.objects.filter(user=request.user)
    if player and player.count() == 1:
        data['player'] = player[0]
        data['isPlayer'] = True
        data['isModerator'] = (data['player'].isModerator and data['player'].adminApproved)
    return data


def startPage(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        return render_to_response('startPage.html', RequestContext(request, data))
    return HttpResponseRedirect('/')


def createTeam(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        data['teams'] = Team.objects.all()
        if request.method == 'POST':
            data['errorText'] = None
            data['teamName'] = request.POST.get('teamName', None)
            if not data['teamName']:
                data['errorText'] = 'Please enter a team name.'
            elif Team.objects.filter(name=data['teamName']).count() > 0:
                data['errorText'] = 'That team already exists.'
            if data['errorText']:
                return render_to_response('createTeam.html', RequestContext(request, data))
            Team.objects.create(name=data['teamName'], owner=request.user)
            return HttpResponseRedirect('/createTeam/')
        return render_to_response('createTeam.html', RequestContext(request, data))
    return HttpResponseRedirect('/')


def viewTeamApprovalList(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        if data['isAdmin'] or data['isModerator']:
            data['teams'] = Team.objects.filter(adminApproved=False)
            return render_to_response('approve.html', RequestContext(request, data))
    return HttpResponseRedirect('/')


def viewModeratorApprovalList(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        data = dict()
        data['loggedIn'] = True
        data['playerName'] = request.user.username
        data['moderators'] = Player.objects.filter(adminApproved=False, isModerator=True)
        return render_to_response('approve.html', RequestContext(request, data))
    return HttpResponseRedirect('/')


def approveTeam(request):
    if request.user.is_authenticated():
        team = request.GET.get('team', None)
        if team:
            teamToApprove = Team.objects.get(pk=team)
            teamToApprove.adminApproved = True
            teamToApprove.save()
        return HttpResponseRedirect('/approveTeamList/')
    return HttpResponseRedirect('/')


def deleteTeam(request):
    if request.user.is_authenticated():
        team = request.GET.get('team', None)
        if team:
            teamToDelete = Team.objects.get(pk=team)
            playersToDelete = Player.objects.filter(team=teamToDelete)
            for player in playersToDelete:
                contentToDelete = Content.objects.filter(player=player)
                for content in contentToDelete:
                    content.delete()
                player.user.delete()
                player.delete()
            teamToDelete.delete()
        return HttpResponseRedirect('/approveTeamList/')
    return HttpResponseRedirect('/')


def approveModerator(request):
    if request.user.is_authenticated():
        moderator = request.GET.get('moderator', None)
        if moderator:
            moderatorToApprove = Player.objects.get(pk=moderator)
            moderatorToApprove.adminApproved = True
            moderatorToApprove.save()
        return HttpResponseRedirect('/approveModeratorList/')
    return HttpResponseRedirect('/')


def rejectModerator(request):
    if request.user.is_authenticated():
        moderator = request.GET.get('moderator', None)
        if moderator:
            moderatorToReject = Player.objects.get(pk=moderator)
            moderatorToReject.isModerator = False
            moderatorToReject.save()
        return HttpResponseRedirect('/approveModeratorList/')
    return HttpResponseRedirect('/')


def createPlayer(request):
    data = dict()
    data['editMode'] = request.GET.get('editMode', None)
    playerObject = None
    if data['editMode'] == 'true':
        data['editMode'] = True
    else:
        data['editMode'] = False
    if data['editMode']:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
        data['username'] = request.user.username
        data['firstName'] = request.user.first_name
        data['lastName'] = request.user.last_name
        playerObject = Player.objects.get(user=request.user)
        data['uscID'] = playerObject.playerID
        data['email'] = request.user.email
        data['teamName'] = playerObject.team.name
    data['teams'] = Team.objects.filter(adminApproved=True)
    if request.method == 'POST':
        data['errorTextUsername'] = None
        data['errorTextPassword'] = None
        data['errorTextPasswordVerify'] = None
        data['errorTextUscID'] = None
        data['errorTextFirstName'] = None
        data['errorTextLastName'] = None
        data['errorTextEmail'] = None
        data['errorTextTeamName'] = None
        data['username'] = request.POST.get('username', None)
        if not data['username']:
            data['errorTextUsername'] = 'Username required.'
        data['password'] = request.POST.get('password', None)
        data['passwordVerify'] = request.POST.get('passwordVerify', None)
        if not data['password']:
            data['errorTextPassword'] = 'Password required.'
        elif data['password'] != data['passwordVerify']:
            data['errorTextPasswordVerify'] = 'Passwords do not match'
        data['uscID'] = request.POST.get('uscID', None)
        if not data['uscID']:
            data['errorTextUscID'] = 'USC ID required.'
        data['firstName'] = request.POST.get('firstName', None)
        if not data['firstName']:
            data['errorTextFirstName'] = 'First name required.'
        data['lastName'] = request.POST.get('lastName', None)
        data['email'] = request.POST.get('email', None)
        posA = data['email'][::-1].find('@')
        posD = data['email'][::-1].find('.')
        if not data['email'] or posA == -1 or posD < 1 or posA < posD:
            data['errorTextEmail'] = 'Enter a valid email address.'
        if not data['lastName']:
            data['errorTextLastName'] = 'Last name required.'
        data['teamName'] = request.POST.get('teamName', None)
        if not data['teamName']:
            data['errorTextTeamName'] = 'Team name required.'
        if data['username'] and data['username'] != request.user.username:
            user = User.objects.filter(username=data['username'])
            if user.count() > 0:
                data['errorTextUsername'] = 'This username already exists.'
        if data['errorTextUsername'] or data['errorTextPassword'] or data['errorTextPasswordVerify'] or data['errorTextUscID'] or data['errorTextFirstName'] or data['errorTextLastName'] or data['errorTextEmail'] or data['errorTextTeamName']:
            return render_to_response('signup.html', RequestContext(request, data))
        data['isModerator'] = request.POST.get('isModerator', None)
        if data['isModerator'] == 'on':
            data['isModerator'] = True
        else:
            data['isModerator'] = False
        if not data['editMode']:
            user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
            user.first_name = data['firstName']
            user.last_name = data['lastName']
            user.save()
            team = Team.objects.get(name=data['teamName'])
            Player.objects.create(playerID=data['uscID'], user=user, team=team, isModerator=data['isModerator'])
        else:
            request.user.username = data['username']
            request.user.set_password(data['password'])
            request.user.email = data['email']
            request.user.first_name = data['firstName']
            request.user.last_name = data['lastName']
            request.user.save()
            if playerObject:
                team = Team.objects.get(name=data['teamName'])
                playerObject.playerID = data['uscID']
                playerObject.user = request.user
                playerObject.team = team
                playerObject.save()
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/map/?mode=player')
        return HttpResponseRedirect('/')
    return render_to_response('signup.html', RequestContext(request, data))


def logoutUser(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/')


def createJSONString(mode, player, isModerator, isAdmin):
    regionJSONString = '['
    if mode:
        points = Content.objects.all()
        for point in points:
            if not startLatitude < float(point.latitude) < endLatitude or not startLongitude < float(point.longitude) < endLongitude:
                continue
            votes = point.upVotes - point.downVotes
            currentOwner = False
            voted = False
            if player in point.upVotePlayers.all() or player in point.downVotePlayers.all():
                voted = True
            if player == point.player:
                currentOwner = True
            if votes > -50:
                if regionJSONString[-1] == '}':
                    regionJSONString += ', '
                dataString = '{"latitude": %s' % point.latitude
                dataString += ', "longitude": %s' % point.longitude
                dataString += ', "regionContentID": "%s"' % point.pk
                if mode == 'team':
                    dataString += ', "owner": "%s"' % point.player.team.name.replace('"', '\\\\"').replace("'", "\\'")
                else:
                    dataString += ', "owner": "%s"' % point.player.user.username.replace('"', '\\\\"').replace("'", "\\'")
                dataString += ', "content": "%s"' % point.getContentHTML()
                dataString += ', "isModerator": "%s"' % (isModerator or isAdmin)
                dataString += ', "isVerified": "%s"' % point.verified
                dataString += ', "voted": "%s"' % voted
                dataString += ', "currentOwner": "%s"' % currentOwner
                dataString += ', "votes": %d}' % votes
                regionJSONString += dataString
    regionJSONString += ']'
    return regionJSONString


def mapPage(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        data['mode'] = request.GET.get('mode', None)
        regionJSONString = createJSONString(data['mode'], data['player'], data['isModerator'], data['isAdmin'])
        data['jsonData'] = regionJSONString
        return render_to_response('map.html', RequestContext(request, data))
    return HttpResponseRedirect('/')


def uploadPage(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        if request.method == 'POST':
            creationTime = datetime.utcnow().replace(tzinfo=utc)
            data['latitude'] = request.POST.get('latitude', None)
            data['longitude'] = request.POST.get('longitude', None)
            data['contentName'] = request.POST.get('contentName', None)
            data['contentPhotoURL'] = request.POST.get('contentPhotoURL', None)
            if not data['contentPhotoURL'] and request.FILES:
                photoFile = request.FILES.get('contentPhoto', None)
                if photoFile:
                    rootDirectory = os.path.abspath(os.path.join(os.path.curdir, 'static/images')).replace('\\', '/')
                    if not os.path.exists(rootDirectory):
                        os.mkdir(rootDirectory)
                    creationTimeString = '%s' % creationTime
                    creationTimeString = creationTimeString.replace(':', '-').replace('.', '-')
                    fileName = '%s_%s-%s_%s' % (data['playerName'][:5], creationTimeString[:10], creationTimeString[11:22], photoFile)
                    filePath = '%s/%s' % (rootDirectory, fileName)
                    with open(filePath, 'wb+') as destination:
                        for chunk in photoFile.chunks():
                            destination.write(chunk)
                    data['contentPhotoURL'] = '/static/images/%s' % (fileName)
            data['contentDescription'] = request.POST.get('contentDescription', None)
            if data['latitude'] and data['longitude'] and data['contentName'] and data['contentDescription']:
                latitude = float(data['latitude'])
                longitude = float(data['longitude'])
                if startLatitude < latitude < endLatitude and startLongitude < longitude < endLongitude:
                    while Content.objects.filter(latitude=latitude, longitude=longitude).count() > 0:
                        latitude += epsilon
                    content = Content.objects.create(name=data['contentName'],
                                           photo=data['contentPhotoURL'],
                                           description=data['contentDescription'],
                                           latitude='%.6f' % latitude,
                                           longitude='%.6f' % longitude,
                                           creationTime=creationTime,
                                           player=data['player'])
                    content.upVote(data['player'])
                    return HttpResponseRedirect('/map/?mode=player')
            data['errorOccurred'] = True
        return render_to_response('uploadContent.html', RequestContext(request, data))
    return HttpResponseRedirect('/')


def upVoteContent(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        regionContentID = request.GET.get('regionContentID', None)
        mode = request.GET.get('mode', None)
        noAjax = request.GET.get('noAjax', None)
        if regionContentID:
            regionContent = Content.objects.get(pk=regionContentID)
            if regionContent:
                regionContent.upVote(data['player'])
        if mode:
            if noAjax:
                return HttpResponseRedirect('/map/?mode=' + mode)
            return HttpResponse(createJSONString(mode, data['player'], data['isModerator'], data['isAdmin']).replace('\\\\"', '\\"').replace('\\\'', '\''))
        else:
            return HttpResponse('Vote Registered')
    return HttpResponseRedirect('/')


def downVoteContent(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        regionContentID = request.GET.get('regionContentID', None)
        mode = request.GET.get('mode', None)
        noAjax = request.GET.get('noAjax', None)
        if regionContentID:
            regionContent = Content.objects.get(pk=regionContentID)
            if regionContent:
                regionContent.downVote(data['player'])
        if mode:
            if noAjax:
                return HttpResponseRedirect('/map/?mode=' + mode)
            return HttpResponse(createJSONString(mode, data['player'], data['isModerator'], data['isAdmin']).replace('\\\\"', '\\"').replace('\\\'', '\''))
        else:
            return HttpResponse('Vote Registered')
    return HttpResponseRedirect('/')


def undoVoteContent(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        regionContentID = request.GET.get('regionContentID', None)
        mode = request.GET.get('mode', None)
        noAjax = request.GET.get('noAjax', None)
        if regionContentID:
            regionContent = Content.objects.get(pk=regionContentID)
            if regionContent:
                regionContent.undoVote(data['player'])
        if mode:
            if noAjax:
                return HttpResponseRedirect('/map/?mode=' + mode)
            return HttpResponse(createJSONString(mode, data['player'], data['isModerator'], data['isAdmin']).replace('\\\\"', '\\"').replace('\\\'', '\''))
        else:
            return HttpResponse('Vote Registered')
    return HttpResponseRedirect('/')


def verifyContent(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        regionContentID = request.GET.get('regionContentID', None)
        mode = request.GET.get('mode', None)
        noAjax = request.GET.get('noAjax', None)
        if regionContentID:
            regionContent = Content.objects.get(pk=regionContentID)
            if regionContent and (data['isModerator'] or data['isAdmin']):
                regionContent.verified = True
                regionContent.save()
        if mode:
            if noAjax:
                return HttpResponseRedirect('/map/?mode=' + mode)
            return HttpResponse(createJSONString(mode, data['player'], data['isModerator'], data['isAdmin']).replace('\\\\"', '\\"').replace('\\\'', '\''))
        else:
            return HttpResponse('Content Verified')
    return HttpResponseRedirect('/')


def deleteContent(request):
    if request.user.is_authenticated():
        data = getUserData(request)
        regionContentID = request.GET.get('regionContentID', None)
        mode = request.GET.get('mode', None)
        noAjax = request.GET.get('noAjax', None)
        if regionContentID:
            regionContent = Content.objects.get(pk=regionContentID)
            if regionContent:
                regionContent.delete()
        if mode:
            if noAjax:
                return HttpResponseRedirect('/map/?mode=' + mode)
            return HttpResponse(createJSONString(mode, data['player'], data['isModerator'], data['isAdmin']).replace('\\\\"', '\\"').replace('\\\'', '\''))
        else:
            return HttpResponse('Content Deleted')
    return HttpResponseRedirect('/')


def getJSONForMap(request):
    if request.user.is_authenticated():
        noAjax = request.GET.get('noAjax', None)
        mode = request.GET.get('mode', None)
        if noAjax:
            HttpResponseRedirect('/map/?mode=' + mode)
        data = getUserData(request)
        data['mode'] = mode
        return HttpResponse(createJSONString(data['mode'], data['player'], data['isModerator'], data['isAdmin']).replace('\\\\"', '\\"').replace('\\\'', '\''))
    return HttpResponseRedirect('/')


def leaderboard(request):
    data = dict()
    data['jsonData'] = createJSONString('player', None, False, False)
    return render_to_response('leaderboard.html', RequestContext(request, data))


def seedContent(request):
    if request.user.is_authenticated():
        logout(request)
    seed.seed()
    return HttpResponseRedirect('/')