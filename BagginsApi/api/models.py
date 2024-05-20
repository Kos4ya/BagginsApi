from django.db import models


class Point(models.Model):
    model_turnover = models.FileField(upload_to="upload_files/")
    model_order = models.FileField(upload_to="upload_files/")
