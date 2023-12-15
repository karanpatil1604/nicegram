import os
from django.conf import settings
from django.db import models
from accounts.models import User
from django.utils import timezone


class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    picture = models.ImageField(
        upload_to='media/posts/pics/', null=False, blank=False)
    caption = models.TextField()
    created = models.DateTimeField(
        default=timezone.now, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        if self.picture:
            image = os.path.join(settings.MEDIA_ROOT,
                                 'posts/pics', str(self.picture))
            os.remove(image)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Post {self.post_id} by {self.author.username}"
