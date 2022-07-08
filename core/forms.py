from django import forms
from django.forms import fields, widgets
from .models import *

class CustomUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUserRegistration
        fields = [
            'name',
            'email',
            'phone',
            ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input--style-5'}),
            'email': forms.EmailInput(attrs={'class': 'input--style-5'}),
            'phone': forms.TextInput(attrs={'class': 'input--style-5'}),
        }

class CustomUserRegistrationUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUserRegistration
        fields = [
            'name',
            'email',
            'phone',
            'other_phone',
            'registration_type',
            'business_name',
            'post_office_or_union',
            'house_info',
            'nid',
            'picture'
            ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input--style-5'}),
            'email': forms.EmailInput(attrs={'class': 'input--style-5'}),
            'phone': forms.TextInput(attrs={'class': 'input--style-5'}),
            'other_phone': forms.TextInput(attrs={'class': 'input--style-5'}),
            'registration_type': forms.Select(attrs={'class': 'reg_type'}),
            'business_name': forms.TextInput(attrs={'class': 'input--style-5'}),
            'post_office_or_union': forms.TextInput(attrs={'class': 'input--style-5'}),
            'house_info': forms.TextInput(attrs={'class': 'input--style-5'}),
            'nid': forms.TextInput(attrs={'class': 'input--style-5'}),
        }

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'details', 'priority', 'files']

        widgets = {
                'title': forms.TextInput(attrs={'class': 'input--style-5'}),
                'details': forms.Textarea(attrs={'class': 'input--style-5', 'rows': '4', 'cols': '40'}),
                'priority': forms.Select(attrs={'class': 'priority-select'}),
                'files': forms.FileInput(attrs={'accept': '.pdf, .jpg, .jpeg, .png, .doc, .docx, .xls, .xlsx, .txt'}),
            }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['tech_charge', 'details', 'equip_charge', 'files']

        widgets = {
                'tech_charge': forms.NumberInput(attrs={'class': 'input--style-5', 'placeholder': 'Enter your charge...'}),
                'details': forms.Textarea(attrs={'class': 'input--style-5', 'rows': '4', 'placeholder': 'Write about equivment/parts details...'}),
                'equip_charge': forms.NumberInput(attrs={'class': 'input--style-5', 'placeholder': 'Enter equipment/parts charge...'}),
                'files': forms.FileInput(attrs={'accept': '.pdf, .jpg, .jpeg, .png, .doc, .docx, .xls, .xlsx, .txt'}),
            }