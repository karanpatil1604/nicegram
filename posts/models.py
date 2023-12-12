from django.db import models
from accounts.models import User


class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    picture = models.ImageField(
        upload_to='posts/', null=False, blank=False)
    caption = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post {self.post_id} by {self.user.username}"
