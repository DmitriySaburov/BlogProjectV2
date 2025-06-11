from django.urls import path

from .views import ProfileUpdateView, ProfileDetailView



urlpatterns = [
    path("user/<slug:slug>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("user/edit/", ProfileUpdateView.as_view(), name='profile_edit'),
]
