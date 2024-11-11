# Generated by Django 5.0.7 on 2024-11-11 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_db', '0011_ruleschapter_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rulesarticle',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='rules_db.ruleschapter'),
        ),
    ]