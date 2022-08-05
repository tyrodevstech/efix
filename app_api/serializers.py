from rest_framework.serializers import ModelSerializer,ValidationError
from django.contrib.auth.models import User
from core.models import CustomUserRegistration,Area, Invoice, NotificationToken, ServiceRequest, Division, District, Upazila
class AdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password','is_superuser']
        extra_kwargs = {'password': {'write_only': True},'is_superuser':{'write_only':True}}

    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)


class CustomUserRegistrationSerializer(ModelSerializer):
    def validate_email(self, value):
        if value:
            lower_email = value.lower()
            if hasattr(self.instance,'email'):
                if lower_email == self.instance.email.lower():
                    return lower_email
                elif CustomUserRegistration.objects.filter(email__iexact=lower_email).exists():
                    raise ValidationError("This email already exist!")
            return lower_email
        return value

    def validate_phone(self, value):
        if value:
            if hasattr(self.instance,'phone'):
                if value == self.instance.phone:
                    return value
            elif CustomUserRegistration.objects.filter(phone__iexact=value).exists() or User.objects.filter(username__iexact=value).exists():
                raise ValidationError("This phone already exist!")
        return value

    def validate(self, data):
        validated_data = super().validate(data)
        if self.instance:
            if not (self.instance.work_area or validated_data.get('work_area',None)) and validated_data.get('active',False):
                raise ValidationError("Please select work area first. ")
        return validated_data

    class Meta:
        model = CustomUserRegistration
        fields = '__all__'

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


class NotificationTokenSerializer(ModelSerializer):
    class Meta:
        model = NotificationToken
        fields = '__all__'
        depth = 1


