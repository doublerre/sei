from django.urls import path
import instituciones_educativas.views as views

app_name = 'instituciones_educativas'

urlpatterns = [
    path(
        'formularios/institucion_educativa',
        views.InstitucionEducativaSolicitud.as_view(),
        name='institucion_educativa_form'),
    path(
        'formularios/institucion_educativa/actualizar',
        views.InstitucionEducativaActualizar.as_view(),
        name='institucion_educativa_actualizar'),
    path(
        'institucion_educativa/solicitud_ingreso',
        views.solicitud_ingreso_lista,
        name='institucion_educativa_solicitudes'),
    path(
        'instituciones_educativas/', views.instituciones_educativas_lista,
        name='instituciones_educativas_lista'),
    path(
        'investigador/solicitud_ingreso/<int:institucion_id>',
        views.crear_solicitud_ingreso,
        name='crear_solicitud_ingreso'),
    path(
        'institucion_educativa/solicitud_ingreso/' +
        '<int:investigador_id>/<int:respuesta>',
        views.contestar_solicitud_ingreso,
        name='contestar_solicitud_ingreso'),
    path(
        'institucion_educativa/miembros/eliminar/<int:investigador_id>',
        views.miembro_eliminar,
        name='miembro_eliminar'),
    path(
        'institucion_educativa/miembros', views.miembros_lista,
        name='institucion_educativa_miembros'),
]
