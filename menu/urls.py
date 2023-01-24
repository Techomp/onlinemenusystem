from django.urls import path
from . import views

urlpatterns= [
    path("", views.menu_list, name="menu"),
    path("create/", views.menu_create, name = "menu_create"),
    path("<slug:slug>/edit/", views.menu_edit, name="menu_edit"),
    path("<slug:slug>/", views.menu_details, name="menu_details"),
    path("<slug:slug>/<slug:category_slug>/", views.category_details, name = "category_details"),
]