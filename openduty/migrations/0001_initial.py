# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(default=b'log', max_length=b'100', choices=[(b'acknowledge', b'acknowledge'), (b'resolve', b'resolve'), (b'silence_service', b'silence service'), (b'silence_incident', b'silence incident'), (b'forward', b'forward'), (b'log', b'log'), (b'notified', b'notified'), (b'notification_failed', b'notification failed'), (b'trigger', b'trigger')])),
                ('data', models.TextField()),
                ('occurred_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'eventlog',
                'verbose_name_plural': 'eventlog',
            },
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('incident_key', models.CharField(max_length=200)),
                ('event_type', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=200)),
                ('details', models.TextField()),
                ('occurred_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'incidents',
                'verbose_name_plural': 'incidents',
            },
        ),
        migrations.CreateModel(
            name='IncidentSilenced',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('silenced', models.BooleanField(default=False)),
                ('silenced_until', models.DateTimeField()),
                ('incident', models.ForeignKey(to='openduty.Incident')),
            ],
        ),
        migrations.CreateModel(
            name='SchedulePolicy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
                ('repeat_times', models.IntegerField()),
            ],
            options={
                'verbose_name': 'schedule_policy',
                'verbose_name_plural': 'schedule_policies',
            },
        ),
        migrations.CreateModel(
            name='SchedulePolicyRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('escalate_after', models.IntegerField()),
                ('schedule', models.ForeignKey(blank=True, to='schedule.Calendar', null=True)),
                ('schedule_policy', models.ForeignKey(related_name='rules', to='openduty.SchedulePolicy')),
                ('user_id', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'schedule_policy_rule',
                'verbose_name_plural': 'schedule_policy_rules',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('name', models.CharField(unique=True, max_length=80)),
                ('id', uuidfield.fields.UUIDField(primary_key=True, serialize=False, editable=False, max_length=32, blank=True, unique=True)),
                ('retry', models.IntegerField(null=True, blank=True)),
                ('escalate_after', models.IntegerField(null=True, blank=True)),
                ('notifications_disabled', models.BooleanField(default=False)),
                ('policy', models.ForeignKey(blank=True, to='openduty.SchedulePolicy', null=True)),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'service',
            },
        ),
        migrations.CreateModel(
            name='ServiceSilenced',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('silenced', models.BooleanField(default=False)),
                ('silenced_until', models.DateTimeField()),
                ('service', models.ForeignKey(to='openduty.Service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceTokens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('service_id', models.ForeignKey(to='openduty.Service')),
            ],
            options={
                'verbose_name': 'service_tokens',
                'verbose_name_plural': 'service_tokens',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('pushover_user_key', models.CharField(max_length=50)),
                ('pushover_app_key', models.CharField(max_length=50)),
                ('slack_room_name', models.CharField(max_length=50)),
                ('prowl_api_key', models.CharField(max_length=50, blank=True)),
                ('prowl_application', models.CharField(max_length=256, blank=True)),
                ('prowl_url', models.CharField(max_length=512, blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='servicetokens',
            name='token_id',
            field=models.ForeignKey(to='openduty.Token'),
        ),
        migrations.AddField(
            model_name='incident',
            name='service_key',
            field=models.ForeignKey(to='openduty.Service'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='incident_key',
            field=models.ForeignKey(to='openduty.Incident', blank=True),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='service_key',
            field=models.ForeignKey(to='openduty.Service'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(related_name='users', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='incident',
            unique_together=set([('service_key', 'incident_key')]),
        ),
    ]
