from django.contrib.auth.models import User
from django.db import models

class UserFavoriteComics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comics_list = models.JSONField(max_length=4096)

    class Meta:
        db_table = "userfavoritecomics"