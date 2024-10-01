from django.contrib import admin
from django.urls import path
from WellenceApp import views
from WellenceApp.api import api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # URLs for page rendering
    path("", views.landing_page, name="landing_page"),
    path("DataEntry", views.data_entry, name="data_entry"),
    path("DashBoard", views.dash_board, name="dash_board"),
    path(
        "password_verify_link", views.password_verify_link, name="password_verify_link"
    ),
    # New API URL
    path("api/", api.urls),
    # Logout URL
    path("logout/", views.logout_view, name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
