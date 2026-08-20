from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.company_signup, name="company_signup"),
    path("manage/", views.manage_companies, name="manage_companies"),
    path("manage/<int:company_id>/approve/", views.approve_company, name="approve_company"),
    path("manage/<int:company_id>/reject/", views.reject_company, name="reject_company"),
    path("dashboard/", views.company_dashboard, name="company_dashboard"),
    path("dashboard/<int:claim_id>/", views.company_claim_review, name="company_claim_review"),
]