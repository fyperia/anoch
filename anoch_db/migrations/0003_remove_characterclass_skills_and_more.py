# Generated by Django 5.0.7 on 2024-07-15 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anoch_db', '0002_skill_category_alter_skillalias_alias_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='characterclass',
            name='skills',
        ),
        migrations.AddField(
            model_name='characterclass',
            name='skill_list',
            field=models.ManyToManyField(related_name='character_classes', to='anoch_db.skill'),
        ),
        migrations.DeleteModel(
            name='SkillAlias',
        ),
    ]