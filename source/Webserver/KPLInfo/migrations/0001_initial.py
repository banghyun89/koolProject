# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RowOBDData',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('time', models.DateTimeField()),
                ('vss', models.DecimalField(max_digits=10, decimal_places=2)),
                ('maf', models.DecimalField(max_digits=10, decimal_places=2)),
                ('kpl', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
    ]
