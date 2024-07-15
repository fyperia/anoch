# Generated by Django 5.0.7 on 2024-07-14 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anoch_db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='category',
            field=models.CharField(choices=[('P', 'Periodic'), ('C', 'Passive/Prof'), ('S', 'Spell'), ('T', 'Talent'), ('E', 'Exalted'), ('R', 'Ritual')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='skillalias',
            name='alias_description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='skillalias',
            name='alias_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]