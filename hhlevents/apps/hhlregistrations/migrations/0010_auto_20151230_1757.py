# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhlregistrations', '0009_auto_20151214_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.CharField(max_length=100, choices=[('/static/img/3dtulostin01.png', '3dtulostin01.png'), ('/static/img/avoin_tiistai01.png', 'avoin_tiistai01.png'), ('/static/img/elektroniikka01.png', 'elektroniikka01.png'), ('/static/img/hacklab_fi01.png', 'hacklab_fi01.png'), ('/static/img/helsinkihacklab01.png', 'helsinkihacklab01.png'), ('/static/img/kokous01.png', 'kokous01.png'), ('/static/img/ompelukone01.png', 'ompelukone01.png'), ('/static/img/tyokalukasa01.png', 'tyokalukasa01.png')]),
        ),
    ]
