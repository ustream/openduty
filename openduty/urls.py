from django.conf import settings
from django.conf.urls import patterns, url, include
from rest_framework import routers as rest_routers
from openduty import views
from . import incidents, healthcheck, opsweekly
from django.contrib import admin
from schedule.periods import  Month, Week
from .models import Incident
from .tables import IncidentTable
from django_tables2_simplefilter import FilteredSingleTableView
from .incidents import ServicesByMe

admin.autodiscover()
rest_router = rest_routers.SimpleRouter(trailing_slash=False)
rest_router.register(r'users', views.UserViewSet)
rest_router.register(r'groups', views.GroupViewSet)
rest_router.register(r'schedule_policies', views.SchedulePolicyViewSet)
rest_router.register(r'schedule_policy_rules', views.SchedulePolicyRuleViewSet)
rest_router.register(r'create_event', incidents.IncidentViewSet)
rest_router.register(r'healthcheck', healthcheck.HealthCheckViewSet)
rest_router.register(r'celeryhealthcheck', healthcheck.CeleryHealthCheckViewSet)
rest_router.register(r'opsweekly', opsweekly.OpsWeeklyIncidentViewSet)
rest_router.register(r'oncall', opsweekly.OpsWeeklyOnCallViewSet)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^api/', include(rest_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^schedule/', include('schedule.urls')),

    #AUTH
    url(r'^login/$', 'openduty.auth.login'),
    url(r'^login/do$', 'openduty.auth.do'),
    url(r'^logout/$', 'openduty.auth.logout'),

    #USERS
    url(r'^users/$', 'openduty.users.list'),
    url(r'^users/new$', 'openduty.users.new'),
    url(r'^users/save', 'openduty.users.save'),
    url(r'^users/testnotification', 'openduty.users.testnotification'),
    url(r'^users/edit/(\d+)$', 'openduty.users.edit'),
    url(r'^users/delete/(\d+)$', 'openduty.users.delete'),

    #SERVICES
    url(r'^services/$', 'openduty.services.list'),
    url(r'^services/new$', 'openduty.services.new'),
    url(r'^services/save', 'openduty.services.save'),
    url(r'^services/edit/(.*)$', 'openduty.services.edit', name="service_detail"),
    url(r'^services/delete/(.*)$', 'openduty.services.delete'),
    url(r'^services/silence/(.*)$', 'openduty.services.silence'),
    url(r'^services/unsilence/(.*)$', 'openduty.services.unsilence'),

    #Policies
    url(r'^policies/$', 'openduty.escalation.list'),
    url(r'^policies/new$', 'openduty.escalation.new'),
    url(r'^policies/save', 'openduty.escalation.save'),
    url(r'^policies/edit/(.*)$', 'openduty.escalation.edit'),
    url(r'^policies/delete/(.*)$', 'openduty.escalation.delete'),


    #SCHEDULES
    url(r'^schedules/$', 'openduty.schedules.list'),
    url(r'^schedules/new$', 'openduty.schedules.new'),
    url(r'^schedules/save', 'openduty.schedules.save'),
    url(r'^schedules/edit/(?P<calendar_slug>[-\w]+)/$', 'openduty.schedules.edit'),
    url(r'^schedules/delete/(?P<calendar_slug>[-\w]+)/$', 'openduty.schedules.delete'),
    url(r'^schedules/view/(?P<calendar_slug>[-\w]+)/$', 'openduty.schedules.details',
        name='calendar_details',  kwargs={'periods': [Month]}),

    #EVENT
    url(r'^events/create/(?P<calendar_slug>[-\w]+)/$', 'openduty.events.create_or_edit_event', name='calendar_create_event'),
    url(r'^events/edit/(?P<calendar_slug>[-\w]+)/(?P<event_id>\d+)/$', 'openduty.events.create_or_edit_event', name='edit_event'),
    url(r'^events/destroy/(?P<calendar_slug>[-\w]+)/(?P<event_id>\d+)/$', 'openduty.events.destroy_event', name='destroy_event'),



    #SERVICES/API TOKEN
    url(r'^services/token_delete/(.*)$', 'openduty.services.token_delete'),
    url(r'^services/token_create/(.*)$', 'openduty.services.token_create'),

    #EVENT_LOG
    url(r'^$', 'openduty.event_log.list'),
    url(r'^dashboard/$', 'openduty.event_log.list'),
    url(r'^dashboard/service/(.*)$', 'openduty.event_log.get'),

    #INCIDENTS
    url(r'^incidents/details/(.*)$', 'openduty.incidents.details'),
    url(r'^incidents/update_type/$', 'openduty.incidents.update_type'),
    url(r'^incidents/forward_incident', 'openduty.incidents.forward_incident'),
    url(r'^incidents/silence/(.*)$', 'openduty.incidents.silence'),
    url(r'^incidents/unsilence/(.*)$', 'openduty.incidents.unsilence'),
    url(r'^incidents/on-call/$', ServicesByMe.as_view(), name="incidents_on_call" ),
    url(r'^incidents/list/$',
        FilteredSingleTableView.as_view(template_name='incidents/list2.html',
                                        table_class=IncidentTable, model=Incident,
                                        table_pagination={"per_page": 10},
                                        ),
        name='incident_list'),
   url(r'^twilio/(\d+)/(\d+)$', 'openduty.call_handler.read_notification'),
   url(r'^twilio/handle/(\d+)/(\d+)$', 'openduty.call_handler.handle_key'),


)

urlpatterns += patterns('',
        (r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )

urlpatterns += patterns('',
             (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
        )
