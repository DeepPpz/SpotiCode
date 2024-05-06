from django import forms
from django.urls import reverse_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    domain_name = forms.CharField(label='Domain Name')
    
    error_messages = {
        'duplicate_user': _('Such person already exists. Try adding middle name.'),
        'password_mismatch': _('You may have missed a button or two - passwords don\'t match.'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].help_text = 'Password is a combination of all lower domain_name and current year.'

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        username = f'{first_name[0].lower()}.{last_name.lower()}'
        
        if User.objects.filter(username=username).exists():
            username = f'{first_name.lower().replace(" ", ".")}.{last_name.lower()}'
  
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['duplicate_user'], code='duplicate_user')
        
        email = f'{username}@{self.cleaned_data.get("domain_name")}'
        
        self.cleaned_data['username'] = username
        self.cleaned_data['email'] = email
                
        return cleaned_data
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'domain_name')


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control mb-4'})
        self.fields['old_password'].help_text = ''
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control mb-4'})
