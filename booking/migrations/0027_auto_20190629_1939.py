# Generated by Django 2.2.1 on 2019-06-29 12:39

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0026_auto_20190622_1638'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='artistprofile',
            name='timeline',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, max_length=500, null=True), blank=True, size=None), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='historicalartistprofile',
            name='location',
            field=models.ForeignKey(blank=True, db_constraint=False, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='booking.Location'),
        ),
        migrations.AlterField(
            model_name='historicalartistprofile',
            name='skill',
            field=models.ForeignKey(blank=True, db_constraint=False, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='booking.Skill'),
        ),
        migrations.AlterField(
            model_name='historicalartistprofile',
            name='timeline',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, max_length=500, null=True), blank=True, size=None), blank=True, null=True, size=None),
        ),
    ]
