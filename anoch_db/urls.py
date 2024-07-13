from django.urls import path

from . import views
from .views import SearchResultsView

app_name = 'db'
urlpatterns = [
    # .../db/
    path("", views.index, name="index"),
    # .../db/skills/1
    path("skills/<int:skill_id>/", views.skill, name="skills"),
    # .../db/classes/1
    path("classes/<int:class_id>/", views.character_class, name="classes"),
    # .../db/search/
    path("search/", SearchResultsView.as_view(), name="search"),
]
