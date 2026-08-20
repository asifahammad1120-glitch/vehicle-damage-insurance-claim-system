from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from claims.models import ClaimRequest
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CompanySignUpForm
from .models import CompanyProfile
from claims.services import annotate_detection_amounts



def company_signup(request):
    if request.method == "POST":
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "companies/pending_approval.html")
    else:
        form = CompanySignUpForm()
    return render(request, "companies/signup.html", {"form": form})


@staff_member_required
def manage_companies(request):
    pending = CompanyProfile.objects.filter(status="pending")
    approved = CompanyProfile.objects.filter(status="approved")
    return render(request, "companies/manage_companies.html", {
        "pending": pending,
        "approved": approved,
    })


@staff_member_required
def approve_company(request, company_id):
    company = CompanyProfile.objects.get(id=company_id)
    company.status = "approved"
    company.save()
    return redirect("manage_companies")


@staff_member_required
def reject_company(request, company_id):
    company = CompanyProfile.objects.get(id=company_id)
    company.status = "rejected"
    company.save()
    return redirect("manage_companies")

def _get_company_or_none(user):
    return CompanyProfile.objects.filter(user=user, status="approved").first()


@login_required
def company_dashboard(request):
    company = _get_company_or_none(request.user)
    if company is None:
        return render(request, "companies/not_approved.html")

    claims = ClaimRequest.objects.filter(insurance_company=company).order_by("-created_at")
    return render(request, "companies/dashboard.html", {"claims": claims, "company": company})


@login_required
def company_claim_review(request, claim_id):
    company = _get_company_or_none(request.user)
    if company is None:
        return render(request, "companies/not_approved.html")

    claim = get_object_or_404(ClaimRequest, id=claim_id, insurance_company=company)
    detections = claim.detections.all()
    report = getattr(claim, "claimreport", None)
    annotate_detection_amounts(detections, claim.vehicle_details.market_price)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "approve":
            claim.status = "approved"
        elif action == "reject":
            claim.status = "rejected"
        claim.save()
        return redirect("company_claim_review", claim_id=claim.id)

    return render(request, "companies/claim_review.html", {
        "claim": claim, "detections": detections, "report": report,
    })