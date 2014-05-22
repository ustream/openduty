#What is this?
**Openduty** is an incident escalation tool, just like [Pagerduty](http://pagerduty.com) . It has a Pagerduty compatible API too. It's the result of the first [Ustream Hackathon](http://www.ustream.tv/blog/2014/03/27/hackathon-recap-21-ideas-11-teams-one-goal/). We enjoyed working on it.
#Integrations
Has been tested with Nagios, works well for us. Any Pagerduty Notifier using the Pagerduty API should work without a problem.
#Notifications
XMPP, email, SMS, Phone(Thanks Twilio for being awesome!), and Push notifications(thanks Pushover also) are supported at the moment.
#Current status
Openduty is in Beta status, it can be considered stable at the moment, however major structural changes can appear anytime (not affecting the API, or the Notifier structure)

#Contribution guidelines
Yes, please. You are welcome.
#Feedback
Any feedback is welcome

#Contributors at Ustream
- [deathowl](http://github.com/deathowl)
- [oker](http://github.com/oker1)
- [tyrael](http://github.com/tyrael)
- [dzsubek](https://github.com/dzsubek)
- [ecsy](https://github.com/ecsy)
- [akos](https://github.com/gyim)

![The team](http://deathowlsnest.com/images/cod.jpg)

# Getting started:
```
sudo easy_install pip
sudo pip install virtualenv
virtualenv env
. env/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=openduty.settings_dev
python manage.py syncdb
python manage.py runserver
```
now, you can start hacking on it.


# Default login:
root/toor

# Celery worker:
```celery -A openduty worker -l info```