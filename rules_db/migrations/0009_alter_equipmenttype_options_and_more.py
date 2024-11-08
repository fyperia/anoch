# Generated by Django 5.0.7 on 2024-11-07 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_db', '0008_remove_material_types'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmenttype',
            options={'ordering': ['name'], 'verbose_name': 'Equipment Type', 'verbose_name_plural': 'Equipment Types'},
        ),
        migrations.AlterModelOptions(
            name='rulesarticle',
            options={'ordering': ['chapter__chapter_number', 'sort_order']},
        ),
        migrations.AlterModelOptions(
            name='ruleschapter',
            options={'ordering': ['chapter_number']},
        ),
        migrations.AddField(
            model_name='ruleschapter',
            name='category',
            field=models.CharField(choices=[('CharacterClass', 'Classes')], default='CharacterClass', max_length=20),
            preserve_default=False,
        ),
    ]
