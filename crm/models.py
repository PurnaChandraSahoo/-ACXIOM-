from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone

phone_validator = RegexValidator(r"^\+?[0-9\s\-]{10,15}$", "Enter a valid phone number.")

class Customer(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, unique=True, validators=[phone_validator])
    company = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, choices=[("Active","Active"),("Inactive","Inactive")], default="Active")
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
    class Meta: ordering = ["-created_at"]

class Lead(models.Model):
    STATUSES = [("New","New"),("Contacted","Contacted"),("Qualified","Qualified"),("Lost","Lost"),("Converted","Converted")]
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=16, validators=[phone_validator])
    company = models.CharField(max_length=120, blank=True)
    source = models.CharField(max_length=60, default="Website")
    status = models.CharField(max_length=20, choices=STATUSES, default="New")
    expected_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
    class Meta: ordering = ["-created_at"]

class Opportunity(models.Model):
    STAGES = [("Qualification","Qualification"),("Proposal","Proposal"),("Negotiation","Negotiation"),("Won","Won"),("Lost","Lost")]
    name = models.CharField(max_length=150)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    probability = models.PositiveSmallIntegerField(default=25, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stage = models.CharField(max_length=20, choices=STAGES, default="Qualification")
    expected_close_date = models.DateField()
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.stage not in ("Won", "Lost") and self.expected_close_date and self.expected_close_date < timezone.localdate():
            raise ValidationError({"expected_close_date": "Expected Close Date cannot be in the past."})
    @property
    def weighted_value(self): return self.amount * self.probability / 100
    def __str__(self): return self.name
    class Meta: ordering = ["-created_at"]

class FollowUp(models.Model):
    TYPES = [("Call","Call"),("Meeting","Meeting"),("Email","Email"),("Task","Task")]
    STATUSES = [("Planned","Planned"),("Completed","Completed"),("Missed","Missed"),("Cancelled","Cancelled")]
    subject = models.CharField(max_length=150)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, null=True, blank=True, on_delete=models.CASCADE)
    follow_up_date = models.DateField()
    follow_up_type = models.CharField(max_length=20, choices=TYPES, default="Call")
    status = models.CharField(max_length=20, choices=STATUSES, default="Planned")
    remarks = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.status == "Planned" and self.follow_up_date and self.follow_up_date < timezone.localdate():
            raise ValidationError({"follow_up_date": "Follow-up date cannot be earlier than today."})
    def __str__(self): return self.subject
    class Meta: ordering = ["follow_up_date"]

class Activity(models.Model):
    activity_type = models.CharField(max_length=30, choices=[("Call","Call"),("Meeting","Meeting"),("Email","Email"),("Task","Task")])
    subject = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    activity_date = models.DateField(default=timezone.localdate)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    lead = models.ForeignKey(Lead, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default="Open")
    def __str__(self): return self.subject

class AuditLog(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=40)
    entity_name = models.CharField(max_length=80)
    record_id = models.CharField(max_length=40, blank=True)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.action} {self.entity_name} #{self.record_id}"
    class Meta: ordering = ["-created_at"]
