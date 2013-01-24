import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'requests',
    'dogpile.cache',
    'redis',
    ]

setup(name='small',
      version='0.9',
      description='Strava Small Code Challenge',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: MIT License",
        ],
      author='Chris Davies',
      author_email='strava@daviesinc.com',
      url='http://clubride.cd34.com/',
      keywords='',
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='small',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = small:main
      [console_scripts]
      initialize_small_db = small.scripts.initializedb:main
      """,
      )
