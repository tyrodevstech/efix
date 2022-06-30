from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
# from app_api.models import  UserProfile
from app_api.serializers import  AdminSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework.response import Response
# Create your views here.

class AdminViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = AdminSerializer
    queryset = User.objects.all()
    def list(self, request):
        queryset = User.objects.filter(is_superuser=True)
        serializer = AdminSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = AdminSerializer(user)
        return Response(serializer.data)

# class CarViewSet(ModelViewSet):
#     serializer_class = CarSerializer
#     queryset = Car.objects.all()
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['name', 'brand']


# class RentCarViewSet(ModelViewSet):
#     serializer_class = RentCarSerializer
#     queryset = RentCar.objects.all()