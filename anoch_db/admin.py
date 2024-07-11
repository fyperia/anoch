from django.contrib import admin

from .models import Type, Skill, CharacterClass

# Register your models here.
admin.site.register(Type)
admin.site.register(Skill)
admin.site.register(CharacterClass)
