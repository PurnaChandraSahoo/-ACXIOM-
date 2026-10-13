import json
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from .models import Customer, Lead, Opportunity, FollowUp, Activity, AuditLog
from .forms import CustomerForm, LeadForm, OpportunityForm, FollowUpForm, ActivityForm

MODULES = {
    "customers": (Customer, CustomerForm, "Customers"),
    "leads": (Lead, LeadForm, "Leads"),
    "opportunities": (Opportunity, OpportunityForm, "Opportunities"),
    "followups": (FollowUp, FollowUpForm, "Follow-ups"),
    "activities": (Activity, ActivityForm, "Activities"),
}
@login_required
def dashboard(request):
    qs = Opportunity.objects.all()
    context = {
        "customers_count": Customer.objects.count(),
        "leads_count": Lead.objects.count(),
        "open_opportunities": qs.exclude(stage__in=["Won","Lost"]).count(),
        "won_count": qs.filter(stage="Won").count(),
        "lost_count": qs.filter(stage="Lost").count(),
        "pipeline_value": sum((o.amount for o in qs.exclude(stage__in=["Won","Lost"])), 0),
        "recent_customers": Customer.objects.all()[:5],
        "lead_labels": json.dumps([x[0] for x in Lead.STATUSES]),
        "lead_values": json.dumps([Lead.objects.filter(status=x[0]).count() for x in Lead.STATUSES]),
        "stage_labels": json.dumps([x[0] for x in Opportunity.STAGES]),
        "stage_values": json.dumps([Opportunity.objects.filter(stage=x[0]).count() for x in Opportunity.STAGES]),
    }
    return render(request, "crm/dashboard.html", context)

@login_required
def module_list(request, module):
    if module not in MODULES: return redirect("dashboard")
    model, form_class, title = MODULES[module]
    query = request.GET.get("q", "").strip()
    qs = model.objects.all()
    if query:
        fields = [f.name for f in model._meta.fields if isinstance(f, ( __import__('django.db.models', fromlist=['CharField']).CharField, __import__('django.db.models', fromlist=['EmailField']).EmailField))]
        from django.db.models import Q
        condition = Q()
        for field in fields: condition |= Q(**{f"{field}__icontains": query})
        qs = qs.filter(condition) if fields else qs
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        if hasattr(obj, "owner") and not obj.owner_id: obj.owner = request.user
        if hasattr(obj, "assigned_to") and not obj.assigned_to_id: obj.assigned_to = request.user
        obj.save()
        AuditLog.objects.create(user=request.user, action="CREATE", entity_name=model.__name__, record_id=obj.pk, details=f"Created {obj}")
        messages.success(request, f"{title[:-1] if title.endswith('s') else title} saved successfully.")
        return redirect("module_list", module=module)
    return render(request, "crm/module_list.html", {"title":title,"module":module,"items":qs[:100],"columns":model._meta.fields,"form":form,"query":query})

@login_required
def audit_log(request):
    return render(request, "crm/audit.html", {"items": AuditLog.objects.select_related("user")[:100]})

def login_page(request):
    from django.contrib.auth.views import LoginView
    return LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True)(request)

@login_required
def logout_page(request):
    logout(request)
    return redirect("login")

def serialize(obj, fields):
    data = {}
    for field in fields:
        value = getattr(obj, field)
        if hasattr(value, "isoformat"): value = value.isoformat()
        data[field] = value
    return data

@require_GET
@login_required
def api_customers(request):
    return JsonResponse({"results":[{"id":x.id,"name":x.name,"email":x.email,"phone":x.phone,"company":x.company,"status":x.status} for x in Customer.objects.all()]})
@require_GET
@login_required
def api_leads(request):
    return JsonResponse({"results":[{"id":x.id,"name":x.name,"email":x.email,"status":x.status,"source":x.source,"expected_value":str(x.expected_value)} for x in Lead.objects.all()]})
@require_GET
@login_required
def api_opportunities(request):
    return JsonResponse({"results":[{"id":x.id,"name":x.name,"amount":str(x.amount),"probability":x.probability,"stage":x.stage,"expected_close_date":x.expected_close_date.isoformat()} for x in Opportunity.objects.all()]})
