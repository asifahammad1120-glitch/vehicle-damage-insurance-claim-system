from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CompanyProfile


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(max_length=200)
    license_number = forms.CharField(max_length=100)
    mobile_number = forms.CharField(max_length=15)
    city = forms.CharField(max_length=100)
    office_address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            CompanyProfile.objects.create(
                user=user,
                company_name=self.cleaned_data["company_name"],
                license_number=self.cleaned_data["license_number"],
                mobile_number=self.cleaned_data["mobile_number"],
                city=self.cleaned_data["city"],
                office_address=self.cleaned_data["office_address"],
                status="pending",
            )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select,)):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"