from rest_framework import status
from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
# from app_api.models import  UserProfile
from app_api.serializers import  AdminSerializer, AreaSerializer, CustomUserRegistrationSerializer, InvoiceSerializer, ServiceRequestSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Area, CustomUserRegistration, Invoice, ServiceRequest
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
class AdminViewSet(ModelViewSet):
    serializer_class = AdminSerializer
    queryset = User.objects.filter(is_superuser=True)
    def list(self, request):
        queryset = User.objects.filter(is_superuser=True).exclude(pk=request.user.pk).exclude(username='superadmin')
        serializer = AdminSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.filter(is_superuser=True)
        user = get_object_or_404(queryset, pk=pk)
        serializer = AdminSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CustomerRegistraionViewSet(ModelViewSet):
    serializer_class = CustomUserRegistrationSerializer
    queryset = CustomUserRegistration.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','role']

    def list(self, request):
        queryset = CustomUserRegistration.objects.filter().order_by('-id')
        role = request.query_params.get('role',None)
        if role is not None:
            queryset = queryset.filter(role=role)
        serializer = CustomUserRegistrationSerializer(self.filter_queryset(queryset), many=True)
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     user = get_object_or_404(self.queryset, pk=pk)
    #     serializer = AdminSerializer(user)
    #     return Response(serializer.data)

    # def create(self, request):
    #     serializer = AdminSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AreaViewSet(ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()

class ServiceRequestViewSet(ModelViewSet):
    serializer_class = ServiceRequestSerializer
    queryset = ServiceRequest.objects.all()
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,]
    filterset_fields = ('customer','priority')
    search_fields = ['servicereq_no','title','priority',]
class InvoiceViewSet(ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    # parser_classes = [FormParser,MultiPartParser]
    def create(self, request):
        print(request.data)
        print(request.FILES)
        serializer = InvoiceSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)