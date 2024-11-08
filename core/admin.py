from django.contrib import admin
from django.contrib.admin import widgets
from django.forms import Textarea, TextInput

from django.db import models
from django.utils.text import format_lazy

from .models import (Player, ArticleTag, ArticleContent)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_number', '__str__', 'player_username', 'player_email')
    list_select_related = True
    search_fields = ('player_number', '__str__', 'player_username', 'player_email')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ArticleTag)
class ArticleTagsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category', 'slug')
    search_fields = ('__str__', 'category', 'slug')


@admin.register(ArticleContent)
class ArticleContentAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('__str__',)
