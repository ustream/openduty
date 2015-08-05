# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openduty', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='incident_key',
            field=models.ForeignKey(blank=True, to='openduty.Incident', null=True),
        ),
    ]
