# Generated by Django 5.0.7 on 2024-07-11 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anoch_db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='characterclass',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
