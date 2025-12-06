from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=[
        ("customer", "Customer"),
        ("owner", "Owner")
    ], default="customer")
    age = models.PositiveIntegerField(null=True, blank=True)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    gym = models.ForeignKey('owners.Gym', on_delete=models.CASCADE, related_name="members",default='')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} → {self.gym.name}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gym = models.ForeignKey('owners.Gym', on_delete=models.CASCADE,default='')
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default="success")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.gym.name}"
