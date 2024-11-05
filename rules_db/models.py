from django.db import models
from polymorphic.models import PolymorphicModel
from core.models import ArticleBase, ArticleContent


class BasicEntryMixin(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(help_text="A description of what the entry represents in-game.")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Entry(PolymorphicModel, BasicEntryMixin):
    pass


class Page(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)


# <editor-fold desc="Expand Skills">
class Type(BasicEntryMixin):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Skill Type'
        verbose_name_plural = 'Skill Types'


class SkillOptions(BasicEntryMixin):
    # For a skill that gives multiple options to the player, ie Acolyte source, Favored Enemy type, Prestige Points
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Skill Option'
        verbose_name_plural = 'Skill Options'


class Skill(Entry):
    mechanics = models.TextField(help_text="The specific rules mechanics of the ability.")
    cost = models.IntegerField(verbose_name='Build Cost')
    types = models.ManyToManyField(Type, related_name='skills')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PeriodicSkill(Skill):
    pass


class PassiveSkill(Skill):
    ABILITY_TYPES = [
        ('PS', 'Passive'),
        ('PF', 'Proficiency'),
        ('PG', 'Paragon')
    ]
    ability_type = models.CharField(max_length=2, choices=ABILITY_TYPES, verbose_name='passive type',
                                    help_text="Passives are learned only once; proficiencies stack.")


class SkillDomain(BasicEntryMixin):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Skill Domain'
        verbose_name_plural = 'Skill Domains'


class SlotSkill(Skill):
    ABILITY_TYPES = [
        ('S', 'Spell'),
        ('T', 'Talent'),
    ]
    rank = models.IntegerField()
    ability_type = models.CharField(max_length=1, choices=ABILITY_TYPES, verbose_name='slot type')
    domain = models.ForeignKey(SkillDomain, related_name='skills', on_delete=models.CASCADE)


class ExaltedSkill(Skill):
    CRITERIA_TYPES = [
        ('Q', 'Quest'),
        ('A', 'Achievement')
    ]
    criteria_type = models.CharField(max_length=1, choices=CRITERIA_TYPES)
    criteria = models.TextField(verbose_name='unlock criteria',
                                help_text="The full text of requirements to be met before the skill can be learned.")
    EXALTED_TYPE = [
        ('EP', 'Passive'),
        ('ES', 'Exalted Slot'),
        ('EC', 'Capstone')
    ]
    exalted_type = models.CharField(max_length=2, choices=EXALTED_TYPE, verbose_name='exalted skill type')


class PrestigePoint(Skill):
    max_purchases = models.IntegerField()
    options = models.ForeignKey(SkillOptions, related_name='prestige_points', on_delete=models.CASCADE)


class UniqueMechanic(Skill):
    # For unique skills like artifact abilities; should not be searchable unless logged in to authorized account
    pass


class SkillAlias(models.Model):
    alias_name = models.CharField(max_length=50, null=True, blank=True,
                                  help_text="The name the skill appears as on the specified class.")
    alias_description = models.TextField(null=True, blank=True,
                                         help_text="The flavor description specific to the class the alias belongs to.")
    alias_domain = models.ForeignKey(SkillDomain, on_delete=models.CASCADE, null=True, blank=True,
                                     help_text="For spells/talents etc where the domain may differ class to class.")
    parent_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True,
                                     help_text="The baseline skill providing the mechanics.")
    alias_criteria = models.TextField(null=True, blank=True,
                                      help_text="For Exalted skill aliases only, to override the base criteria.")

    class Meta:
        verbose_name_plural = 'Skill Aliases'

    def __str__(self):
        return self.alias_name

    @property
    def parent_class(self):
        return self.class_skill.character_class


class Effect(Entry):
    mechanics = models.TextField(help_text="The specific rules mechanics of the effect.")
    duration = models.IntegerField(help_text="The standard duration of the effect in seconds. -1 for N/A or instant.",
                                   default=-1)
# </editor-fold>


# <editor-fold desc="Expand Crafting/Rituals">
class Component(Entry):
    COMPONENT_TYPES = [
        ('BU', 'Unrefined (Basic)'),
        ('BR', 'Refined (Basic)'),
        ('BE', 'Equipment (Basic)'),
        ('RL', 'Lesser (Ritual)'),
        ('RG', 'Greater (Ritual)'),
        ('RU', 'Unique (Ritual)'),
        ('SP', 'Special')
    ]
    component_type = models.CharField(max_length=2, choices=COMPONENT_TYPES)


class CraftableMixin(models.Model):
    components = models.ManyToManyField(Component)
    time = models.DurationField(help_text="Standard time to cast/craft, in minutes/seconds.",
                                verbose_name="crafting time")

    class Meta:
        abstract = True


class GenericItem(Entry):
    mechanics = models.TextField(help_text="The specific rules mechanics of the item.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Item"
        verbose_name_plural = "Items"


class EquipmentType(Type):
    CATEGORY_CHOICES = [
        ('HW', 'Weapon'),
        ('HS', 'Secondary'),
        ('AC', 'Accessory'),
        ('AS', 'Armor (Slot)'),
        ('AW', 'Armor (Weight)')
    ]
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Equipment Type"
        verbose_name_plural = "Equipment Types"
        ordering = ['name']


class Material(GenericItem):
    # Equipment materials with specific mechanics, ie granting a damage type or a periodic effect
    allowed_equipment = models.ManyToManyField(EquipmentType, related_name='materials_allowed',
                                               help_text="Which types of equipment the material can be used to craft.")
    material_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True,
                                       help_text="The skill granted by the item, if any.", verbose_name="skill")


class Consumable(GenericItem, CraftableMixin):
    types = models.ManyToManyField(Type, related_name='consumables_of_type')


class Ritual(ExaltedSkill, CraftableMixin):
    duration = models.IntegerField(default=1, help_text="Duration in months, including the month it is cast.")
    rank = models.IntegerField(default=0)
    frequency = models.CharField(max_length=50, help_text="Format: Nx per XYZ. I.E.: '1x per event', '3x per period'")
# </editor-fold>


# <editor-fold desc="Expand Classes">
class ClassOptions(BasicEntryMixin):
    # For classes that need a dropdown menu, ie picking a hybrid casting source or exalted subclass
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Class Option'
        verbose_name_plural = 'Class Options'


class CharacterClass(Entry):
    CLASS_TYPES = [
        ('B', 'Base Class'),
        ('M', 'Master Class'),
        ('E', 'Exalted Class'),
        ('S', 'Subclass'),
        ('C', 'Common/Background'),
        ('N', 'NPC Only')
    ]
    body_points = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill, related_name='character_classes', through='ClassSkills')
    class_type = models.CharField(max_length=1, choices=CLASS_TYPES, default='B')
    class_options = models.ManyToManyField(ClassOptions, related_name='character_classes', blank=True,
                                           help_text="Available class choices, i.e. casting source, subclass, etc.")
    class_options_help = models.CharField(max_length=50,
                                          help_text="A description of what the class options are for. Blank if n/a."
                                                    " Text is visible to players.",
                                          blank=True, null=True)

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = 'classes'
        ordering = ['name']

    def __str__(self):
        return self.name


class ClassSkills(models.Model):
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, verbose_name='class')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    alias = models.OneToOneField(SkillAlias, on_delete=models.CASCADE, related_name='class_skill', blank=True,
                                 null=True, help_text="Expanded options for the specified alias. Be sure to set "
                                                      "the description for the specified class, and domain if needed.")
    prerequisites = models.ForeignKey(ClassOptions, on_delete=models.CASCADE, blank=True, null=True,
                                      help_text="Set if skill is only available with certain class options, ie casting "
                                                "source, subclass, etc. Leave blank if available by default.")

    class Meta:
        verbose_name = 'skill'
        verbose_name_plural = 'skill List'
        unique_together = ('character_class', 'skill', 'alias')

    def __str__(self):
        if self.alias is not None:
            if self.alias.alias_name is not None:
                return self.alias.alias_name
        else:
            return self.skill.name
# </editor-fold>


class RulesChapter(models.Model):
    chapter_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, help_text="Name of chapter - do not include the chapter number.")
    introduction = models.OneToOneField(ArticleContent, on_delete=models.CASCADE,
                                        help_text="Non-mechanical introduction of the chapter.")


class RulesArticle(ArticleBase):
    chapter = models.ForeignKey(RulesChapter, on_delete=models.CASCADE)
    sort_order = models.IntegerField(help_text="Ascending order within chapter; same numbers will sort alphabetically.")
