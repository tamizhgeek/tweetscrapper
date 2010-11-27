# Create your views here.


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404 
#from django.core.context_processors import csrf                                                                            
from google.appengine.ext import db
from django.core.urlresolvers import reverse
from google.appengine.api import urlfetch
from django.template import RequestContext
from scrapper.models import *
from django.contrib.auth.decorators import login_required
from google.appengine.api import users
import os
import oauth, oauth_details
from django.utils import simplejson as json


def login_required(func):
    def _wrapperfunc(request, *args, **kwargs):
        
        user = users.get_current_user()
        if user:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
    return _wrapperfunc

def index(request):
    cur_user = users.get_current_user()
    if cur_user:
        reg_users = db.GqlQuery("select * from Users where user = :1", cur_user)
        if reg_users.count() == 0:
            
            if request.method == 'POST':
                form = UserEntryForm(request.POST)
                if form.is_valid():
                    new_entry = form.save()
                    new_entry.user = cur_user
                    new_entry.put()
                    return render_to_response("sucess.html",{'user':new_entry, }, context_instance=RequestContext(request))
            else:
                form = UserEntryForm()
                return render_to_response("register.html", {
                        'form': form,
                        }, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/authenticate')
    else:
        return HttpResponseRedirect(users.create_login_url(reverse('scrapper.views.index')))

    
@login_required
def authenticate(request):
    
    query = Users.all()
    u = users.get_current_user()
    cur_user = query.filter('user =', u).fetch(1)[0]
    if cur_user.oauth_token is not None:
        
        return HttpResponseRedirect('/home')
    
    else:

        client = oauth.TwitterClient(oauth_details.consumer_key, oauth_details.consumer_secret, oauth_details.callback)
        return HttpResponseRedirect(client.get_authorization_url())
    

def save_twitter_auth(request):
    
    client = oauth.TwitterClient(oauth_details.consumer_key, oauth_details.consumer_secret, oauth_details.callback)

    auth_token = request.REQUEST['oauth_token']
    auth_verifier = request.REQUEST['oauth_verifier']
    user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
    
    query = Users.all()
    cur_user = query.filter('user =',  users.get_current_user()).fetch(1)[0]
    cur_user.oauth_token = user_info.get('token')
    cur_user.oauth_secret = user_info.get('secret')
    cur_user.realname = user_info.get('name')
    cur_user.put()
    return HttpResponseRedirect('/authenticate')

@login_required
def home(request):
    cur_user = get_user_info()
    client = oauth.TwitterClient(oauth_details.consumer_key, oauth_details.consumer_secret, oauth_details.callback)
    additional_params = {
        'count': 199,
        'screen_name':'azhaguselvan',
        }
    result = client.make_request(
        "http://api.twitter.com/1/statuses/user_timeline.json",
        token = cur_user.oauth_token,
        secret = cur_user.oauth_secret,
        additional_params = additional_params,
        method = urlfetch.GET)
    details = json.loads(result.content)[0]['user']
    return render_to_response("home.html", {'info': details, }, context_instance = RequestContext(request))

    
def thenticate(request):
    query = Users.all()
    cur_user = query.filter('user =',  users.get_current_user()).fetch(1)[0]
    client = oauth.TwitterClient(oauth_details.consumer_key, oauth_details.consumer_secret, oauth_details.callback)
    additional_params = {
        'status': "Testing Twitter OAuth with Django and AppEngine",
        }

    result = client.make_request(
        "http://twitter.com/statuses/update.json",
        token=cur_user.oauth_token,
        secret=cur_user.oauth_secret,
        additional_params=additional_params,
        method=urlfetch.POST)


def get_user_info():
    query = Users.all()
    u = users.get_current_user()
    cur_user = query.filter('user =', u).fetch(1)[0]
    return cur_user

def logout(request):
    
    return HttpResponseRedirect(users.create_logout_url(reverse('scrapper.views.index')))
