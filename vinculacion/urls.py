from django.urls import path
import vinculacion.views as views

app_name = "vinculacion"

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('noticias', views.noticias, name='noticias'),
    path('noticias/<int:id>', views.noticia, name='noticia'),
    path('perfil', views.perfil, name='perfil'),

    # Acciones
    path(
        'perfil/eliminar', views.UsuarioEliminar.as_view(),
        name='usuario_eliminar'),

    # Formularios
    path(
        'formularios/solicitud_trabajo/<int:investigador_id>',
        views.CrearSolicitudTrabajo.as_view(), name='solicitud_trabajo_nueva'),

    # Listas

    # Solicitudes
    path(
        'perfil/solicitudes_trabajo/aprobar/<int:pk>',
        views.aceptar_solicitud,
        name='aceptar_solicitud'),
    path(
        'perfil/solicitudes_trabajo/rechazar/<int:pk>',
        views.rechazar_solicitud,
        name='rechazar_solicitud'),

    #Premio estatal CyT
    path(
        'perfil/premio-estatal',
        views.premiosCyT,
        name = 'premios'
    ),

    # Trabajos
    path(
        'perfil/trabajos', views.trabajos_en_curso,
        name='trabajos_lista'),
    path(
        'perfil/trabajos/historial', views.historial_trabajos,
        name='trabajos_historial'),
    path(
        'perfil/trabajos/cambiar_estado/<int:pk>/<str:estado>',
        views.cambiar_estado,
        name='cambiar_estado_solicitud'),

    # Misc
    path(
        'contacto',
        views.contacto,
        name='contacto'),
    path(
        'acerca_de',
        views.acerca_de,
        name='acerca_de'),

    #Usuarios Revisores
    path(
        'revisor',
        views.RevisorListaCategoriaA,
        name='revisor'
    ),
    path(
        'revisor/categoria-b',
        views.RevisorCategoriaB,
        name='revisor-categoria-b'
    ),
]
