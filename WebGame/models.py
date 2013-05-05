from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    adminApproved = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=False)

    def __unicode__(self):
        return self.name


class Player(models.Model):
    playerID = models.CharField(max_length=15, null=False)
    user = models.OneToOneField(User)
    isModerator = models.BooleanField(default=False)
    adminApproved = models.BooleanField(default=False)
    team = models.ForeignKey(Team)

    def __unicode__(self):
        return '%s: %s' % (self.playerID, self.user.username)


class Content(models.Model):
    name = models.CharField(max_length=50, null=False)
    photo = models.URLField(null=True)
    description = models.TextField(null=False)
    latitude = models.TextField(null=False)
    longitude = models.TextField(null=False)
    upVotes = models.PositiveIntegerField(default=0, null=False)
    downVotes = models.PositiveIntegerField(default=0, null=False)
    upVotePlayers = models.ManyToManyField(Player, related_name='upVotePlayer')
    downVotePlayers = models.ManyToManyField(Player, related_name='downVotePlayer')
    verified = models.BooleanField(default=False)
    creationTime = models.DateTimeField(null=False)
    player = models.ForeignKey(Player, null=False)

    def __unicode__(self):
        return self.name

    def getContentHTML(self):
        htmlString = '<table class=\\\\"contentCard\\\\" style=\\\\"width: 300px;\\\\">'
        htmlString += '<tr class=\\\\"contentCard\\\\">'
        htmlString += '<th class=\\\\"contentCard\\\\">%s</th>' % self.name
        htmlString += '</tr>'
        if self.photo:
            htmlString += '<tr class=\\\\"contentCard\\\\">'
            htmlString += '<td class=\\\\"contentCard\\\\"><img width=\\\\"295px\\\\" height=\\\\"150px\\\\" src=\\\\"%s\\\\" /></td>' % self.photo
            htmlString += '</tr>'
        htmlString += '<tr class=\\\\"contentCard\\\\">'
        htmlString += '<td class=\\\\"contentCard\\\\">%s</td>' % self.description.replace('"', '\\\\"').replace("'", "\\'")
        htmlString += '</tr>'
        htmlString += '</table>'
        return htmlString

    def upVote(self, currentPlayer):
        self.upVotes += 1
        if currentPlayer:
            self.upVotePlayers.add(currentPlayer)
        self.save()

    def downVote(self, currentPlayer):
        self.downVotes += 1
        if currentPlayer:
            self.downVotePlayers.add(currentPlayer)
        self.save()

    def undoVote(self, currentPlayer):
        if currentPlayer in self.upVotePlayers.all():
            self.upVotePlayers.remove(currentPlayer)
            self.upVotes -= 1
        elif currentPlayer in self.downVotePlayers.all():
            self.downVotePlayers.remove(currentPlayer)
            self.downVotes -= 1
        self.save()