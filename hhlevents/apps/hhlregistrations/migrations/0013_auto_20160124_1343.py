# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hhlregistrations', '0012_auto_20160124_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_cost',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='materials_cost',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_registrations',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='messisevent',
            name='event_cost',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='messisevent',
            name='materials_cost',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='messisevent',
            name='max_registrations',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
    ]
