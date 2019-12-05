# Generated by Django 2.2.1 on 2019-06-10 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0021_auto_20190610_2038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='slug',
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
