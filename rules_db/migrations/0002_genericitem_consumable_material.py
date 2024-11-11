# Generated by Django 5.0.7 on 2024-11-04 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericItem',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rules_db.entry')),
                ('mechanics', models.TextField(help_text='The specific rules mechanics of the item.')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
                'ordering': ['name'],
            },
            bases=('rules_db.entry',),
        ),
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('genericitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rules_db.genericitem')),
                ('time', models.IntegerField(help_text='Standard activation time in minutes.')),
                ('components', models.ManyToManyField(to='rules_db.component')),
                ('types', models.ManyToManyField(related_name='consumables_of_type', to='rules_db.type')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('rules_db.genericitem', models.Model),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('genericitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rules_db.genericitem')),
                ('allowed_equipment', models.ManyToManyField(help_text='Which types of equipment the material can be used to craft.', related_name='materials_allowed', to='rules_db.type')),
                ('types', models.ManyToManyField(related_name='materials_of_type', to='rules_db.type')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('rules_db.genericitem',),
        ),
    ]