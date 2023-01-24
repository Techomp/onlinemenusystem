from django.contrib import admin
from .models import Menu, Category, Product

class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "account")
    search_fields = ("name", "account")
    list_filter = ("name", "account")

class CategoryAdmin(admin.ModelAdmin):
    list_display= ("name", "menu")
    search_fields = ("name", "menu")
    list_filter = ("menu",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "category")
    search_fields = ("name", "category")
    list_filter = ("price", "category")


admin.site.register(Menu)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

# Register your models here.
