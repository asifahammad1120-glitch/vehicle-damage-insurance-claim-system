from  django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_claim, name="create_claim"),
    path("<int:claim_id>/", views.claim_detail, name="claim_detail"),
    path("history/", views.claim_history, name="claim_history"),
    path("<int:claim_id>/download/", views.download_claim_report, name="download_claim_report"),

]