from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from tweetscrapper.twitter_users.models import TwitterInfo 
from twitter_users import settings
import oauth2 as oauth

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    else:
        return HttpResponse("Sign in with twitter - <a href='/twitter/login'>Login</a>")

@login_required
def index(request):
    tf = TwitterInfo.objects.get(user = request.user)	
    consumer = oauth.Consumer(settings.KEY, settings.SECRET)
    client = oauth.Client(consumer)
    
    return HttpResponse("Welcome to tweetscrapper. Hi "+tf.name+"<img src=http://api.twitter.com/1/users/profile_image/"+tf.name+".json>")

