from django.db import models
from accounts.models import User


class Follower(models.Model):
    follower = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
