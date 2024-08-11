from django.contrib import admin
from django.db import models
from prose.fields import RichTextField
from prose.models import AbstractDocument
from django.contrib.auth.models import User


class Player(models.Model):
    # Player will need to be automatically generated when account is made, or a character card is made, or something.
    # Some level of verification before creating the player is ideal, so that player numbers are not being allocated
    # to bots or registered users who will never actually play.
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    player_number = models.IntegerField(primary_key=True)

    @admin.display(description='username')
    def player_username(self):
        return self.user.username

    @admin.display(description='email')
    def player_email(self):
        return self.user.email

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"


# <editor-fold desc="Expand Articles">
class ArticleContent(AbstractDocument):
    pass


class ArticleTag(models.Model):
    CATEGORY_CHOICES = [
        ('D', 'Database'),
        ('I', 'Info'),
        ('B', 'Blog'),
    ]
    name = models.CharField(max_length=50, primary_key=True)
    slug = models.SlugField(unique=True, verbose_name='URL')
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        verbose_name = 'Article Tag'
        verbose_name_plural = 'Article Tags'


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
    tags = models.ManyToManyField(ArticleTag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    prepopulated_fields = {"slug": ("title",)}

    class Meta:
        abstract = True
# </editor-fold>


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)