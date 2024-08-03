from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='images_created',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='images_liked')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
