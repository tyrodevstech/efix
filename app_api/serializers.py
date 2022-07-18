from rest_framework.serializers import ModelSerializer,ValidationError
from django.contrib.auth.models import User
from core.models import CustomUserRegistration,Area, Invoice, ServiceRequest, Division, District, Upazila
class AdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password','is_superuser']
        extra_kwargs = {'password': {'write_only': True},'is_superuser':{'write_only':True}}

    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)


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
    def validate_email(self, value):
        lower_email = value.lower()
        if CustomUserRegistration.objects.filter(email__iexact=lower_email).exists():
            raise ValidationError("This email already exits!")
        return lower_email

    def validate_phone(self, value):
        lower_phone = value.lower()
        if CustomUserRegistration.objects.filter(phone__iexact=lower_phone).exists():
            raise ValidationError("This phone already exits!")
        return lower_phone
    class Meta:
        model = CustomUserRegistration
        fields = '__all__'
        depth=1

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['customer'] = UserSerializer(instance.user).data
    #     return response


class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class ServiceRequestSerializer(ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        depth = 1


class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 2


class DivisionSerializer(ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'
        depth = 1


class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
        depth = 1


class UpazilaSerializer(ModelSerializer):
    class Meta:
        model = Upazila
        fields = '__all__'
        depth = 1


