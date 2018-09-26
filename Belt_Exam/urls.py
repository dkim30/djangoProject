
from django.urls import path
from wish_list import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('dashboard',views.dashboard),
    path('logout',views.logout),
    path('home',views.home),
    path('create',views.create),
    path('wishes',views.wishes),
    path('add_item',views.add_item),
    path('addwish/<int:wish_id>', views.addwish),
    path('removewish/<int:wish_id>', views.removewish),
    path('wish/<int:wish_id>',views.wishInfo)
]
