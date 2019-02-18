from django.db import models


class VoicePost(models.Model):
    name = models.CharField(max_length=255)
    media_file = models.FileField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Voice Post'
        verbose_name_plural = 'Voice Posts'
