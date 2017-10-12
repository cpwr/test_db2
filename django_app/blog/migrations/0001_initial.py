# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('text', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'posts',
                'ordering': ('-pub_date', '-updated'),
            },
        ),
    ]