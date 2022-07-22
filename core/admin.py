from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from .models import *
from .utils import confirmMail, paymentStatusMail,technicianAssignMail,serviceStatusMail

# Register your models here.
admin.site.register(Country)
admin.site.register(Division)
admin.site.register(District)
admin.site.register(Upazila)
admin.site.register(NotificationToken)


class CustomUserRegistrationAdmin(admin.ModelAdmin):
    list_filter = ('role','active','registration_type',)
    list_display = ('name','phone','email','role','active')
    search_fields = ['phone','role','name','email','reg_no',]
    # def save_model(self, request, obj, form, change):
    #     if obj.active and ('active' in form.changed_data):
    #         confirmMail(obj)
    #     super(CustomUserRegistrationAdmin, self).save_model(request, obj, form, change)

admin.site.register(CustomUserRegistration, CustomUserRegistrationAdmin)


class ServiceRequestAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceRequestAdminForm, self).__init__(*args, **kwargs)
        self.fields['technician'].queryset = CustomUserRegistration.objects.filter(role='technician')


class ServiceRequestAdmin(admin.ModelAdmin):
    form = ServiceRequestAdminForm
    # readonly_fields=('customer', )
    list_filter = ('priority', 'status',)
    list_display = ('servicereq_no','title', 'get_customer_name','get_customer_phone','get_customer_email','get_tech_name','status','update_status',)
    list_editable = ('status',)
    search_fields = ['title','customer__phone','servicereq_no',]
    change_list_template = 'custom_change_list/custom_service_change_list.html'
    def get_tech_name(self,obj):
        return obj
    get_tech_name.admin_order_field = 'technicain__name'
    get_tech_name.short_description = 'Technician Name'

    def get_customer_name(self,obj):
        return obj.customer.name
    get_customer_name.admin_order_field = 'customer__name'
    get_customer_name.short_description = 'Customer Name'

    def get_customer_phone(self,obj):
        return obj.customer.phone
    get_customer_phone.admin_order_field = 'customer__phone'
    get_customer_phone.short_description = 'Customer Phone'

    def get_customer_email(self,obj):
        return obj.customer.email
    get_customer_email.admin_order_field = 'customer__email'
    get_customer_email.short_description = 'Customer Email'


    def update_status(self, obj):
        return format_html('<input type="submit" name="_save" class="default update__status" value="Save">')
    update_status.short_description = "update"

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.technician:
            serviceStatusMail(obj)
        if obj.technician and ('technician' in form.changed_data):
            technicianAssignMail(obj)
        super(ServiceRequestAdmin, self).save_model(request, obj, form, change)

admin.site.register(ServiceRequest,ServiceRequestAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('id','get_servicereq_no','get_service_title','status', 'get_customer_name', 'get_customer_phone', 'get_customer_email','get_technician_name','created_at')
    list_editable = ('status',)
    change_list_template = 'custom_change_list/custom_invoice_change_list.html'

    def get_servicereq_no(self,obj):
        return obj.service.servicereq_no
    get_servicereq_no.admin_order_field = 'service__servicereq_no'
    get_servicereq_no.short_description = 'Service No'

    def get_customer_name(self,obj):
        return obj.service.customer.name
    get_customer_name.admin_order_field = 'service__customer__name'
    get_customer_name.short_description = 'Customer Name'

    def get_customer_phone(self,obj):
        return obj.service.customer.phone
    get_customer_phone.admin_order_field = 'service__customer__phone'
    get_customer_phone.short_description = 'Customer Phone'

    def get_customer_email(self,obj):
        return obj.service.customer.email
    get_customer_email.admin_order_field = 'service__customer__email'
    get_customer_email.short_description = 'Customer Email'

    def get_service_title(self,obj):
        return obj.service.title
    get_service_title.admin_order_field = 'service__title'
    get_service_title.short_description = 'Service'

    def get_technician_name(self,obj):
        return obj.service.technician.name
    # get_technician_name.admin_order_field = 'service__title'
    get_technician_name.short_description = 'Technician'

    # def save_model(self, request, obj, form, change):
    #     if ('status' in form.changed_data) and (obj.status == 'Paid'):
    #         paymentStatusMail(obj)
    #     super(InvoiceAdmin, self).save_model(request, obj, form, change)


admin.site.register(Invoice, InvoiceAdmin)

admin.site.site_header = 'E-Fix'