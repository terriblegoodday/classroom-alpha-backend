# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-29 09:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_object', jsonfield.fields.JSONField(verbose_name='Объект задания')),
                ('generator_id', models.CharField(max_length=100, verbose_name='ID генератора')),
                ('date_created', models.DateTimeField(verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Задание',
                'ordering': ['?'],
                'get_latest_by': 'date_created',
                'verbose_name_plural': 'Задания',
            },
            managers=[
                ('tasks', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SolvedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generator_id', models.CharField(max_length=100, verbose_name='ID генератора')),
                ('date_created', models.DateTimeField(verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Решенное задание',
                'get_latest_by': 'date_created',
                'verbose_name_plural': 'Решенные задания',
            },
        ),
    ]
