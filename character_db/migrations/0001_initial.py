# Generated by Django 5.0.7 on 2024-08-11 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stacks', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='NPCCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(help_text='A description of what the entry represents in-game.')),
                ('rp_notes', models.TextField(blank=True, help_text='Optional notes on how to roleplay this NPC', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NPCCategorySkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='NPCCharacterCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(help_text='A description of what the entry represents in-game.')),
                ('rp_notes', models.TextField(blank=True, help_text='Optional notes on how to roleplay this NPC', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PCCharacterCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.CharField(max_length=2)),
                ('build_total', models.IntegerField(default=50)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
    ]
