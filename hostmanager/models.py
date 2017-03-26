from django.db import models

# Create your models here.


class Host(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    user = models.CharField(max_length=30)

    def __repr__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=60)

