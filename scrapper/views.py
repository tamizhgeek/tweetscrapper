from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from tweetscrapper.twitter_users.models import TwitterInfo 
from twitter_users import settings
import oauth2 as oauth
from django.utils import simplejson as json
#from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import cStringIO  
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    else:
        return render_to_response("home.html", context_instance=RequestContext(request))

@login_required
def index(request):
    tf = TwitterInfo.objects.get(user = request.user)	
    consumer = oauth.Consumer(settings.KEY, settings.SECRET)
    client = oauth.Client(consumer)
    status, resp = client.request('http://api.twitter.com/1/users/show.json?user_id='+str(tf.id))
    details = json.loads(resp)
    return render_to_response("index.html", {'info': details, }, context_instance = RequestContext(request))
    

def scrap(request):
    
    tf = TwitterInfo.objects.get(user = request.user)	
    consumer = oauth.Consumer(settings.KEY, settings.SECRET)
    token = oauth.Token(tf.token, tf.secret)
    client = oauth.Client(consumer, token)
    resp, result = client.request(
        "http://api.twitter.com/1/statuses/user_timeline.json?count=200",
        body = 'count=200')
    if json.loads(resp['status']) != 200:
        exit()
    else:
        result = json.loads(result)
        tweets = []
        for entry in result:
        
            tweets.append(unicode(entry['text']))
                          
        request.session['tweets'] = tweets
        return render_to_response("scrap.html", {'tweets': tweets, }, context_instance = RequestContext(request))
    
def getpdf(request):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf'%request.user.username

    buf = cStringIO.StringIO()
    doc = SimpleDocTemplate(buf,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    styles=getSampleStyleSheet()
    
    text = ""
    Story = []
    tweets = request.session['tweets']
    for tw in tweets:
        Story.append(Paragraph(unicode(tw), styles['Normal']))
    doc.build(Story)
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response
