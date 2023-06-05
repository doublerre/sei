# from django.urls import path
from django.urls import path
from django.contrib.auth.decorators import login_required
import investigadores.views as views

app_name = "investigadores"

urlpatterns = [
    path(
        'formularios/investigador',
        login_required(views.InvestigadorSolicitud.as_view()),
        name='investigador_form'),
    path(
        'formularios/investigador/actualizar',
        views.InvestigadorActualizar.as_view(),
        name='investigador_actualizar'),
    path(
        'investigadores',
        views.InvestigadorLista.as_view(),
        name='investigadores_lista'),
    path(
        'perfil/investigaciones', views.InvestigadorInvestigaciones.as_view(),
        name='investigaciones_lista'),
    path(
        'perfil/solicitudes_trabajo',
        views.InvestigadorSolicitudesTrabajo.as_view(),
        name='solicitudes_trabajo_lista'),
    path(
        'formularios/investigacion',
        views.InvestigacionNuevo.as_view(),
        name='investigacion_nuevo'),
    path(
        'perfil/investigaciones/fetch',
        views.investigaciones_google,
        name='investigaciones_fetch'),
    path(
        'investigadores/<int:investigador_id>',
        views.investigador_perfil,
        name='investigador_perfil'),
    path(
        'investigadores/<int:investigador_id>/CV',
        views.mostrar_cv,
        name='mostrar_cv'
    )
]
