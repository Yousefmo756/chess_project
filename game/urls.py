from django.urls import path
from . import views

urlpatterns = [
    #path("", views.game),
    path('stat/',views.create_game),
]