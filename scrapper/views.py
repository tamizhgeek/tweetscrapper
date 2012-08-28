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
from time import sleep
from django.template.loader import render_to_string
#import ho.pisa as pisa


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    else:
        return render_to_response("home.html", context_instance=RequestContext(request))

def about(request):
    return render_to_response("about.html", context_instance=RequestContext(request))

@login_required
def index(request):
    tf = TwitterInfo.objects.get(user = request.user)	
    consumer = oauth.Consumer(settings.KEY, settings.SECRET)
    client = oauth.Client(consumer)
    status, resp = client.request('http://api.twitter.com/1/users/show.json?user_id='+str(tf.id))
    if status['status'] != '200':
        success = False
    else:
        success = True
    details = json.loads(resp)
    return render_to_response("index.html", {'info': details, 'result' : success}, context_instance = RequestContext(request))
    
@login_required
def scrap(request, show_all = None):
    if request.session.has_key('tweets'):
        return render_to_response("scrap.html", {'tweets' : request.session['tweets'], }, context_instance = RequestContext(request))
    else:
        return render_to_response("scrap.html", context_instance = RequestContext(request))
    
@login_required    
def getpdf(request):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf'%request.user.username
    
    html = render_to_string('tweetlist.html', {'tweets': request.session['tweets']})
    
    buf = cStringIO.StringIO()
    
    pdf = pisa.pisaDocument(cStringIO.StringIO(
        html.encode("utf-8")), buf)
    #if not pdf.err:
     #   return HttpResponse(buf.getvalue(), \
      #                               mimetype='application/pdf')
    pdf = buf.getvalue() 

    buf.close()
    response.write(pdf)
    return response

