from django import forms
from .models import ClaimRequest


class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = [
            "insurance_company",
            "vehicle_details",
            "vehicle_number",
            "accident_date",
            "accident_image",
        ]
        widgets = {
            "accident_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select,)):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"