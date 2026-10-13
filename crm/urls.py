from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("customers/", views.module_list, {"module":"customers"}, name="customers"),
    path("leads/", views.module_list, {"module":"leads"}, name="leads"),
    path("opportunities/", views.module_list, {"module":"opportunities"}, name="opportunities"),
    path("followups/", views.module_list, {"module":"followups"}, name="followups"),
    path("activities/", views.module_list, {"module":"activities"}, name="activities"),
    path("audit/", views.audit_log, name="audit"),
    path("api/customers/", views.api_customers, name="api_customers"),
    path("api/leads/", views.api_leads, name="api_leads"),
    path("api/opportunities/", views.api_opportunities, name="api_opportunities"),
]
