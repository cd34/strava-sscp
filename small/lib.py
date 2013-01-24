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
little heavy on the caching as this really hammers the API server
"""

def get_strava(uri, key):
    r = requests.get(BASE_API + uri)
    try:
        return r.json()[key]
    except:
        return None

@region.cache_on_arguments(expiration_time=3600)
def get_clubs(name):
    return get_strava('/clubs?name=%s' % name, 'clubs')

@region.cache_on_arguments(expiration_time=3600)
def get_members(id):
    return get_strava('/clubs/%s/members' % id, 'members')

@region.cache_on_arguments(expiration_time=3600)
def get_rides(id, date_start, date_end):
    return get_strava('/rides?athleteId=%s&startDate=%s&endDate=%s' % \
        (id, date_start, date_end) , 'rides')

@region.cache_on_arguments(expiration_time=86400)
def get_ride(id):
    return get_strava('/rides/%s' % id, 'ride')
