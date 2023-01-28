from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Menu(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to="menus")
    background_image = models.ImageField(upload_to="menus_backgrounds", default=("menus_backgrounds/default.jpg"))
    slug = models.SlugField(null=False ,unique=True, db_index=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="categories", null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, db_index=True, editable=False, unique=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        try:
            category = Category.objects.get(slug=slugify(self.name), menu=self.menu)
            self.slug = slugify(self.name)
            if not (category == self):
                slug = slugify(self.name) 
                i = 1
                while True:
                    try:
                        Category.objects.get(slug = slug + str(i), menu=self.menu)
                    except:
                        self.slug = slugify(self.name + str(i))
                        break;
                    i = i+1
        except:
            self.slug = slugify(self.name)
        
        return super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(db_index=True, editable=False, unique=True)
    image = models.ImageField(upload_to="products", null=True)
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        try:
            product = Product.objects.get(slug=slugify(self.name), category=self.category)
            self.slug = slugify(self.name)
            if not (product == self):
                slug = slugify(self.name) 
                i = 1
                while True:
                    try:
                        Product.objects.get(slug = slug + str(i), category=self.category)
                    except:
                        self.slug = slugify(self.name + str(i))
                        break;
                    i = i+1
        except:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"