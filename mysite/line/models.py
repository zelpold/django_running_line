from django.db import models


# Create your models here.
class LineText(models.Model):
    line_text = models.TextField()
    pub_date = models.DateTimeField("Время публикации")
