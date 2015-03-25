# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coursebase', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='likes',
            new_name='likecount',
        ),
    ]
