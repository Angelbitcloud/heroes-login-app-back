from django.contrib.auth.models import User
from django.db import models

class Comic(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title

class UserFavoriteComic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comic')
