# Generated by Django 5.0.7 on 2024-07-11 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anoch_db', '0002_characterclass_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playercharactercard',
            old_name='player_id',
            new_name='player',
        ),
        migrations.AlterField(
            model_name='characterclass',
            name='skills',
            field=models.ManyToManyField(related_name='classes', to='anoch_db.skill'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='types',
            field=models.ManyToManyField(related_name='skills', to='anoch_db.type'),
        ),
    ]