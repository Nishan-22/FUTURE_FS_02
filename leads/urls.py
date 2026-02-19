from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('leads/', views.lead_list, name='lead_list'),
    path('lead/create/', views.create_lead, name='create_lead'),
    path('lead/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('lead/edit/<int:pk>/', views.edit_lead, name='edit_lead'),
    path('note/delete/<int:pk>/', views.delete_note, name='delete_note'),
    path('api/capture/', views.LeadCaptureView.as_view(), name='api_capture_lead'),
]
