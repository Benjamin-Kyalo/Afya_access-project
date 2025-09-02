from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return HttpResponse(f"Hello, {request.user.username} (Patient Dashboard)")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),             # signup route
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
    path("dashboard/", dashboard, name="dashboard"),
]
