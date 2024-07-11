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
    name = models.CharField(max_length=50)
    description = models.TextField()
    cost = models.IntegerField()
    types = models.ManyToManyField(Type, related_name='skills')

    def __str__(self):
        return self.name


class CharacterClass(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    body_points = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill, related_name='classes')

    def __str__(self):
        return self.name


class PlayerCharacterCard(models.Model):
    card_id = models.CharField(max_length=2)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    build_total = models.IntegerField(default=50)
    character_classes = models.ManyToManyField(CharacterClass)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f"{self.player.name} {self.card_id}"
