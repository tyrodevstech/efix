from datetime import datetime, timedelta
from django.http import HttpResponse
from .models import CustomUserRegistration,ServiceRequest
from django.conf import settings
from django.core.mail import send_mail, EmailMessage,BadHeaderError
from django.template.loader import render_to_string

def getTicketNo():
    snum = 100001
    obj = ServiceRequest.objects.last()
    if obj and obj.servicereq_no:
        last_t_no = obj.servicereq_no.replace('#', '')
        t_no = int(last_t_no)+1
    else:
        t_no=snum
    return f'#{t_no}'


def getRegnum():
    snum = 100001
    obj = CustomUserRegistration.objects.last()
    if obj:
        rnumber = obj.reg_no+1
    else:
        rnumber=snum
    return rnumber


def confirmMail(obj):
    subject = 'Account Activation'
    message = f'Hi {obj.name}, Your E-Fix account has been activated. You can got to https://efixbd.com and use your account now. Thank you.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [obj.email, ]
    send_mail( subject, message, email_from, recipient_list )


def technicianAssignMail(obj):
    subject = 'New Work Assingment'
    c = {
        'service_no':obj.servicereq_no,
        'service_title':obj.title,
        'customer_name':obj.customer.customuserregistration.name,
        'customer_phone':obj.customer.customuserregistration.phone,
        'customer_email':obj.customer.customuserregistration.email,
        'technician_name':obj.technician.name,
    }
    text_version = 'service_assigned.txt'
    text_message = render_to_string(text_version,c)

    try:
        send_mail(subject, text_message, settings.DEFAULT_FROM_EMAIL,[obj.technician.email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def serviceStatusMail(obj):
    subject = f"{obj.servicereq_no} {obj.title}"
    c = {
        'customer_name':obj.customer.customuserregistration.name,
        'status':obj.status,
        'technician_name':obj.technician.name,
        'technician_phone':obj.technician.phone,
        'technician_email':obj.technician.email,
    }
    text_version = 'service_request_status.txt'
    text_message = render_to_string(text_version,c)
    try:
        send_mail(subject, text_message, settings.DEFAULT_FROM_EMAIL,[obj.customer.customuserregistration.email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def serviceInvoiceMail(obj):
    subject = f'Invoice for {obj.service.servicereq_no}-{obj.service.title}'
    c = {
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
    html_version = 'invoice.html'
    html_template = render_to_string(html_version,c)
    try:
        message = EmailMessage(subject, html_template, settings.DEFAULT_FROM_EMAIL,[obj.service.customer.customuserregistration.email])
        message.content_subtype = 'html'
        message.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def paymentStatusMail(obj):
    subject = f"Invoice#{obj.id}-Service{obj.service.servicereq_no}-{obj.service.title}"
    c = {
        'customer_name':obj.service.customer.customuserregistration.name,
        'status':obj.status,
    }
    text_version = 'payment_status.txt'
    text_message = render_to_string(text_version,c)
    try:
        send_mail(subject, text_message, settings.DEFAULT_FROM_EMAIL,[obj.service.customer.customuserregistration.email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')









def get_months():
    date_today = datetime.today()
    month_fday = date_today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = date_today.replace(day=28) + timedelta(days=4)
    month_lday = next_month - timedelta(days = next_month.day)
    return month_fday,month_lday