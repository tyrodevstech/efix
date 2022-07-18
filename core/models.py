from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Area(models.Model):
    area_name = models.CharField(max_length=255, null=True)
    def __str__(self):
        return f'{self.area_name}'


class CustomUserRegistration(models.Model):
    registrationType = (
        ('','Please Select'),
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Other', 'Other')
    )

    roleType = (
        ('customer', 'customer'),
        ('admin', 'admin'),
        ('technician', 'technician'),
    )
# ,related_name='custuserreg'
    user = models.OneToOneField(User, on_delete =models.CASCADE, null=True)
    reg_no = models.BigIntegerField(null=True)
    name = models.CharField(max_length=122, null=True)
    email = models.EmailField(max_length=122, null=True , blank=True)
    phone = models.CharField(max_length=122, null=True)
    other_phone = models.CharField(max_length=122, null=True, blank=True)
    registration_type = models.CharField(max_length=122, choices = registrationType ,null=True, blank=True)
    role = models.CharField(max_length=122, choices = roleType ,null=True, default=roleType[0][0])
    business_name = models.CharField(max_length=122, null=True, blank=True)
    country = models.CharField(max_length=122, null=True, blank=True)
    division = models.CharField(max_length=122, null=True, blank=True)
    district = models.CharField(max_length=122, null=True, blank=True)
    upazila = models.CharField(max_length=122, null=True, blank=True)
    post_office_or_union = models.CharField(max_length=122, null=True, blank=True)
    house_info = models.CharField(max_length=122, null=True, blank=True)
    work_area = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True)
    nid = models.CharField(max_length=122, null=True, blank=True)
    picture = models.ImageField(upload_to= 'image', null=True, blank=True)
    active = models.BooleanField(default=False,null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    priority_choice  = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    )
    STATUS_CHOICE = (
        ('new','New'),
        ('in_progress','In Progress'),
        ('waittingoncustomer','Waitting on Customer'),
        ('fixed','Fixed'),
        ('closed','Closed'),
        ('cancelled','Cancelled'),
    )
    customer = models.ForeignKey(CustomUserRegistration, on_delete=models.SET_NULL, null=True,related_name='customerrs',blank=True)
    technician = models.ForeignKey(CustomUserRegistration, on_delete=models.SET_NULL, null=True,related_name='technicianrs',blank=True)
    servicereq_no = models.CharField(max_length=122, null=True)
    title = models.CharField(max_length=250, null=True)
    details = models.TextField(max_length=1000, null=True)
    files = models.FileField(upload_to= 'service_file', null=True, blank=True)
    priority = models.CharField(max_length=122, choices=priority_choice, null=True)
    created_at = models.DateField(auto_now_add=True)
    status =  models.CharField(max_length=122, choices=STATUS_CHOICE, null=True,blank=True,default='new')
    
    def __str__(self):
        return f'{self.title}'


class Invoice(models.Model):
    PAYMENT_STATUS = (
        ('Paid','Paid'),
        ('Unpaid','Unpaid'),
    )
    service = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True)
    tech_charge = models.FloatField(max_length=250, null=True)
    details = models.TextField(max_length=1000, null=True)
    equip_charge = models.FloatField(max_length=250, null=True, blank=True)
    files = models.FileField(upload_to= 'invoice_file', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    status =  models.CharField(max_length=122, choices=PAYMENT_STATUS, null=True,blank=True,default='Unpaid')
    
    def __str__(self):
        return f'#{self.id}-Invoice-{self.service.title}'


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Division(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class District(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Upazila(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
