from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Menu(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to="menus")
    slug = models.SlugField(null=False ,unique=True, db_index=True, editable=False)
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="categories")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, db_index=True, editable=False)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products")
    description = models.TextField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"