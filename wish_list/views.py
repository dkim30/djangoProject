from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages

def index(request):
    return render(request,"index.html")

def register(request):
    results = User.objects.register(request.POST)
    if isinstance(results, User):
        request.session['user_id'] = results.id 
        messages.add_message(request, messages.SUCCESS, 'Welcome to our site, {}'.format(results.username))
        return redirect("/")
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
        return redirect("/")

def login(request):
    results = User.objects.login(request.POST)
    if isinstance(results, User):
        request.session['user_id'] = results.id 
        messages.add_message(request, messages.SUCCESS, "Welcome back,{}".format(results.username))
        return redirect("/wishes")
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
        return redirect("/")

def dashboard(request):
    print(Wish.objects.all())
    context = {
        "wishes":Wish.objects.all()
    }
    return render(request, "dashboard.html",context)

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    return redirect('/dashboard')

def create(request):
    return render(request, "createItem.html")

def wishes(request):
    wish_list = User.objects.get(id=request.session["user_id"]).wish_list.all()
    wishes = Wish.objects.all()
    for wish in wish_list:
        wishes = wishes.exclude(id=wish.id)
    return render(request, "dashboard.html", {"wishes": wishes, "wish_list": wish_list})

def add_item(request):
    results = Wish.objects.add_item(request.POST, request.session['user_id'])
    print(results)
    if isinstance(results, Wish):
        messages.add_message(request, messages.SUCCESS, 'You successfully added an item to your wishlist')
        return redirect('/wishes')
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
    return redirect('/wishes')

def addwish(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session['user_id'])
    wish.favs.add(user)
    return redirect("/wishes")

def removewish(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session['user_id'])
    wish.favs.remove(user)
    return redirect("/wishes")

def wishInfo(request, wish_id):
    wish = Wish.objects.get(id= wish_id)
    context = {
        "wish":wish
    }
    return render(request, "info.html", context)


