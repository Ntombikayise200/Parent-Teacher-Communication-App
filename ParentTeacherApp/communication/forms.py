from mailbox import Message
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ProgressReport  # Ensure your Profile model is imported

class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'NAME'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'PHONE NUMBER'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'EMAIL ADDRESS'}))

    PROVINCE_CHOICES = [
        ('', 'Select Province'),
        ('GP', 'Gauteng'),
        ('WC', 'Western Cape'),
        ('KZN', 'KwaZulu-Natal'),
        ('EC', 'Eastern Cape'),
        ('FS', 'Free State'),
        ('LIM', 'Limpopo'),
        ('NW', 'North West'),
        ('MP', 'Mpumalanga'),
        ('NC', 'Northern Cape'),
    ]
    province = forms.ChoiceField(choices=PROVINCE_CHOICES, required=True)
    school_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'SCHOOL NAME'}))
    gender = forms.ChoiceField(choices=[('male', 'MALE'), ('female', 'FEMALE'), ('non-binary', 'NON-BINARY')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Password fields from UserCreationForm
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'USERNAME'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'PASSWORD'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'CONFIRM PASSWORD'}),
        }

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()

        # Save additional fields in the Profile model
        Profile.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            phone_number=self.cleaned_data['phone_number'],
            province=self.cleaned_data['province'],
            school_name=self.cleaned_data['school_name'],
            gender=self.cleaned_data['gender']
        )

        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ['report']
