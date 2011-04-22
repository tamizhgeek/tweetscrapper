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

    buf = cStringIO.StringIO()
    doc = SimpleDocTemplate(buf,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    styles=getSampleStyleSheet()
    from reportlab.pdfbase import pdfmetrics,ttfonts
    import os
    #pdfmetrics.findFontAndRegister(ttfonts.TTFont('LinLibertine_Bd', "/home/tamizhgeek/virtualenvs/tweetscrapper/lib/python2.6/site-packages/reportlab-2.5-py2.6-linux-i686.egg/reportlab/fonts/LinLibertine_Bd.ttf"))
    pdfmetrics.registerFont(ttfonts.TTFont('TAM', os.path.join(os.path.dirname('..'), 'TSCu_Paranar.ttf'))) 
    styles.add(ParagraphStyle(name='TestStyle',fontName='TAM',
                              fontSize=12,
                              leading=12)) 
    text = ""
    Story = []
    tweets = request.session['tweets']
    for tw in tweets:
        Story.append(Paragraph(tw, styles['TestStyle']))
    doc.build(Story)
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response

