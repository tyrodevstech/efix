from dataclasses import fields
from rest_framework.serializers import ModelSerializer,StringRelatedField
# from app_api.models import UserProfile
from django.contrib.auth.models import User
from core.models import CustomUserRegistration,Area, Invoice, ServiceRequest
class AdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password','is_superuser']
        # extra_kwargs = {'password': {'write_only': True},'is_superuser':{'write_only':True}}

    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.set_password(validated_data['password'])
    #     instance.save()
    #     return instance

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['customerreg',]
        # depth=1
        # exclude='__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customerreg'] = CustomUserRegistrationSerializer(instance.customerreg).data
        return response
class CustomUserRegistrationSerializer(ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = CustomUserRegistration
        fields = '__all__'
        # depth=1
        # exclude = ['user__password',]
        # extra_kwargs = {'password': {'write_only': True},'is_superuser':{'write_only':True}}

    # def create(self, validated_data):
    #     return User.objects.create_superuser(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.set_password(validated_data['password'])
    #     instance.save()
    #     return instance
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['customer'] = UserSerializer(instance.user).data
    #     return response

class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'
class ServiceRequestSerializer(ModelSerializer):
    # technician = CustomUserRegistrationSerializer()
    # customer = UserSerializer(read_only=True)
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        depth = 1

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['customer'] = UserSerializer(instance.customer).data
    #     return response
class InvoiceSerializer(ModelSerializer):
    # technician = CustomUserRegistrationSerializer()
    # customer = UserSerializer(read_only=True)
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 3

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['customer'] = UserSerializer(instance.customer).data
    #     return response
