# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pointset', '0002_pointset_given_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointset',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
