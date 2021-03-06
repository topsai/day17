from django.db import models

# Create your models here.


class Host(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    users = models.CharField(max_length=30)

    class Meta:
        # db_table = "tablename"  # 定制表名
        verbose_name = "主机"

    def __str__(self):

        return self.name

    def __repr__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=60)
    h = models.ManyToManyField("Host")
    type_choices = [
        (1, "管理员"),
        (2, "用户"),
    ]
    ugrup = models.IntegerField(choices=type_choices, default=2)
    # a = models.CharField(max_length=20)

    def __str__(self):

        return self.name

    def __repr__(self):
        return self.name


class HostGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


# class UserGroup(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=30)
#
#     def __repr__(self):
#         return self.name
#
#     def __str__(self):
#         return self.name