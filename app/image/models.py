import os.path

from django.db import models

image_types = (
    ("PNG", "PNG"),
    ("JPG", "JPG"),
    ("GIF", "GIF")
)


class Image(models.Model):
    label = models.CharField(max_length=50, verbose_name='Label')
    type = models.CharField(max_length=20, choices=image_types, default="", verbose_name='Type')
    image_file = models.ImageField(upload_to='uploads/images', verbose_name='Image File')

    def __str__(self):
        return self.label

