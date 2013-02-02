import calendar
import datetime

from pyramid.response import Response
from pyramid.view import view_config

from small.lib import (get_member_data,
                       get_club,
                       get_clubs,
                       get_members,
                       get_ride,
                       get_rides,
                       region)


@view_config(route_name='home', renderer='index.mako')
def home(request):
    return {}

@view_config(route_name='json', renderer='json')
@view_config(route_name='json_lastmonth', renderer='json')
def json(request):
    curdate = datetime.date.today()
    if request.matched_route.name == 'json_lastmonth':
        curdate = datetime.date(curdate.year, curdate.month, 1) - \
          datetime.timedelta(1)
    (date_start_weekday, date_end) = calendar.monthrange( \
        curdate.year, curdate.month)
    date_start = datetime.date(curdate.year, curdate.month, 1). \
        isoformat()
    date_end = datetime.date(curdate.year, curdate.month, date_end). \
        isoformat()
 
    return {'member_data':get_member_data(request.matchdict['id'], \
            date_start, date_end), \
            'club_data':get_club(request.matchdict['id'])}

@view_config(route_name='clubname', renderer='json', request_method='POST')
def clubname(request):
    return {'data':get_clubs(request.POST['clubname'])}
