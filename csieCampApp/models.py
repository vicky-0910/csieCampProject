from django.contrib.auth.models import AbstractUser
from django.db import models
import random

#inherit django auth_user
class CampUser(AbstractUser):
    ROLE_CHOICES = (
        ('team', '小隊'),
        ('admin', '管理者'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='team')

#connect to teamuser
class TeamProfile(models.Model):
    user = models.OneToOneField(CampUser, on_delete=models.CASCADE, related_name="team_profile")
    current_points = models.IntegerField(default=0)   # 現有積分
    fixed_savings = models.IntegerField(default=-1)    # 定存

#connect to adminuser and teamprofie
class PointRecord(models.Model):
    team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE, related_name="records")
    change = models.IntegerField()  # 更動積分
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField() # 變動後持有積分
    modified_by = models.ForeignKey(CampUser, null=True, blank=True, on_delete=models.SET_NULL, related_name="modified_records")  # 紀錄哪個管理者修改

class GameStatus(models.Model):
    key = models.CharField(max_length=50, unique=True) 
    value = models.CharField(max_length=200, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True)  

class CommentBoard(models.Model):
    user = models.ForeignKey(CampUser, on_delete=models.CASCADE, related_name="user_comment")
    comment = models.TextField(blank=True, null=True)
    pos = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pos:
            self.pos = random.randint(-30, 30)
        super().save(*args, **kwargs)