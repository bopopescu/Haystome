# Generated by Django 2.0.2 on 2019-05-09 03:00

import booking.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistprofile',
            name='folioImg5',
            field=models.ImageField(blank=True, upload_to=booking.models.artist_folio_directory_path),
        ),
        migrations.AddField(
            model_name='artistprofile',
            name='folioImg6',
            field=models.ImageField(blank=True, upload_to=booking.models.artist_folio_directory_path),
        ),
        migrations.AddField(
            model_name='artistprofile',
            name='folioImg7',
            field=models.ImageField(blank=True, upload_to=booking.models.artist_folio_directory_path),
        ),
        migrations.AddField(
            model_name='artistprofile',
            name='folioImg8',
            field=models.ImageField(blank=True, upload_to=booking.models.artist_folio_directory_path),
        ),
        migrations.AddField(
            model_name='artistprofile',
            name='video',
            field=models.FileField(blank=True, upload_to=booking.models.artist_video_directory_path),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='folioImg1',
            field=models.ImageField(upload_to=booking.models.artist_folio_directory_path),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='folioImg2',
            field=models.ImageField(upload_to=booking.models.artist_folio_directory_path),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='folioImg3',
            field=models.ImageField(upload_to=booking.models.artist_folio_directory_path),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='folioImg4',
            field=models.ImageField(upload_to=booking.models.artist_folio_directory_path),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='highlights',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, max_length=500), size=None), size=None),
        ),
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.TextField(max_length=2000),
        ),
    ]
