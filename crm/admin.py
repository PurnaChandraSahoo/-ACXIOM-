from django.contrib import admin
from .models import Customer, Lead, Opportunity, FollowUp, Activity, AuditLog
admin.site.register([Customer, Lead, Opportunity, FollowUp, Activity, AuditLog])
