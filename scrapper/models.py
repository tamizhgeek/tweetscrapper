from appengine_django.models import BaseModel
from google.appengine.ext import db
import google.appengine.ext.db.djangoforms as djangoforms

# Create your models here.
 
    

class Users(BaseModel):
    user = db.UserProperty()
    twitter_handle = db.StringProperty()
    oauth_token = db.TextProperty()
    oauth_secret = db.TextProperty()
    realname = db.StringProperty()

class Tweet(BaseModel):
    
    author = db.ReferenceProperty(Users)
    permalink = db.LinkProperty()
    created_at = db.DateTimeProperty()

class UserEntryForm(djangoforms.ModelForm):
    
    class Meta:
        model = Users
        exclude = ('user', 'oauth_token', 'oauth_secret', 'realname')


    
    
