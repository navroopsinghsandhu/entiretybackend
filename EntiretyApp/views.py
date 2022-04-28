from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from numpy import product
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from EntiretyApp.models import Users, Products, UserProductsMappings, UserRolesMappings, Roles
from EntiretyApp.serializers import UserSerializer, ProductSerializer, UserProductsMappingSerializer, RoleSerializer, UserRolesMappingsSerializer

from django.core.files.storage import default_storage
import hashlib

@csrf_exempt
def userRegistrationApi(request,id=0):
    if request.method=='GET':
        users = Users.objects.all()
        users_serializer=UserSerializer(users,many=True)
        return JsonResponse(users_serializer.data,safe=False)
    elif request.method=='POST':
        user_data=JSONParser().parse(request)
        role_id = 2
        if(user_data["wantMembership"]) :
            role_id = 3
        user_data['Password'] = hashlib.sha256(str(user_data['Password']).encode('utf-8')).hexdigest()
        users_serializer=UserSerializer(data=user_data)  
        if users_serializer.is_valid():
            users_serializer.save()
            user_id = Users.objects.filter(UserName=user_data['UserName'])\
                               .values_list('UserId', flat=True)
            role_mapping_serializer = UserRolesMappingsSerializer(data={'UserId' : user_id[0], 'RoleId' : role_id})
            if role_mapping_serializer.is_valid():
                role_mapping_serializer.save()
            return JsonResponse("Registration Successful",safe=False)
        return JsonResponse("Failed to Register",safe=False)

@csrf_exempt
def userLoginApi(request):
    data = JSONParser().parse(request)
    userExist = False
    userId = 0
    username = data["UserName"]
    password = data["Password"]
    users = Users.objects.all()
    users_serializer=UserSerializer(users,many=True)
    for x in users_serializer.data:
        usernameExist = False
        passwordExist = False
        for key, value in x.items():
            if(key == 'UserId'):
                userId = value
                roleId = UserRolesMappings.objects.filter(UserId=userId)\
                               .values_list('RoleId', flat=True)
                role = Roles.objects.filter(RoleId = roleId[0])
                role_serializer=RoleSerializer(role,many=True)
                userRole = role_serializer.data[0]["Role"]
            if(key == 'FirstName'):
                userName = value
            if(key == 'UserName' and value == username):
                usernameExist = True
            if(key == 'Password' and value == hashlib.sha256(str(password).encode('utf-8')).hexdigest()) :
                passwordExist = True
            if(usernameExist and passwordExist) :
                userExist = True
                break
        if(userExist) :
            break
    if(userExist) :
        return JsonResponse({"message" : "Login Successful", "token": userId, "role" : userRole, "UserName" : userName},safe=False)
    return JsonResponse({"message" : "Username or Password is incorrect", "token" : '', "role" : '',  "UserName" : ''},safe=False)
    
@csrf_exempt
def productsApi(request,id=0):
    if request.method=='GET':
        products = Products.objects.all()
        print("products", products)
        products_serializer=ProductSerializer(products,many=True)
        return JsonResponse(products_serializer.data,safe=False)
    elif request.method=='POST':
        product_data=JSONParser().parse(request)
        products_serializer=ProductSerializer(data=product_data)
        if products_serializer.is_valid():
            products_serializer.save()
            return JsonResponse("Product added",safe=False)
        return JsonResponse("Failed to add the product",safe=False)
    elif request.method=='DELETE':
        products = Products.objects.get(ProductId=id)
        mappings=UserProductsMappings.objects.filter( ProductId=id)
        mappings.delete()
        products.delete()
        return JsonResponse("Product deleted",safe=False)

@csrf_exempt
def userProductMapApi(request,userid=0, productid=0):
    if request.method=='GET':
        mappingids = UserProductsMappings.objects.filter(UserId=userid)\
                               .values_list('ProductId', flat=True)
        dataArray = {}
        y = 1
        keyHeader = "product"
        for x in mappingids:
            print(x)
            product = Products.objects.filter(ProductId = x)
            products_serializer=ProductSerializer(product,many=True)
            key = keyHeader+str(y)
            print(key)
            dataArray[key] = products_serializer.data
            y += 1
        return JsonResponse(dataArray, safe=False)
    elif request.method=='POST':
        mapping_data=JSONParser().parse(request)
        mapping_serializer=UserProductsMappingSerializer(data=mapping_data)
        if mapping_serializer.is_valid():
            mapping_serializer.save()
            return JsonResponse("Product added to the cart",safe=False)
        return JsonResponse("Failed to add product to the cart",safe=False)
    elif request.method=='DELETE':
        mappings=UserProductsMappings.objects.get(UserId=userid, ProductId=productid)
        mappings.delete()
        return JsonResponse("Product removed from the cart",safe=False)
    
@csrf_exempt
def userRoleMapApi(request,userid=0):
    if request.method=='GET':
        roleId = UserRolesMappings.objects.filter(UserId=userid)\
                               .values_list('RoleId', flat=True)
        role = Roles.objects.filter(RoleId = roleId[0])
        role_serializer=RoleSerializer(role,many=True)
        return JsonResponse(role_serializer.data, safe=False)
  
@csrf_exempt
def userProductMapCheckApi(request,userid=0, productid=0):
    if request.method=='GET':
        mappingids = UserProductsMappings.objects.filter(UserId=userid)\
                               .values_list('ProductId', flat=True)
        
        isAdded = "False"
        if(int(productid) in mappingids) :
            isAdded = "True"
        return JsonResponse({"isAdded" : isAdded}, safe=False)