# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeojsonCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_description', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeojsonFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_description', models.CharField(max_length=100, null=True, blank=True)),
                ('friendly_description', models.CharField(max_length=100, null=True, blank=True)),
                ('file_path', models.CharField(max_length=500)),
                ('category', models.ForeignKey(blank=True, to='aema_geography.GeojsonCategory', null=True)),
            ],
            options={
                'ordering': ('friendly_description', 'category'),
            },
        ),
        migrations.CreateModel(
            name='GeojsonMajorCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=30, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Halsatt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('location_desc', models.CharField(max_length=500, null=True, blank=True)),
                ('description', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Halsatt',
                'verbose_name_plural': 'Halsatt',
            },
        ),
        migrations.CreateModel(
            name='RitualSitesIronAgeRoman',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('shape_id', models.IntegerField(null=True, blank=True)),
                ('location', models.CharField(max_length=50, null=True, blank=True)),
                ('count', models.IntegerField(null=True, blank=True)),
                ('context', models.CharField(max_length=50, null=True, blank=True)),
                ('contents', models.CharField(max_length=200, null=True, blank=True)),
                ('description', models.CharField(max_length=150, null=True, blank=True)),
                ('shape', models.CharField(max_length=30, null=True, blank=True)),
                ('no_of_shr', models.CharField(max_length=30, null=True, blank=True)),
                ('site_type', models.CharField(max_length=40, null=True, blank=True)),
                ('species', models.CharField(max_length=60, null=True, blank=True)),
                ('dating', models.CharField(max_length=50, null=True, blank=True)),
                ('region', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Ritual Sites - Iron Age/Roman',
                'verbose_name_plural': 'Ritual Sites - Iron Age/Roman',
            },
        ),
        migrations.CreateModel(
            name='TribalRegalExtent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Tribal and Royal influence',
                'verbose_name_plural': 'Tribal and Royal influence',
            },
        ),
        migrations.AddField(
            model_name='geojsoncategory',
            name='major_category',
            field=models.ForeignKey(blank=True, to='aema_geography.GeojsonMajorCategory', null=True),
        ),
    ]
