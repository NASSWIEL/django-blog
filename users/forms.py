from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta: 
        model = User 
        fields = ['username','email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password to change'
        }),
        required=False,
        help_text="Leave blank if you don't want to change your password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New password'
        }),
        required=False,
        label='New password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        required=False,
        label='Confirm new password'
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        # If any password field is filled, all must be filled
        if any([current_password, new_password1, new_password2]):
            if not all([current_password, new_password1, new_password2]):
                raise forms.ValidationError("To change password, all password fields must be filled.")
            
            # Verify current password
            if not authenticate(username=self.instance.username, password=current_password):
                raise forms.ValidationError("Current password is incorrect.")
            
            # Check if new passwords match
            if new_password1 != new_password2:
                raise forms.ValidationError("New passwords don't match.")
            
            # Check password length
            if len(new_password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get('new_password1')
        
        if new_password1:
            user.set_password(new_password1)
        
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


