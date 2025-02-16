from django.shortcuts import path
from . import views

urlpatterns = [    
  path('teste/', views.pacientesm name="pacientes"),
]