# mon_application/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("portfolio/", views.simple_page, name="portfolio"),  # Page Portfolio
    path("", views.home, name="home"),
    path("download-cv/", views.download_cv, name="download_cv"),
    path("checkout/<int:service_id>/", views.create_checkout_session, name="checkout"),
    path("email/", views.email_page, name="email_page"),
    path("send-email/", views.send_email, name="send_email"),
]
