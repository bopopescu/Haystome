# Generated by Django 2.2.1 on 2019-05-30 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_auto_20190530_0934'),
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
            model_name='bookingrequest',
            name='facilitator',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_superuser': False}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
