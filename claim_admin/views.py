from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from claims.models import VehicleDetails


class VehicleDetailsForm(forms.ModelForm):
    class Meta:
        model = VehicleDetails
        fields = ["brand", "manufacturing_year", "market_price"]


@staff_member_required
def manage_vehicles(request):
    vehicles = VehicleDetails.objects.all().order_by("brand", "manufacturing_year")
    return render(request, "claim_admin/manage_vehicles.html", {"vehicles": vehicles})


@staff_member_required
def add_vehicle(request):
    if request.method == "POST":
        form = VehicleDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_vehicles")
    else:
        form = VehicleDetailsForm()
    return render(request, "claim_admin/vehicle_form.html", {"form": form, "action": "Add"})


@staff_member_required
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(VehicleDetails, id=vehicle_id)
    if request.method == "POST":
        form = VehicleDetailsForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect("manage_vehicles")
    else:
        form = VehicleDetailsForm(instance=vehicle)
    return render(request, "claim_admin/vehicle_form.html", {"form": form, "action": "Edit"})


@staff_member_required
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(VehicleDetails, id=vehicle_id)
    vehicle.delete()
    return redirect("manage_vehicles")