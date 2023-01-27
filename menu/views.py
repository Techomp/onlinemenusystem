from django.shortcuts import render, redirect
from .models import Menu, Category, Product


def menu_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    menu_list = Menu.objects.filter(user = request.user)
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

        menu = Menu.objects.create(name = name, image = image, user = request.user)
        menu.save()
        return redirect("menu")
        
    return render(request, "menu/menu_form.html")


def menu_details(request, slug):
    try:
        menu = Menu.objects.get(slug=slug)
    except:
        return redirect("home")

    if not menu.user.account.has_paid():
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

    if(menu.user != request.user):
        return redirect("menu_details", slug=slug)

    if request.method == "POST" :
        if "image" in request.FILES:
            menu.image = request.FILES["image"]

        name = request.POST["name"]
        if len(name) > 4:
            menu.name = name
        
        menu.save()     
        return redirect("menu_edit", slug=menu.slug)

    categories = Category.objects.filter(menu = menu)
    data = {
        "menu": menu,
        "categories": categories,
    }
    return render(request, "menu/menu_edit.html", data)


def category_details(request, slug, category_slug):
    menu = Menu.objects.get(slug=slug)

    if not menu.user.account.has_paid():
        return redirect("home")
    category = Category.objects.get(slug=category_slug, menu=menu)
    if(category.menu != menu):
        return redirect("menu_details", slug = slug)
    products = Product.objects.filter(category=category)

    data = {
        "menu":menu,
        "category":category,
        "products":products
    }
    return render(request, "menu/category_details.html", data)


def category_create(request, slug):
    menu = Menu.objects.get(slug=slug)
    if(menu.user != request.user):
        return redirect("menu_details", slug=slug)
    
    if request.method == "POST":
        name = request.POST["name"]
        if(len(name) > 4):
            category = Category.objects.create(name=name, menu=menu)
            category.save()
    
    return redirect("menu_edit", slug=slug)


def category_edit(request, slug, category_slug):
    menu = Menu.objects.get(slug=slug)
    if(menu.user != request.user):
        return redirect("category_details", slug=slug, category_slug=category_slug)
    category = Category.objects.get(slug=category_slug, menu=menu)
    products = Product.objects.filter(category=category)

    if request.method == "POST":
        name = request.POST["name"]
        if(len(name) > 4):
            category.name = name
        if "image" in request.FILES:
            category.image = request.FILES["image"]

        category.save()
        return redirect("category_edit", slug=slug, category_slug=category.slug)

    data = {
        "menu":menu,
        "category":category,
        "products":products
    }
    return render(request, "menu/category_edit.html", data)

def category_delete(request, slug, category_slug):
    menu = Menu.objects.get(slug=slug)
    if(menu.user != request.user):
        return redirect("category_details", slug=slug, category_slug=category_slug)
    try:
        category = Category.objects.get(slug=category_slug, menu=menu)
    except:
        return redirect(request, "menu_edit", slug=slug)

    category.delete()

    return redirect("menu_edit", slug=slug)
    


def product_create(request, slug, category_slug):
    
    menu = Menu.objects.get(slug=slug)
    if(menu.user != request.user):
        return redirect("category_details", slug=slug, category_slug=category_slug)

    category = Category.objects.get(slug=category_slug, menu=menu)

    if(category.menu != menu):
        return redirect("menu_details", slug=slug)

    if request.method == "POST":
        name = request.POST["name"]
        if(len(name) > 4):
            product = Product.objects.create(name=name, category=category)
            product.save()
    
    return redirect("category_edit", slug= slug, category_slug = category_slug)
    
def product_edit(request, slug, category_slug, product_slug):
    menu = Menu.objects.get(slug=slug)

    if(menu.user != request.user):
        return redirect("category_details", slug=slug, category_slug=category_slug)

    category = Category.objects.get(slug=category_slug, menu = menu)
    product = Product.objects.get(slug=product_slug)
    if(category.menu != menu or product.category != category):
        return redirect("menu_details", slug=slug)
    
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        price = request.POST["price"]

        if "image" in request.FILES:
            image = request.FILES["image"]
            product.image = image

        if(len(name) > 4):
            product.name = name

        if(len(description) > 4):
            product.description = description

        if(float(price) > 0):
            product.price = float(price)

        product.save()
        return redirect("product_edit", slug=slug, category_slug = category_slug, product_slug= product_slug)

    data = {
        "menu":menu,
        "category": category,
        "product": product
    }
    return render(request, "menu/product_edit.html", data)



def product_delete(request, slug, category_slug, product_slug):
    
    menu = Menu.objects.get(slug=slug)
    if(menu.user != request.user):
        return redirect("category_details", slug=slug, category_slug=category_slug)

    category = Category.objects.get(slug=category_slug, menu=menu)

    if(category.menu != menu):
        return redirect("menu_details", slug=slug)

    product = Product.objects.get(slug=product_slug, category = category)
    product.delete()

    return redirect("category_edit", slug =slug, category_slug=category_slug)  