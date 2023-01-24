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
    if request.method == "POST": 
        name = request.POST["name"]
        if len(name) < 5:
            return render(request, "menu/menu_form.html", {
                "error": "İsim uzunluğu 4'den küçük"
            })
        
        if not("image" in request.FILES):
            return render(request, "menu/menu_form.html", {
                "error": "Resim yüklenmemiş"
            })
        image = request.FILES["image"]

        menu = Menu.objects.create(name = name, image = image, account = request.user)
        menu.save()
        
    return render(request, "menu/menu_form.html")


def menu_details(request, slug):
    try:
        menu = Menu.objects.get(slug=slug)
    except:
        return redirect("home")
    categories = Category.objects.filter(menu = menu)
    data = {
        "menu": menu,
        "categories": categories,
    }
    return render(request, "menu/menu_details.html", data)

def menu_edit(request, slug):
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        menu = Menu.objects.get(slug=slug)
    except:
        return redirect("menu")

    if(menu.account != request.user):
        return redirect("menu_details", slug=slug)

    if request.method == "POST" :
        if "image" in request.FILES:
            image = request.FILES["image"]
            menu.image = image
            if len(request.POST["name"]):
                name = request.POST["name"]
                menu.name = name
            menu.save()
        elif "name" in request.POST:
            name = request.POST["name"]
            menu.name = name
            menu.save()
              
        return redirect("menu_edit", slug=menu.slug)

    categories = Category.objects.filter(menu = menu)
    data = {
        "menu": menu,
        "categories": categories,
    }
    return render(request, "menu/menu_edit.html", data)


def category_edit(request, slug, category_slug):
    menu = Menu.objects.get(slug=slug)
    if(menu.account != request.user):
        return redirect("category_details", slug=slug, category_slug=category_slug)
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)

    data = {
        "menu":menu,
        "category":category,
        "products":products
    }
    return render(request, "menu/category_edit.html", data)


def category_details(request, slug, category_slug):
    menu = Menu.objects.get(slug=slug)
    category = Category.objects.get(slug=category_slug)
    if(category.menu != menu):
        return redirect("menu_details", slug = slug)
    products = Product.objects.filter(category=category)

    data = {
        "menu":menu,
        "category":category,
        "products":products
    }
    return render(request, "menu/category_details.html", data)