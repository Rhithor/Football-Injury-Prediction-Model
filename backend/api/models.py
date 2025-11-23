from django.db import models


class PlayerData(models.Model):
    """Model to store player data for injury prediction"""
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=50)
    matches_played = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)
    previous_injuries = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.position}"

