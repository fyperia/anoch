# Generated by Django 5.0.7 on 2024-10-30 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_db', '0005_skillalias_parent_skill'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='characterclass',
            options={'ordering': ['name'], 'verbose_name': 'class', 'verbose_name_plural': 'classes'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='skillalias',
            name='alias_criteria',
            field=models.TextField(blank=True, help_text='For Exalted skill aliases only, to override the base criteria.', null=True),
        ),
        migrations.AlterField(
            model_name='classskills',
            name='alias',
            field=models.OneToOneField(blank=True, help_text='Expanded options for the specified alias. Be sure to set the description for the specified class, and domain if needed.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_skill', to='rules_db.skillalias'),
        ),
        migrations.AlterField(
            model_name='classskills',
            name='character_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rules_db.characterclass', verbose_name='class'),
        ),
        migrations.AlterField(
            model_name='classskills',
            name='prerequisites',
            field=models.ForeignKey(blank=True, help_text='Set if skill is only available with certain class options, ie casting source, subclass, etc. Leave blank if available by default.', null=True, on_delete=django.db.models.deletion.CASCADE, to='rules_db.classoptions'),
        ),
        migrations.AlterField(
            model_name='skillalias',
            name='alias_description',
            field=models.TextField(blank=True, help_text='The flavor description specific to the class the alias belongs to.', null=True),
        ),
        migrations.AlterField(
            model_name='skillalias',
            name='alias_domain',
            field=models.ForeignKey(blank=True, help_text='For spells/talents etc where the domain may differ class to class.', null=True, on_delete=django.db.models.deletion.CASCADE, to='rules_db.skilldomain'),
        ),
        migrations.AlterField(
            model_name='skillalias',
            name='alias_name',
            field=models.CharField(blank=True, help_text='The name the skill appears as on the specified class.', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='skillalias',
            name='parent_skill',
            field=models.ForeignKey(blank=True, help_text='The baseline skill providing the mechanics.', null=True, on_delete=django.db.models.deletion.CASCADE, to='rules_db.skill'),
        ),
    ]