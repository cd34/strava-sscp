#!/var/www/sscp python

import os
import site

site.addsitedir('/var/www/sscp/lib/python2.7/site-packages')
from pyramid.paster import get_app
application = get_app(
    '/var/www/sscp/small/production.ini', 'main')
