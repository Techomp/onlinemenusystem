from django.shortcuts import render, redirect
from .models import Menu, Category, Product



def menu_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    menu_list = Menu.objects.filter(account = request.user)
    data = {
        "menu_list": menu_list
    }

    return render(request, "menu/menu_list.html", data)

def menu_create(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST" and request.FILES['image']:
        image = request.FILES["image"]
        name = request.POST["name"]
        menu = Menu.objects.create(name = name, image = image, account = request.user)
        menu.save()

    return render(request, "menu/menu_form.html")


def menu_details(request, slug):
    menu = Menu.objects.get(slug=slug)
    categories = Category.objects.filter(menu = menu)
    data = {
        "menu": menu,
        "categories": categories,
    }
    return render(request, "menu/menu_details.html", data)


def category_details(request, slug, category_slug):
    menu = Menu.objects.get(slug=slug)
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)

    data = {
        "menu":menu,
        "category":category,
        "products":products
    }
    return render(request, "menu/category_details.html", data)