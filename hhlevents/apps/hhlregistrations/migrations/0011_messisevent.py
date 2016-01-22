# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('happenings', '0001_initial'),
        ('hhlregistrations', '0010_auto_20151230_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessisEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='happenings.Event', serialize=False, primary_key=True)),
                ('uuid', models.UUIDField(editable=False, default=uuid.uuid4)),
                ('extra_url', models.URLField(blank=True)),
                ('registration_requirement', models.CharField(max_length=2, choices=[('RQ', 'Required'), ('OP', 'Optional'), ('NO', 'None')])),
                ('max_registrations', models.PositiveSmallIntegerField(default=0)),
                ('close_registrations', models.DateTimeField(null=True, blank=True)),
                ('payment_due', models.DateTimeField(null=True, blank=True)),
                ('event_cost', models.PositiveSmallIntegerField(default=0)),
                ('materials_cost', models.PositiveSmallIntegerField(default=0)),
                ('materials_mandatory', models.BooleanField(default=False)),
                ('image', models.CharField(max_length=100, choices=[('/static/img/3dtulostin01.png', '3dtulostin01.png'), ('/static/img/avoin_tiistai01.png', 'avoin_tiistai01.png'), ('/static/img/elektroniikka01.png', 'elektroniikka01.png'), ('/static/img/hacklab_fi01.png', 'hacklab_fi01.png'), ('/static/img/helsinkihacklab01.png', 'helsinkihacklab01.png'), ('/static/img/kokous01.png', 'kokous01.png'), ('/static/img/ompelukone01.png', 'ompelukone01.png'), ('/static/img/tyokalukasa01.png', 'tyokalukasa01.png')])),
                ('messis_slug', models.CharField(max_length=255, editable=False)),
            ],
            options={
                'verbose_name': 'Messis event',
                'verbose_name_plural': 'Messis events',
                'ordering': ['-end_date'],
            },
            bases=('happenings.event',),
        ),
    ]
