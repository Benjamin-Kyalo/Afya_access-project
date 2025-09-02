# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PractitionerProfile

class PractitionerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    id_number = forms.CharField(required=True, max_length=50)
    designation = forms.ChoiceField(choices=PractitionerProfile.Designation.choices, required=True)
    service_location = forms.CharField(required=True, max_length=120)
    phone_number = forms.CharField(required=True, max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'id_number', 'designation', 'service_location', 'phone_number',
                  'password1', 'password2')

    def save(self, commit=True):
        # create the user but keep them inactive (pending approval)
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()
            # populate profile created by signal
            profile = user.practitionerprofile
            profile.id_number = self.cleaned_data['id_number']
            profile.designation = self.cleaned_data['designation']
            profile.service_location = self.cleaned_data['service_location']
            profile.phone_number = self.cleaned_data['phone_number']
            profile.save()
        return user
