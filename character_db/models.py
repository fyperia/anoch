from django.db import models
from rules_db.models import BasicEntryMixin, Entry, Skill, CharacterClass, SkillAlias
from core.models import Player

# Create your models here.


# <editor-fold desc="Expand PC Card">
class Species(Entry):
    # The category for the creature i.e. elf, human
    species_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.species_name

    class Meta:
        verbose_name = 'OPT_Species'
        verbose_name_plural = 'OPT_Species'


class Race(Entry):
    # The sub-race for the creature i.e. Selendrian elf, Kormyrian human
    parent_species = models.ForeignKey(Species, on_delete=models.CASCADE)


class PCCharacterCard(models.Model):
    card_id = models.CharField(max_length=2)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    build_total = models.IntegerField(default=50)
    name = models.CharField(max_length=80)
    skills = models.ManyToManyField(Skill, through='CharacterSkills')
    character_classes = models.ManyToManyField(CharacterClass)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('card_id', 'player')

    def __str__(self):
        return f"{self.player.pk}-{self.card_id}"


class CharacterSkills(models.Model):
    character = models.ForeignKey(PCCharacterCard, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    stacks = models.IntegerField(default=1)
# </editor-fold>


# <editor-fold desc="Expand NPC Card">
class NPCCategory(BasicEntryMixin):
    rp_notes = models.TextField(null=True, blank=True, help_text="Optional notes on how to roleplay this NPC")
    skills = models.ManyToManyField(Skill, through='NPCCategorySkills')


class NPCCategorySkills(models.Model):
    npc_category = models.ForeignKey(NPCCategory, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    alias = models.OneToOneField(SkillAlias, on_delete=models.CASCADE, related_name='npc_skill')


class NPCCharacterCard(BasicEntryMixin):
    skills = models.ManyToManyField(Skill)
    rp_notes = models.TextField(null=True, blank=True, help_text="Optional notes on how to roleplay this NPC")
    categories = models.ManyToManyField(NPCCategory, related_name='npc_cards')
# </editor-fold>
