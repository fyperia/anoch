from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from polymorphic.models import PolymorphicModel
from prose.fields import RichTextField
from prose.models import AbstractDocument


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    EMAIL_FIELD = 'email'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.get_full_name


class BasicEntryMixin(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(help_text="A description of what the entry represents in-game.")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Entry(PolymorphicModel, BasicEntryMixin):
    pass


# <editor-fold desc="Expand Skills">
class Type(BasicEntryMixin):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'OPT_Skill Type'
        verbose_name_plural = 'OPT_Skill Types'


class SkillOptions(BasicEntryMixin):
    # For a skill that gives multiple options to the player, ie Acolyte, Favored Enemy
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'OPT_Skill Option'
        verbose_name_plural = 'OPT_Skill Options'


class Skill(Entry):
    mechanics = models.TextField(help_text="The specific rules mechanics of the ability.")
    cost = models.IntegerField()
    types = models.ManyToManyField(Type, related_name='skills')


class PeriodicSkill(Skill):
    pass


class PassiveSkill(Skill):
    ABILITY_TYPES = [
        ('PS', 'Passive'),
        ('PF', 'Proficiency'),
        ('PG', 'Paragon')
    ]
    ability_type = models.CharField(max_length=2, choices=ABILITY_TYPES)


class SkillDomain(BasicEntryMixin):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'OPT_Skill Domain'
        verbose_name_plural = 'OPT_Skill Domains'


class SlotSkill(Skill):
    ABILITY_TYPES = [
        ('S', 'Spell'),
        ('T', 'Talent'),
    ]
    rank = models.IntegerField()
    ability_type = models.CharField(max_length=1, choices=ABILITY_TYPES)
    domain = models.ForeignKey(SkillDomain, related_name='skills', on_delete=models.CASCADE)


class ExaltedSkill(Skill):
    CRITERIA_TYPES = [
        ('Q', 'Quest'),
        ('A', 'Achievement'),
    ]
    criteria_type = models.CharField(max_length=1, choices=CRITERIA_TYPES)
    criteria = models.TextField()


class PrestigePoint(Skill):
    max_purchases = models.IntegerField()
    options = models.ForeignKey(SkillOptions, related_name='prestige_points', on_delete=models.CASCADE)


class UniqueMechanic(Skill):
    # For unique skills like artifact abilities; should not be searchable unless logged in to authorized account
    pass


class SkillAlias(models.Model):
    alias_name = models.CharField(max_length=50, null=True, blank=True)
    alias_description = models.TextField(null=True, blank=True)
    alias_domain = models.ForeignKey(SkillDomain, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'skill Aliases'


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
    time = models.IntegerField(help_text="Standard activation time in minutes.")

    class Meta:
        abstract = True


class GenericItem(Entry):
    mechanics = models.TextField(help_text="The specific rules mechanics of the item.")

    class Meta:
        abstract = True


class EquipmentType(Type):
    class Meta:
        verbose_name = "OPT_Equipment Type"
        verbose_name_plural = "OPT_Equipment Types"


class Material(GenericItem):
    # Equipment materials with specific mechanics, ie granting a damage type or a periodic effect
    allowed_equipment = models.ManyToManyField(Type, related_name='materials_allowed')
    types = models.ManyToManyField(Type, related_name='materials_of_type')


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
        verbose_name = "OPT_Class Options"
        verbose_name_plural = "OPT_Class Options"


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

    def __str__(self):
        return self.name


class ClassSkills(models.Model):
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    alias = models.OneToOneField(SkillAlias, on_delete=models.CASCADE, related_name='class_skill')
    prerequisites = models.ForeignKey(ClassOptions, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'skill'
        verbose_name_plural = 'skill List'
        unique_together = ('character_class', 'skill')

    def __str__(self):
        if self.alias.alias_name is not None:
            return self.alias.alias_name
        else:
            return self.skill.name
# </editor-fold>


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


# <editor-fold desc="Expand Articles">
class ArticleContent(AbstractDocument):
    pass


class ArticleTags(models.Model):
    CATEGORY_CHOICES = [
        ('D', 'Database'),
        ('I', 'Info'),
        ('B', 'Blog'),
    ]
    name = models.CharField(max_length=50, primary_key=True)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

    prepopulated_fields = {"slug": ("name",)}


class ArticleBase(models.Model):
    STATUS_CHOICES = [
        ('D', 'Draft'),
        ('P', 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    excerpt = RichTextField(null=True, blank=True)
    body = models.OneToOneField(ArticleContent, on_delete=models.CASCADE)
    publish_datetime = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='D')
    tags = models.ManyToManyField(ArticleTags)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    prepopulated_fields = {"slug": ("title",)}

    class Meta:
        abstract = True


class RulesChapter(models.Model):
    chapter_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, help_text="Name of chapter - do not include the chapter number.")
    introduction = models.OneToOneField(ArticleContent, on_delete=models.CASCADE,
                                        help_text="Non-mechanical introduction of the chapter.")


class RulesArticle(ArticleBase):
    chapter = models.ForeignKey(RulesChapter, on_delete=models.CASCADE)
    sort_order = models.IntegerField(help_text="Ascending order within chapter; same numbers will sort alphabetically.")
# </editor-fold>


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
