from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("show/<str:name>", views.show, name="show")

]
