from django.db import models


class Message(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    diff_gender = models.BooleanField(null=True, verbose_name='Differentiable by gender')
    message = models.TextField(max_length=500, verbose_name='Message')
    message_female = models.TextField(max_length=500, null=True, blank=True, verbose_name='Message (F)')
    csv_fields = models.FileField(upload_to='uploads/message_fields', verbose_name='CSV File')
    html = models.BooleanField(default=False)

    def __str__(self):
        return self.title
