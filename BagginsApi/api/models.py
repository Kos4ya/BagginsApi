from django.db import models


class Point(models.Model):
    model = models.FileField(upload_to="upload_files/")
