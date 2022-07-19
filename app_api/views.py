from io import BytesIO
from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from app_api.serializers import  *
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.custom_context_processor import get_mdod
from core.models import Area, CustomUserRegistration, Invoice, ServiceRequest, Division, District, Upazila
from django_filters.rest_framework import DjangoFilterBackend
from django.template.loader import get_template
from xhtml2pdf import pisa
from rest_framework.views import APIView
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


class CustomerRegistraionViewSet(ModelViewSet):
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AreaViewSet(ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['area_name',]

class ServiceRequestViewSet(ModelViewSet):
    serializer_class = ServiceRequestSerializer
    queryset = ServiceRequest.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,]
    search_fields = ['title', 'priority', 'status', 'created_at']
    filterset_fields = ['customer', ]
    
    def create(self, request):
        data = request.data
        customer = CustomUserRegistration.objects.get(id=data.get('customerID'))
        serializer = ServiceRequestSerializer(data=data)

        if serializer.is_valid():
            serializer.save( customer = customer, servicereq_no = getTicketNo())

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class InvoiceViewSet(ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['service__id','status',]
    # parser_classes = [FormParser,MultiPartParser]
    def create(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class TransactionView(APIView):
    
    def get(self, request, format=None):
        due = request.query_params.get('due',None)
        if due == 'total':
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
        filename = f"Invoice_{pk}.pdf"
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