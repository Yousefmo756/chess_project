from django.db import models

# Create your models here.
class ChessGame(models.Model):
    positions = models.JSONField()
    turn = models.CharField(max_length=5, default="white")
    status = models.CharField(max_length=20, default="ongoing")
    moves_log=models.CharField(max_length=50)