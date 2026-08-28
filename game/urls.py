from django.urls import path
from . import views

urlpatterns = [
    path("", views.game),
    path('new/',views.create_game),
    path('<int:game_id>/move/',views.make_move)
]