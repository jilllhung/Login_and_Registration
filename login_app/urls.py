from django.urls import path
from . import views

urlpatterns = [
    # render routes
    path('', views.index),
    path('success', views.success),

    #redirect routes
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
]
