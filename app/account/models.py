from django.db import models
from django.conf import settings
import uuid


def profile_pic_path(instance, filename):
    unique = uuid.uuid4()
    return "users/user_{pk}/profile/{unique}{filename}".format(pk=instance.pk, unique=unique, filename=filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=profile_pic_path, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

