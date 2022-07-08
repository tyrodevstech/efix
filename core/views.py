from django.shortcuts import redirect, render
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from .utils import getRegnum,getTicketNo, serviceInvoiceMail, serviceStatusMail

from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError,EmailMessage
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from .decorators import *

# Create your views here.
@user_is_admin
def login_view(request):
    if request.user.is_authenticated:        
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username =  request.POST.get('username')
            password =  request.POST.get('password')
            userObject = User.objects.filter(email = username).last()
            if userObject:
                username = userObject.username
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request,"Email / Phone or Password didn't match. Please try again!")
    return render(request, 'login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@user_is_admin
def dashboard_view(request):
    if hasattr(request.user, 'customuserregistration'):
        if request.user.customuserregistration.active:
            remaining = 0
            completed = 0
            totalService = 0
            tech_total_charge=0
            equip_total_charge=0
            if request.user.customuserregistration.role == 'customer':
                totalService = ServiceRequest.objects.filter(customer = request.user).count()
                currentUser = 'customer'
            elif request.user.customuserregistration.role == 'technician':
                remaining = ServiceRequest.objects.filter(Q(technician = request.user.customuserregistration)).exclude(status = 'closed').count()
                completed = ServiceRequest.objects.filter(Q(technician = request.user.customuserregistration)&Q(status='closed')).count()
                invoiceListtech = Invoice.objects.filter(service__technician=request.user.customuserregistration)
                for i in invoiceListtech:
                    tech_total_charge += i.tech_charge
                    equip_total_charge += i.equip_charge
                currentUser = 'technician'

            invoiceList = Invoice.objects.filter(service__customer=request.user)
            totalDue=0
            
            for i in invoiceList:
                if i.status == 'Unpaid':
                    totalDue += (i.tech_charge + i.equip_charge)
            Due=False
            if totalDue > 0:
                Due=True
            
            context = {
                'total':totalDue,
                'dueStatus': Due,
                'tech_total_charge':tech_total_charge,
                'equip_total_charge':equip_total_charge,
                'totalService':totalService,
                'remaining':remaining,
                'completed':completed,
                'currentUser':currentUser,
            }
            return render(request, 'dashboard.html', context)
        else:
            return render(request, 'comfirm_account.html')
    else:
        raise Http404


@login_required(login_url='login')
@user_is_admin
def updateProfile_view(request, pk):
    customer_info = customerRegistration.objects.get(id=pk)
    form = customerRegistrationUpdateForm(instance= customer_info)
    if request.method == 'POST':
        form = customerRegistrationUpdateForm(request.POST,request.FILES, instance= customer_info)
        if form.is_valid():
            user = User.objects.get(id = request.user.id)
            user.email = request.POST.get('email')
            user.save()
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.country=request.POST.get('country')
            new_form.division=request.POST.get('division')
            new_form.district=request.POST.get('district')
            new_form.upazila=request.POST.get('upazila')
            new_form.save()
            messages.success(request, 'Your information has been updated!')
            return redirect('updateProfile', pk)
    divisions = Division.objects.all()
    context = {
        'divisions':divisions,
        'form' : form,
        'customer_info':customer_info
    }
    return render(request, 'update_info.html',context)



@login_required(login_url='login')
@user_is_admin
def changePassword_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changePassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



def registration_view(request):
    form = customerRegistrationForm()
    userform = UserCreationForm()
    if request.method == 'POST':
        form = customerRegistrationForm(request.POST,request.FILES)
        updated_request = request.POST.copy()
        updated_request['username']= request.POST.get('phone')
        userform = UserCreationForm(updated_request)

        if form.is_valid() and userform.is_valid():
            new_userform=userform.save(commit=False)
            new_userform.email = request.POST.get('email')
            new_userform.save()

            new_form = form.save(commit=False)
            new_form.user = new_userform
            new_form.reg_no = getRegnum()
            new_form.save()
            messages.success(request, 'Account Created successfully !')
            return redirect('login')
    divisions = Division.objects.all()
    context = {
        'divisions':divisions,
        'form' : form,
        'userform':userform
    }
    return render(request, 'registration.html',context)



def getDistrict_view(request):
    divisionName = request.POST.get('division')
    districts = District.objects.filter(division__name = divisionName)
    districtsList = list(districts.values())
    return JsonResponse({'districtsList':districtsList})



def getUpazila_view(request):
    districtName = request.POST.get('district')
    upazilas = Upazila.objects.filter(district__name = districtName)
    upazilaList = list(upazilas.values())
    return JsonResponse({'upazilaList':upazilaList})



def getEmail_view(request):
    emailName = request.POST.get('emailName')
    Customerinfo = customerRegistration.objects.filter(email__icontains = emailName)
    if Customerinfo.count() > 0:
        return JsonResponse({'status' : 1})
    else:
        return JsonResponse({'status' : 0})



def getPhone_view(request):
    phoneNum = request.POST.get('phoneNum')
    Customerinfo = customerRegistration.objects.filter(phone__icontains = phoneNum)
    if Customerinfo.count() > 0:
        return JsonResponse({'status' : 1})
    else:
        return JsonResponse({'status' : 0})



def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    c = {
                        "email":user.email,
                        # 'domain':'127.0.0.1:8000',
                        'domain':'efixbd.com',
                        'site_name': 'E-Fix',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                        # 'protocol': 'http',
                        }
                    html_version = 'password_reset/password_reset_email.html'
                    html_message = render_to_string(html_version,c)
                    try:
                        message = EmailMessage(subject, html_message, settings.DEFAULT_FROM_EMAIL,[user.email])
                        message.content_subtype = 'html'
                        message.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect ("password_reset_done")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset/password_reset.html", context={"password_reset_form":password_reset_form})


@login_required(login_url='login')
@user_is_admin
@user_is_customer
def create_service_view(request):
    form = ServiceRequestForm()
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.customer = request.user
            newform.servicereq_no = getTicketNo()
            newform.save()
            messages.success(request, 'Your requested service has been created!')
            return redirect('create_service')
    context ={
        'form': form
    }

    return render(request, 'create_service.html', context)

@login_required(login_url='login')
@user_is_admin
@user_is_customer
def service_request_list_view(request):
    service_list = ServiceRequest.objects.filter(customer = request.user)
    context ={
        'service_list': service_list 
        }
    return render(request, 'service_request_list.html', context)

@login_required(login_url='login')
@user_is_admin
@user_is_technician
def work_request_list_view(request):
    work_list = ServiceRequest.objects.filter(technician = request.user.customuserregistration).order_by('-created_at')

    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        service_id = request.POST.get('service_id')
        curr_status = request.POST.get('curr_status')
        service_obj = ServiceRequest.objects.get(id = service_id)

        if service_obj and curr_status and service_obj.status != curr_status:
            service_obj.status = curr_status
            service_obj.save()
            if form.is_valid():
                newform = form.save(commit=False)
                newform.service =  service_obj
                newform.save()
                serviceStatusMail(service_obj)
                serviceInvoiceMail(newform)
                messages.success(request, 'Your requested service has been created!')
                return redirect('work_request_list')
        else:
            messages.success(request,'No changes Detected')
    context ={
        'work_list': work_list,
        }
    return render(request, 'work_request_list.html', context)


@login_required(login_url='login')
@user_is_admin
@user_is_technician
def satusUpdate(request):
    status = request.GET.get('status')
    id = request.GET.get('id')
    service_obj = ServiceRequest.objects.get(id = id)

    if service_obj.status == status:
        return JsonResponse({'status' : 'null', 'service_no': service_obj.servicereq_no })
    elif service_obj and status and service_obj.status != status:
        service_obj.status = status
        service_obj.save()
        serviceStatusMail(service_obj)
        return JsonResponse({'status' : 1, 'service_no': service_obj.servicereq_no })
    else:
        return JsonResponse({'status' : 0})

@login_required(login_url='login')
@user_is_admin
@user_is_technician
def details_service_view(request, pk):
    details = ServiceRequest.objects.get(id = pk)
    context ={
        'obj': details
    }

    return render(request, 'details_service.html', context)






@login_required(login_url='login')
def admin_invoice_view(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        service_id = request.POST.get('service_id')
        curr_status = request.POST.get('curr_status')
        service_obj = ServiceRequest.objects.get(id = service_id)
        if service_obj and curr_status and service_obj.status != curr_status:
            service_obj.status = curr_status
            service_obj.save()
            if form.is_valid():
                newform = form.save(commit=False)
                newform.service =  service_obj
                newform.save()
                serviceStatusMail(service_obj)
                serviceInvoiceMail(newform)
                messages.success(request, '1 service request was changed successfully.')
        else:
            messages.success(request,'No changes Detected')

    return redirect('/admin/core/servicerequest/')


# @login_required(login_url='login')
def admin_servicelist_view(request):
    technician_id = request.POST.get('technician_id')
    servicelist = ServiceRequest.objects.filter(technician__id = technician_id)

    print(technician_id)
    print(servicelist)
    context = {
        'servicelist':list(servicelist.values()),
    }
    return JsonResponse(context,safe=False)



@login_required(login_url='login')
def get_technician_work_list(request):
    technicianList = customerRegistration.objects.filter(role = 'technician' )
    technician_id = request.POST.get('technician_id')
    if technician_id:
        technician_id =  int(technician_id)
    servicelist = ServiceRequest.objects.filter(technician__id = technician_id)
    context = {
        'technicianList':technicianList,
        'servicelist':servicelist,
        'technician_id':technician_id,
    }
    return render(request,'technician_work_list.html',context)




# custom error handling page
def custom_page_not_found_view(request, exception=None):
    return render(request, "custom-error-page/404.html", {})