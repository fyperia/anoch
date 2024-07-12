from django.urls import path

from . import views

app_name = 'db'
urlpatterns = [
    # .../db/
    path("", views.index, name="index"),
    # .../db/skills/1
    path("skills/<int:skill_id>/", views.skill, name="skills"),
    # .../db/classes/1
    path("classes/<int:class_id>/", views.character_class, name="classes"),
]
