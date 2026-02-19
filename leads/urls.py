from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_lead, name='create_lead'),
    path('lead/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('lead/edit/<int:pk>/', views.edit_lead, name='edit_lead'),

]
