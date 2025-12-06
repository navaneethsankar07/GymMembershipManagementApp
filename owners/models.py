from django.db import models
from user.models import User

class Gym(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gyms")
    name = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("owner", "name")
        
    def __str__(self):
        return self.name
