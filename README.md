#What is this?
**Openduty** is an incident escalation tool, just like [Pagerduty](http://pagerduty.com) . It has a Pagerduty compatible API too. It's the result of the first [Ustream Hackathon](http://www.ustream.tv/blog/2014/03/27/hackathon-recap-21-ideas-11-teams-one-goal/). We enjoyed working on it.
#Integrations
Has been tested with Nagios, works well for us. Any Pagerduty Notifier using the Pagerduty API should work without a problem.
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
- [deathowl](http://github.com/deathowl)
- [oker](http://github.com/oker1)
- [tyrael](http://github.com/tyrael)
- [dzsubek](https://github.com/dzsubek)
- [ecsy](https://github.com/ecsy)
- [akos](https://github.com/gyim)

![The team](http://deathowlsnest.com/images/cod.jpg)
#Other contributors
- [DazWorrall](https://github.com/DazWorrall)
- [leventyalcin](https://github.com/leventyalcin)
- [sheran-g](https://github.com/sheran-g)

# Getting started:
```
sudo easy_install pip
sudo pip install virtualenv
virtualenv env
. env/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=openduty.settings_dev
python manage.py syncdb
python manage.py migrate
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