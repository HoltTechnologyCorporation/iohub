import json
from datetime import datetime, timedelta
from pprint import pprint
import json
import yaml

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied

from project.database import db

with open('var/config.yml') as inp:
    config = yaml.load(inp, Loader=yaml.SafeLoader)


def home_page(request):
    ts = datetime.utcnow() - timedelta(minutes=30)
    query = {
        'date': {'$gte': ts}
    }
    sessions = db.session.find(query, sort=[('date', -1)])
    return render(request, 'board/home_page.html', {
        'sessions': sessions,
    })


@csrf_exempt
def api_ping(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.headers.get('access_token') not in config['access_tokens']:
        raise PermissionDenied
    db.ping.insert_one({
        'date': datetime.utcnow(),
        'data': data,
    })
    db.session.update_one(
        {'session_id': data['session_id']},
        {'$set': {
            'date': datetime.utcnow(),
            'data': data,
        }},
        upsert=True,
    )
    return HttpResponse('OK')


def session_page(request, session_id):
    query = {'session_id': session_id}
    session = db.session.find_one({'session_id': session_id})
    if not session:
        raise Http404
    data = session['data']
    handlers = sorted(data.pop('handlers'), key=lambda x: x['start_time'])
    stat = sorted(data.pop('stat').items(), key=lambda x: x[0])
    return render(request, 'board/session_page.html', {
        'session': session,
        'session_data': json.dumps(data, indent=2, ensure_ascii=False),
        'session_handlers': handlers,
        'stat': stat,
    })
