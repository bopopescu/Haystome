# Generated by Django 2.2.1 on 2019-06-03 04:57

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0019_auto_20190530_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistprofile',
            name='item_prepare',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, max_length=500, null=True), size=None), null=True, size=None),
        ),
        migrations.AddField(
            model_name='artistprofile',
            name='timeline',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, max_length=500, null=True), size=None), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='location',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='booking.Location'),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='skill',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='booking.Skill'),
        ),
    ]