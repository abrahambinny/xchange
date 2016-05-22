# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('country', models.CharField(max_length=100, db_index=True)),
                ('currency', models.CharField(max_length=200, db_index=True)),
                ('code', models.CharField(max_length=50, db_index=True)),
                ('symbol', models.CharField(max_length=50, db_index=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='XchangeStore',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('main_title', models.CharField(max_length=250)),
                ('main_category', models.CharField(max_length=200, db_index=True)),
                ('category', models.CharField(max_length=200, db_index=True)),
                ('country', models.CharField(max_length=100, db_index=True)),
                ('region', models.CharField(max_length=150, db_index=True)),
                ('sub_region', models.CharField(max_length=150, db_index=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('from_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_num', models.CharField(max_length=100)),
                ('is_international', models.BooleanField(default=False, db_index=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('image_url', models.TextField(blank=True, null=True)),
                ('image_url_vendor', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='barter.Question'),
        ),
    ]
