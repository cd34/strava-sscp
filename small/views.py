import calendar
import datetime
import re

from pyramid.view import view_config

from small.lib import (get_member_data,
                       get_club,
                       get_clubs)

date_regexp = re.compile('\d{4}-\d{2}-\d{2}')

@view_config(route_name='home', renderer='index.mako')
def home(request):
    return {}

@view_config(route_name='json', renderer='json')
@view_config(route_name='json_lastmonth', renderer='json')
def json(request):
    curdate = datetime.date.today()
    if request.matched_route.name == 'json_lastmonth':
        if request.matchdict['lastmonth'] == 'lastmonth':
            curdate = datetime.date(curdate.year, curdate.month, 1) - \
              datetime.timedelta(1)
    (date_start_weekday, date_end) = calendar.monthrange( \
        curdate.year, curdate.month)
    date_start = datetime.date(curdate.year, curdate.month, 1). \
        isoformat()
    date_end = datetime.date(curdate.year, curdate.month, date_end). \
        isoformat()
    if request.matched_route.name == 'json_lastmonth':
        if date_regexp.match(request.matchdict['lastmonth']):
            date_start = datetime.datetime.strptime( \
              request.matchdict['lastmonth'], '%Y-%m-%d').date()
            date_end = (date_start + datetime.timedelta(1)).isoformat()
            date_start = date_start.isoformat()
 
    return {'member_data':get_member_data(request.matchdict['id'], \
            date_start, date_end), \
            'club_data':get_club(request.matchdict['id'])}

@view_config(route_name='clubname', renderer='json', request_method='POST')
def clubname(request):
    return {'data':get_clubs(request.POST['clubname'])}
