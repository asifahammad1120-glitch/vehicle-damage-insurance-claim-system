from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .forms import ClaimRequestForm
from .models import ClaimRequest, DamageDetection, ClaimReport
from .services import calculate_claim_amount, annotate_detection_amounts
from ai_pipeline.inference import run_pipeline


@login_required
def create_claim(request):
    if request.method == "POST":
        form = ClaimRequestForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.user = request.user
            claim.save()

            # Run the AI pipeline on the uploaded image
            detections = run_pipeline(claim.accident_image.path)

            # Save each detected part as a DamageDetection row
            for det in detections:
                DamageDetection.objects.create(
                    claim=claim,
                    part_name=det["part_name"],
                    yolo_confidence=det["yolo_confidence"],
                    severity=det["severity"],
                    severity_confidence=det["severity_confidence"],
                    bbox_x1=det["bbox"][0],
                    bbox_y1=det["bbox"][1],
                    bbox_x2=det["bbox"][2],
                    bbox_y2=det["bbox"][3],
                )

            # Calculate and save the claim report
            market_price = claim.vehicle_details.market_price
            amount = calculate_claim_amount(market_price, detections)
            ClaimReport.objects.create(claim=claim, claim_amount=amount)

            return redirect("claim_detail", claim_id=claim.id)
    else:
        form = ClaimRequestForm()

    return render(request, "claims/create_claim.html", {"form": form})


@login_required
def claim_detail(request, claim_id):
    claim = get_object_or_404(ClaimRequest, id=claim_id, user=request.user)
    detections = claim.detections.all()
    report = getattr(claim, "claimreport", None)

    annotate_detection_amounts(detections, claim.vehicle_details.market_price)

    return render(request, "claims/claim_detail.html", {
        "claim": claim, "detections": detections, "report": report,
    })

@login_required
def claim_history(request):
    claims = ClaimRequest.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "claims/claim_history.html", {"claims": claims})


@login_required
def download_claim_report(request, claim_id):
    claim = get_object_or_404(ClaimRequest, id=claim_id, user=request.user)
    detections = claim.detections.all()
    report = getattr(claim, "claimreport", None)
    annotate_detection_amounts(detections, claim.vehicle_details.market_price)

    html = render_to_string("claims/claim_report_pdf.html", {
        "claim": claim, "detections": detections, "report": report,
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="claim_{claim.id}_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response