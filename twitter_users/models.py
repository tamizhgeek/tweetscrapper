import oauth2 as oauth
from django.db import models
from django.contrib.auth.models import User
from twitter_users import settings
from django.utils import simplejson as json

class TwitterInfo(models.Model):
    user = models.OneToOneField(User)
    name    = models.CharField(max_length=15)
    id      = models.BigIntegerField(primary_key=True)
    token   = models.CharField(max_length=100)
    secret  = models.CharField(max_length=100)

    def initialise_oauth_client(self):
        consumer = oauth.Consumer(settings.KEY, settings.SECRET)
        token = oauth.Token(self.token, self.secret)
        client = oauth.Client(consumer, token)
        return client

    def get_tweets(self, client, since_id = 0):
        if since_id == 0:
            resp, res = client.request(
                "http://api.twitter.com/1/statuses/user_timeline.json?count=10&include_rts=1")
        else:
            resp, res = client.request(
                "http://api.twitter.com/1/statuses/user_timeline.json?count=11&include_rts=1&max_id=%d"%since_id)

        if json.loads(resp['status']) == 200: #If the API gets down or something weird happens at network side
            res = json.loads(res)
            if since_id != 0:
                res.pop(0)  # Removing the first element, as it would be a repitition

        result = self.accumulate_tweets(res)
        return result

    def accumulate_tweets(self, input):
        result = []

        for entry in input:
            result.append({ 'text' : unicode(entry['text']), 'tweet_id' : entry['id']})
        return result
