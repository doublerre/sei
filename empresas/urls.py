from django.urls import path
import empresas.views as views

app_name = "empresas"

urlpatterns = [
    path(
        'formularios/empresa',
        views.EmpresaSolicitud.as_view(),
        name='empresa_form'),
    path(
        'formularios/empresa/actualizar',
        views.EmpresaActualizar.as_view(),
        name='empresa_actualizar'),
    path(
        'empresas', views.EmpresaLista.as_view(),
        name='empresas_lista'),
]
