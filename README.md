#Build status

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ustream/openduty)
[![image](https://api.travis-ci.org/ustream/openduty.svg)](https://travis-ci.org/ustream/openduty)
[![Requirements Status](https://requires.io/github/openduty/openduty/requirements.svg?branch=master)](https://requires.io/github/openduty/openduty/requirements/?branch=master)
#What is this?
**Openduty** is an incident escalation tool, just like [Pagerduty](http://pagerduty.com) . It has a Pagerduty compatible API too. It's the result of the first [Ustream Hackathon](http://www.ustream.tv/blog/2014/03/27/hackathon-recap-21-ideas-11-teams-one-goal/). We enjoyed working on it.
#Integrations
Has been tested with Nagios, works well for us. Any Pagerduty Notifier using the Pagerduty API should work without a problem.
[Icinga2 config](https://github.com/deathowl/OpenDuty-Icinga2) for openduty integration

#Notifications
XMPP, email, SMS, Phone(Thanks Twilio for being awesome!), and Push notifications(thanks Pushover also),and Slack are supported at the moment.
#Current status
Openduty is in Beta status, it can be considered stable at the moment, however major structural changes can appear anytime (not affecting the API, or the Notifier structure)

#Contribution guidelines
Yes, please. You are welcome.
#Feedback
Any feedback is welcome

#Try it
go to http://openduty.herokuapp.com , log in with root/toor , create your own user.
In heroku demo mode user edit feature is disabled, so you can't misbehave.

#Running on Heroku
add the parts below to your settings.py and add psycopg2==2.5.1 to your requirements.txt

```
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```

#Contributors at Ustream
- [oker](http://github.com/oker1)
- [tyrael](http://github.com/tyrael)
- [dzsubek](https://github.com/dzsubek)
- [ecsy](https://github.com/ecsy)
- [akos](https://github.com/gyim)

![The team](http://deathowlsnest.com/images/cod.jpg)
#Main contributors
- [deathowl](http://github.com/deathowl) 

#Other contributors
- [DazWorrall](https://github.com/DazWorrall)
- [leventyalcin](https://github.com/leventyalcin)
- [sheran-g](https://github.com/sheran-g)

# Getting started:
```
sudo easy_install pip
sudo pip install virtualenv
virtualenv env --python python2.7
. env/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=openduty.settings_dev
python manage.py syncdb
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
now, you can start hacking on it.

# After models you've changed your models please run:
```
./manage.py schemamigration openduty --auto
./manage.py schemamigration notification --auto
./manage.py migrate

```

#If you see a new file appearing in migrations directory when pulling from upstream please run
```
./manage.py migrate
```

# Default login:
root/toor

# Celery worker:
```
celery -A openduty worker -l info
```

# Login using basic authentication with LDAP-backend

Add the following snippet to your settings_prod/dev.py, dont forget about import

```
AUTH_LDAP_SERVER_URI = "ldap://fqdn:389"
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_START_TLS = False
AUTH_LDAP_MIRROR_GROUPS = True #Mirror LDAP Groups as Django Groups, and populate them as well.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Group,dc=domain,dc=com",
    ldap.SCOPE_SUBTREE, "(&(objectClass=posixGroup)(cn=openduty*))"
)
AUTH_LDAP_GROUP_TYPE = PosixGroupType()

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People,dc=domain,dc=com",
ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
"first_name": "uid",
"last_name": "sn",
"email": "mail"
}


AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
  'openduty.middleware.basicauthmiddleware.BasicAuthMiddleware',
)

```
