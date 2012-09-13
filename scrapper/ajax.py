from django.utils import simplejson
from dajaxice.core import dajaxice_functions
from scrapper.views import *


def scrap_ajax(request, show_all = None):
    print 1
    tf = TwitterInfo.objects.get(user = request.user)	
    client = tf.initialise_oauth_client()
    request.session['tweets'] = []
    # Delete the previosly set session values, if they still exist
    if request.session.get('since_id', False):
        del request.session['total_count']
    request.session['since_id'] = 0
    try:
        resp, res = get_tweets(request, client)
    except Exception as e:
        sleep(5) #Sometimes twitter becomes a 'bad monster' after repeated requests. A gap of 5 seconds will make it cool again.
        return HttpResponse("Something wrong happened with the twitter API.<a href='/scrap'> Try Now </a>")
    accumulate_tweets(request, res)
    show_all = request.GET.get('show_all', None) # This loop should go on only when there is a show_all tweets request
    while len(request.session['tweets']) < request.session['total_count']-1: 
        # This loop should execute until the collected tweets becomes equal for total count
        try:
            resp, res = get_tweets(request, client)
        except:
            sleep(5)
            continue #Same as above, a small gap to cool down twitter
        accumulate_tweets(request, res)
    
    return simplejson.dumps({'tweets':request.session['tweets']})
    

def get_tweets(request, client):

    since_id = request.session['since_id']
    if since_id == 0:
        resp, res = client.request(
            "http://api.twitter.com/1/statuses/user_timeline.json?count=3200&include_rts=1")
    else:
        resp, res = client.request(
            "http://api.twitter.com/1/statuses/user_timeline.json?count=3200&include_rts=1&max_id=%d"%since_id)
    try:
        result = json.loads(res)
    except: #This JSON error happens at random. So this try block. Should find the root cause and fix this.
        return HttpResponse("Something wrong happened with the application. <a href='/'>Try again</a>")
    
    if json.loads(resp['status']) != 200: #If the API gets down or something weird happens at network side
        return HttpResponse("Something wrong happened with the twitter API. Try after some time")
    
    if not (request.session.get('total_count', False)): #If no total count is already set, do it now.
    
        request.session['total_count'] = result[0]['user']['statuses_count'] #The twitter will give only 3200 tweets at any point of time. So if a user has more tweets than that. Set total count to 3200.
        
        request.session['total_count'] = request.session['total_count'] if  request.session['total_count'] < 3200 else 3200
    request.session['since_id'] = result[-1]['id']
    return resp, result

def accumulate_tweets(request, result):
    
    for entry in result:
        request.session['tweets'].append(unicode(entry['text']))
    print len(request.session['tweets'])



dajaxice_functions.register(scrap_ajax)
