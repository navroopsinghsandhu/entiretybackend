from django.db import models

class Users(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserName = models.CharField(unique=True, max_length=500)
    FirstName = models.CharField(max_length=500)
    LastName = models.CharField(max_length=500)
    Password = models.CharField(max_length=500, unique=True)

class Products(models.Model):
    ProductId = models.AutoField(primary_key=True)
    ProductName = models.CharField(unique=True, max_length=500)
    ProductPrice = models.IntegerField()
    ProductPhotoFileName = models.CharField(max_length=500)

class UserProductsMappings(models.Model):
    MappingId = models.AutoField(primary_key=True)
    UserId = models.IntegerField()
    ProductId = models.IntegerField()

class Roles(models.Model):
    RoleId = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=500)

class UserRolesMappings(models.Model):
    MappingId = models.AutoField(primary_key=True)
    UserId = models.IntegerField()
    RoleId = models.IntegerField()
