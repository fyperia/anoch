from django import forms
from django.db import models

# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("P", "Periodic"),
        ("C", "Passive/Prof"),
        ("S", "Spell"),
        ("T", "Talent"),
        ("E", "Exalted"),
        ("R", "Ritual"),
    ]

    name = models.CharField(max_length=50)
    description = models.TextField()
    mechanics = models.TextField()
    cost = models.IntegerField()
    types = models.ManyToManyField(Type, related_name='skills')
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='P')

    def __str__(self):
        return self.name


class CharacterClass(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    body_points = models.IntegerField(default=0)
    skill_list = models.ManyToManyField(Skill, related_name='character_classes', through='SkillAlias')

    class Meta:
        verbose_name_plural = 'character Classes'

    def __str__(self):
        return self.name


class SkillAlias(models.Model):
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    alias_name = models.CharField(max_length=50, null=True)
    alias_description = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'skill Aliases'

    def __str__(self):
        if self.alias_name is not None:
            return f'{self.skill.name} ({self.alias_name})'
        else:
            return self.skill.name


class PlayerCharacterCard(models.Model):
    card_id = models.CharField(max_length=2)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    build_total = models.IntegerField(default=50)
    character_classes = models.ManyToManyField(CharacterClass)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f"{self.player.name} {self.card_id}"
