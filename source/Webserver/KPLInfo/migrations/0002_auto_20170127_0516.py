# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KPLInfo', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RowOBDData',
            new_name='Obd',
        ),
    ]
