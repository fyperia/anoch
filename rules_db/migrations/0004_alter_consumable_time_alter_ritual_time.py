# Generated by Django 5.0.7 on 2024-11-04 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_db', '0003_alter_consumable_time_alter_ritual_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumable',
            name='time',
            field=models.DurationField(help_text='Standard time to cast/craft, in minutes/seconds.', verbose_name='crafting time'),
        ),
        migrations.AlterField(
            model_name='ritual',
            name='time',
            field=models.DurationField(help_text='Standard time to cast/craft, in minutes/seconds.', verbose_name='crafting time'),
        ),
    ]
