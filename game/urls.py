from django.urls import path
from . import views

urlpatterns = [
    path("", views.game),
    path('new/',views.create_game),
    path('<int:game_id>/move/',views.make_move),
    path('<int:game_id>/board/', views.get_board),
    path('<int:game_id>/renderlegal/', views.get_legal_sqrs),
    path('<int:game_id>/ai-move/', views.ai_move),
]