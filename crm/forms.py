from django import forms
from django.utils import timezone
from .models import Customer, Lead, Opportunity, FollowUp, Activity

class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
            if isinstance(field.widget, forms.DateInput):
                field.widget.attrs["type"] = "date"

class CustomerForm(StyledModelForm):
    class Meta:
        model = Customer
        fields = ["name","email","phone","company","address","city","status"]
        widgets = {"address": forms.TextInput()}
class LeadForm(StyledModelForm):
    class Meta:
        model = Lead
        fields = ["name","email","phone","company","source","status","expected_value"]
class OpportunityForm(StyledModelForm):
    class Meta:
        model = Opportunity
        fields = ["name","customer","amount","probability","stage","expected_close_date"]
        widgets = {"expected_close_date": forms.DateInput()}
class FollowUpForm(StyledModelForm):
    class Meta:
        model = FollowUp
        fields = ["subject","customer","lead","follow_up_date","follow_up_type","status","remarks"]
        widgets = {"follow_up_date": forms.DateInput()}
class ActivityForm(StyledModelForm):
    class Meta:
        model = Activity
        fields = ["activity_type","subject","description","activity_date","customer","lead","status"]
        widgets = {"activity_date": forms.DateInput()}
