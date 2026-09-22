from django.db import models

# Create your models here.
class ChessGame(models.Model):
    positions = models.JSONField()
    turn = models.CharField(max_length=5, default="white")
    status = models.CharField(max_length=20, default="ongoing")
    castling_flags = models.JSONField()
    board_snapshots=models.JSONField(default=list)
    moves_log = models.JSONField()
    vs_ai = models.BooleanField(default=False)