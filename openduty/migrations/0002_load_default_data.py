# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.contrib.auth import models as auth_models
from django.core.management import call_command

from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        #Creating root user
        try:
            auth_models.User.objects.get(username='root')
        except auth_models.User.DoesNotExist:
            print '*' * 80
            print 'Creating root user -- login: root, password: toor'
            print '*' * 80
            assert auth_models.User.objects.create_superuser('root', 'admin@localhost', 'toor')
        else:
            print 'Test user already exists.'

        ##Loading user profile
        #call_command("loaddata", "openduty_userprofile")

    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'openduty.eventlog': {
            'Meta': {'object_name': 'EventLog'},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'occurred_at': ('django.db.models.fields.DateTimeField', [], {}),
            'service_key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openduty.Service']"})
        },
        u'openduty.incident': {
            'Meta': {'unique_together': "(('service_key', 'incident_key'),)", 'object_name': 'Incident'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_key': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'occurred_at': ('django.db.models.fields.DateTimeField', [], {}),
            'service_key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openduty.Service']"})
        },
        u'openduty.schedulepolicy': {
            'Meta': {'object_name': 'SchedulePolicy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'repeat_times': ('django.db.models.fields.IntegerField', [], {})
        },
        u'openduty.schedulepolicyrule': {
            'Meta': {'object_name': 'SchedulePolicyRule'},
            'escalate_after': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Calendar']", 'null': 'True', 'blank': 'True'}),
            'schedule_policy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': u"orm['openduty.SchedulePolicy']"}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'openduty.service': {
            'Meta': {'object_name': 'Service'},
            'escalate_after': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'policy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openduty.SchedulePolicy']", 'null': 'True', 'blank': 'True'}),
            'retry': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'openduty.servicetokens': {
            'Meta': {'object_name': 'ServiceTokens'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'service_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openduty.Service']"}),
            'token_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openduty.Token']"})
        },
        u'openduty.token': {
            'Meta': {'object_name': 'Token'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        },
        u'openduty.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pushover_app_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pushover_user_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slack_room_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'schedule.calendar': {
            'Meta': {'object_name': 'Calendar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['openduty']
    symmetrical = True
