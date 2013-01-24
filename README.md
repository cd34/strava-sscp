small README
==================

Project
-------

While reading the Strava API documentation, I came across this code challenge
that was similar to something I intended to write. This is written using
AngularJS, D3 and Pyramid, a Python framework.

https://stravasite-main.pbworks.com/w/page/51754156/Strava%20Small%20Coding%20Project

Site can be viewed at http://clubride.cd34.com/

Unable to create an account in pbworks to see how to contact Derek, so, I'm 
posting this through a trouble ticket.

Installation Documentation
---------------

    virtualenv /var/www/sscp
    cd /var/www/sscp
    source bin/activate
    git clone https://github.com/cd34/strava-sscp.git small
    cd /var/www/sscp/small
    python setup.py develop
    pserve --reload development.ini

    Browse to http://127.0.0.1:8080

Notes
-----

Due to the number of hits against the API, I used dogpile.cache to cache
the ride data in a redis backend which is the only storage that is used.
Since you have to walk the club to walk the members to walk their rides
by date, a busy club will generate hundreds of requests. The second pageload
will be pulled from the cache. After an hour, the club and riders will be 
fetched, but, the actual ride data is cached for 24 hours.
