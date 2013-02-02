from urllib import quote_plus
from dogpile.cache import make_region
import requests

BASE_API = 'http://www.strava.com/api/v1'

region = make_region().configure(
    'dogpile.cache.redis',
    arguments = {
        'host': 'localhost',
        'port': 6379,
        'db': 1,
        'redis_expiration_time': 60*60*24,
        'distributed_lock':True
        }
)

"""
   add a second region with a 32 day cache for the rides to cut down on
   API hits for clubs. Rides generally don't disappear, though, this only
   reports for the current month, so, should never exceed 31 days.
   moved dogpile lockfiles to tmpfs, anydbm is slloooooooooow handling
   locks.
"""
dbmregion = make_region().configure(
    'dogpile.cache.dbm',
    expiration_time = 60*60*24*32,
    arguments = {
        "filename":"/var/www/sscp/small/data/cachefile.dbm",
        "rw_lockfile":"/var/lib/dogpile/cachefile.dbm.rw.lock",
        "dogpile_lockfile":"/var/lib/dogpile/cachefile.dbm.dogpile.lock"
    }
)

"""
little heavy on the caching as this really hammers the API server
"""

def get_strava(uri, args, key):
    r = requests.get(BASE_API + uri, params=args)
    try:
        return r.json()[key]
    except:
        return []

@region.cache_on_arguments(expiration_time=3600)
def get_clubs(name):
    return get_strava('/clubs', {'name':name}, 'clubs')

@region.cache_on_arguments(expiration_time=28800)
def get_club(id):
    return get_strava('/clubs/%s' % id, None, 'club')

@region.cache_on_arguments(expiration_time=3600)
def get_members(id):
    return get_strava('/clubs/%s/members' % id, None, 'members')

@region.cache_on_arguments(expiration_time=3600)
def get_rides(id, date_start, date_end):
    return get_strava('/rides', {'athleteId':id, 'startDate':date_start, \
        'endDate':date_end} , 'rides')

@dbmregion.cache_on_arguments(expiration_time=2764800)
def get_ride(id):
    return get_strava('/rides/%s' % id, None, 'ride')

def get_member_data(id, date_start, date_end):
    member_data = []

    for member in get_members(id):
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

    return member_data
            
