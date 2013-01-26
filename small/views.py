import calendar
import datetime

from pyramid.response import Response
from pyramid.view import view_config

from small.lib import (get_clubs,
                       get_members,
                       get_ride,
                       get_rides,
                       region)


@view_config(route_name='home', renderer='index.mako')
def home(request):
    return {}

@view_config(route_name='json', renderer='json')
def json(request):
    curdate = datetime.date.today()
    (date_start, date_end) = calendar.monthrange(curdate.year, curdate.month)
    date_start = datetime.date(curdate.year, curdate.month, date_start). \
        isoformat()
    date_end = datetime.date(curdate.year, curdate.month, date_end). \
        isoformat()
 
    member_data = []

    for member in get_members(request.matchdict['id']):
        elevation = rides = avg_elevation = distance = commute = trainer = \
            total_distance = wattage = 0

        for ride in get_rides(member['id'], date_start, date_end):
            ride_stats = get_ride(ride['id'])
            rides += 1
            elevation += ride_stats['elevationGain']
            total_distance += ride_stats['distance']
            if ride_stats['commute']:
                commute += ride_stats['distance']
            elif ride_stats['trainer']:
                trainer += ride_stats['distance']
            else:
                distance += ride_stats['distance']
            if ride_stats['averageWatts']:
                wattage += ride_stats['averageWatts']

        if rides > 0:
            avg_elevation = elevation / rides
            wattage = wattage / rides

        member_data.append({'id':member['id'], 'name':member['name'], \
            'elevation':elevation, 'rides':rides, \
            'avg_elevation':avg_elevation, 'total_distance':total_distance, \
            'ride':distance, 'commute':commute, 'trainer':trainer, \
            'wattage':wattage })

    return {'member_data':member_data}

@view_config(route_name='clubname', renderer='json', request_method='POST')
def clubname(request):
    return {'data':get_clubs(request.POST['clubname'])}
