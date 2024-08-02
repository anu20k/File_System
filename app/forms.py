from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import UploadedFile, Category

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))




class UploadedFileForm(forms.ModelForm):
    
    
    
    
    class Meta:
        model = UploadedFile
        fields = ['category','user_id','uploaded_on']
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")
