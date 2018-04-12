# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-28 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20180326_2031'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': '\u8bfe\u7a0b\u7ba1\u7406', 'verbose_name_plural': '\u8bfe\u7a0b\u7ba1\u7406'},
        ),
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='\u8bfe\u7a0b\u673a\u6784'),
        ),
    ]