from django.urls import path
from . import views

urlpatterns= [
    path("", views.menu_list, name="menu"),
    #path("create/", views.menu_create, name = "menu_create"),
    path("<slug:slug>/edit/", views.menu_edit, name="menu_edit"),
    path("<slug:slug>/", views.menu_details, name="menu_details"),
    path("<slug:slug>/edit/category/create/", views.category_create, name = "category_create"),
    path("<slug:slug>/<slug:category_slug>/edit/", views.category_edit, name = "category_edit"),
    path("<slug:slug>/<slug:category_slug>/delete/", views.category_delete, name = "category_delete"),
    path("<slug:slug>/<slug:category_slug>/", views.category_details, name = "category_details"),
    path("<slug:slug>/<slug:category_slug>/product/create", views.product_create, name = "product_create"),
    path("<slug:slug>/<slug:category_slug>/<slug:product_slug>/edit", views.product_edit, name = "product_edit")
]