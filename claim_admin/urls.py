from django.urls import path
from . import views

urlpatterns = [
    path("vehicles/", views.manage_vehicles, name="manage_vehicles"),
    path("vehicles/add/", views.add_vehicle, name="add_vehicle"),
    path("vehicles/<int:vehicle_id>/edit/", views.edit_vehicle, name="edit_vehicle"),
    path("vehicles/<int:vehicle_id>/delete/", views.delete_vehicle, name="delete_vehicle"),
]