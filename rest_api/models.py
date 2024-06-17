from django.db import models


class MyToken(models.Model):
    id = models.AutoField(primary_key=True)
    tokens = models.TextField()

    class Meta:
        managed = False
        db_table = 'mytoken'


class MyLinks(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.TextField()
    title = models.TextField()
    icon = models.TextField()
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'mylinks'
