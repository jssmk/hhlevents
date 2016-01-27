# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('happenings', '0001_initial'),
        ('hhlregistrations', '0011_messisevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_ptr', models.OneToOneField(serialize=False, to='happenings.Location', auto_created=True, parent_link=True, primary_key=True)),
                ('messis_id', models.CharField(blank=True, null=True, max_length=16)),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
            ],
            bases=('happenings.location',),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_cost',
            field=models.PositiveSmallIntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.CharField(choices=[('/static/img/elektroniikka01.png', 'elektroniikka01.png'), ('/static/img/hacklab_fi01.png', 'hacklab_fi01.png'), ('/static/img/ompelukone01.png', 'ompelukone01.png'), ('/static/img/helsinkihacklab01.png', 'helsinkihacklab01.png'), ('/static/img/tyokalukasa01.png', 'tyokalukasa01.png'), ('/static/img/kokous01.png', 'kokous01.png'), ('/static/img/3dtulostin01.png', '3dtulostin01.png'), ('/static/img/avoin_tiistai01.png', 'avoin_tiistai01.png')], max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='materials_cost',
            field=models.PositiveSmallIntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_registrations',
            field=models.PositiveSmallIntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_requirement',
            field=models.CharField(choices=[('RQ', 'Required'), ('OP', 'Optional'), ('NO', 'None'), ('HA', 'Handled by the organiser')], max_length=2, default='NO'),
        ),
        migrations.AlterField(
            model_name='messisevent',
            name='event_cost',
            field=models.PositiveSmallIntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='messisevent',
            name='image',
            field=models.CharField(choices=[('/static/img/elektroniikka01.png', 'elektroniikka01.png'), ('/static/img/hacklab_fi01.png', 'hacklab_fi01.png'), ('/static/img/ompelukone01.png', 'ompelukone01.png'), ('/static/img/helsinkihacklab01.png', 'helsinkihacklab01.png'), ('/static/img/tyokalukasa01.png', 'tyokalukasa01.png'), ('/static/img/kokous01.png', 'kokous01.png'), ('/static/img/3dtulostin01.png', '3dtulostin01.png'), ('/static/img/avoin_tiistai01.png', 'avoin_tiistai01.png')], max_length=100),
        ),
        migrations.AlterField(
            model_name='messisevent',
            name='materials_cost',
            field=models.PositiveSmallIntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='messisevent',
            name='max_registrations',
            field=models.PositiveSmallIntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='messisevent',
            name='messis_slug',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='messisevent',
            name='registration_requirement',
            field=models.CharField(choices=[('RQ', 'Required'), ('OP', 'Optional'), ('NO', 'None'), ('HA', 'Handled by the organiser')], max_length=2, default='NO'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='registered',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
