from django.db import models

class homesite(models.Model):
    summary=models.CharField(max_length=200)