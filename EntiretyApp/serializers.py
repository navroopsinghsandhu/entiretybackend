from rest_framework import serializers
from EntiretyApp.models import Users, Products, UserProductsMappings, Roles, UserRolesMappings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users 
        fields=('UserId','UserName','FirstName','LastName','Password')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields=('ProductId','ProductName','ProductPrice','ProductPhotoFileName')

class UserProductsMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProductsMappings
        fields=('MappingId','UserId','ProductId')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Roles
        fields=('RoleId','Role')

class UserRolesMappingsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserRolesMappings
        fields=('MappingId','UserId','RoleId')