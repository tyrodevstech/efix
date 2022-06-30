from dataclasses import fields
from rest_framework.serializers import ModelSerializer
# from app_api.models import UserProfile
from django.contrib.auth.models import User

class AdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password','is_superuser']
        # extra_kwargs = {'password': {'write_only': True},'is_superuser':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        return user

    # def update(self, instance, validated_data):
    #     instance.set_password(validated_data['password'])
    #     instance.save()
    #     return instance


# class CarSerializer(ModelSerializer):
#     class Meta:
#         model = Car
#         fields = '__all__'


# class RentCarSerializer(ModelSerializer):
#     class Meta:
#         model = RentCar
#         fields = '__all__'