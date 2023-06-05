from django.urls import path
from usuarios import views

app_name = 'usuarios'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('registrar', views.RegistrarView.as_view(), name='registrar'),
    path(
        'activar/<slug:uidb64>/<slug:token>',
        views.ActivarCuentaView.as_view(), name='activar'),
]
