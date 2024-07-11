from django.urls import path

from . import views

urlpatterns = [
    # .../db/
    path("", views.index, name="index"),
    # .../db/skill/1
    path("skill/<int:skill_id>/", views.skill, name="skill"),
    # .../db/class/1
    path("class/<int:class_id>/", views.character_class, name="class"),
]
