from io import BytesIO
from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from app_api.permissions import IsPostOrIsAuthenticated
from app_api.serializers import  *
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from app_api.utils import notify_admins, send_push_message
from core.custom_context_processor import get_mdod
from core.models import Area, CustomUserRegistration, Invoice, ServiceRequest, Division, District, Upazila
from django_filters.rest_framework import DjangoFilterBackend
from django.template.loader import get_template
from xhtml2pdf import pisa
from rest_framework.views import APIView
from core.templatetags.customtags import uppercon
from core.utils import getRegnum, getTicketNo
# Create your views here.
class AdminViewSet(ModelViewSet):
    serializer_class = AdminSerializer
    queryset = User.objects.filter(is_superuser=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name','last_name', 'username','email']

    def list(self, request):
        queryset = User.objects.filter(is_superuser=True).exclude(pk=request.user.pk).exclude(username='superadmin')
        serializer = AdminSerializer(self.filter_queryset(queryset), many=True)
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


class CustomUserRegistraionViewSet(ModelViewSet):
    permission_classes=[IsPostOrIsAuthenticated]
    serializer_class = CustomUserRegistrationSerializer
    queryset = CustomUserRegistration.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','role', 'user__id']

    def list(self, request):
        queryset = CustomUserRegistration.objects.filter().order_by('-id')
        role = request.query_params.get('role',None)
        if role is not None:
            queryset = queryset.filter(role=role)
        serializer = CustomUserRegistrationSerializer(self.filter_queryset(queryset), many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = CustomUserRegistrationSerializer(data=data)
            
        if serializer.is_valid():
            newUser = User.objects.create_user(username = data.get('phone'), email = data.get('email'), password = data.get('password'))
            serializer.save(user = newUser, reg_no= getRegnum())
            role = data.get('role')
            notify_admins(title='New Account Created',message=f'A new "{role}" account is created. Please check it for further details.')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        previousStatus = instance.active
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        currentStatus = instance.active
        if previousStatus != currentStatus and hasattr(instance.user,'userdevicetoken'):
            if instance.user.userdevicetoken.device_token:
                send_push_message(instance.user.userdevicetoken.device_token,'Account Status',f'Hi, {instance.name} your account has been \'{"Activated" if currentStatus else "Deactivated"}\'. Please check it for further details.')
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

        
class AreaViewSet(ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['area_name',]

class ServiceRequestViewSet(ModelViewSet):
    serializer_class = ServiceRequestSerializer
    queryset = ServiceRequest.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title','servicereq_no', 'priority', 'status', 'created_at']
    filterset_fields = ['customer','technician','status' ]

    def create(self, request):
        data = request.data
        customer = CustomUserRegistration.objects.get(id=data.get('customerID'))

        serializer = ServiceRequestSerializer(data=data)
        if serializer.is_valid():
            if customer.work_area:
                technician = CustomUserRegistration.objects.filter(role='technician').filter(work_area=customer.work_area).first()
                if technician:
                    serializer.save( customer = customer, technician=technician, servicereq_no = getTicketNo())
                    if hasattr(technician.user,'userdevicetoken'):
                        if technician.user.userdevicetoken.device_token:
                            send_push_message(technician.user.userdevicetoken.device_token,'New Service Created','A new service is created and assigned to you. Please check it.')
                    notify_admins(title='New Service Created',message='A new service is created and assigned. Please check it for further details.')
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                else:
                    return Response(data={"status": "Admin doesn't assigned area to technician yet!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"status": "Admin doesn't assigned area to customer yet!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        queryset = ServiceRequest.objects.all().order_by('-id')
        exclude_status = self.request.query_params.get('exclude_status', None)
        if exclude_status is not None:
            queryset = queryset.exclude(status = exclude_status)
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        updatedStatus = uppercon(instance.status)
        if hasattr(instance.technician.user,'userdevicetoken'):
            if instance.technician.user.userdevicetoken.device_token:
                send_push_message(instance.technician.user.userdevicetoken.device_token,'Service Status Updated',f'Service of {instance.servicereq_no} status is updated to \'{updatedStatus}\'. Please check it for further details.')
        notify_admins(title='Service Status Updated',message=f'Service of {instance.servicereq_no} status is updated to \'{updatedStatus}\'. Please check it for further details.')
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class InvoiceViewSet(ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    filterset_fields = ['service__customer','service__technician','status' ]
    search_fields = ['service__id','created_at','=status','service__servicereq_no']

    def create(self, request):
        service = ServiceRequest.objects.get(id=request.data.get('serviceID'))
        serializer = InvoiceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(service = service)
            notify_admins(title='New Invoice Created',message='A new invoice is created. Please check it for further details.')
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TransactionView(APIView):
    
    def get(self, request, format=None):
        total = request.query_params.get('total',None)
        if total == 'pd':
            return Response(get_mdod(request))
        return Response({})


def render_pdf_view(request,pk):
    template_path = 'inv.html'
    obj = get_object_or_404(Invoice,pk=pk)
    context = {
        # 'domain':'127.0.0.1:8000',
        'domain':'efixbd.com',
        'protocol': 'https',
        # 'protocol': 'http',
        'id':obj.id,
        'date':obj.created_at,
        'parts_charge':obj.equip_charge,
        'parts_details':obj.details,
        'tech_charge':obj.tech_charge,
        'document':obj.files,
    }

    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"invoice-{pk}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return None


class DivisionViewSet(ModelViewSet):
    serializer_class = DivisionSerializer
    queryset = Division.objects.all()

class DistrictViewSet(ModelViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['division__name',]

class UpazilaViewSet(ModelViewSet):
    serializer_class = UpazilaSerializer
    queryset = Upazila.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['district__name',]

class NotificationTokenViewSet(ModelViewSet):
    serializer_class = NotificationTokenSerializer
    queryset = NotificationToken.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['user',]

    def create(self, request):
        serializer = NotificationTokenSerializer(data=request.data)
        deviceToken = request.data.get('device_token',None)
        existingTokenqs = NotificationToken.objects.filter(device_token=deviceToken)
        if existingTokenqs:
            for tokenObj in existingTokenqs:
                tokenObj.device_token = None
                tokenObj.save()
                
        if serializer.is_valid():
            if hasattr(request.user,'userdevicetoken'):
                userdevicetoken =  request.user.userdevicetoken
                userdevicetoken.device_token = deviceToken
                userdevicetoken.save()
            else:
                serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)