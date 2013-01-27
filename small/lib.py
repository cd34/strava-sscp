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
        'redis_expiration_time': 60*60*1,
        'distributed_lock':True
        }
)

"""
   add a second region with a 32 day cache for the rides to cut down on
   API hits for clubs. Rides generally don't disappear, though, this only
   reports for the current month, so, should never exceed 31 days.
"""
dbmregion = make_region().configure(
    'dogpile.cache.dbm',
    expiration_time = 60*60*24*32,
    arguments = {
        "filename":"/var/www/sscp/small/data/cachefile.dbm"
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
        return None

@region.cache_on_arguments(expiration_time=3600)
def get_clubs(name):
    return get_strava('/clubs', {'name':name}, 'clubs')

@region.cache_on_arguments(expiration_time=3600)
def get_members(id):
    return get_strava('/clubs/%s/members' % id, None, 'members')

@region.cache_on_arguments(expiration_time=3600)
def get_rides(id, date_start, date_end):
    return get_strava('/rides', {'athleteID':id, 'startDate':date_start, \
        'endDate':date_end} , 'rides')

@region.cache_on_arguments(expiration_time=2764800)
def get_ride(id):
    return get_strava('/rides/%s' % id, None, 'ride')
