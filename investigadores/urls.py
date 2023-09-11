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
    ),
    path(
        'investiadores/<int:investigador_id>/CG',
        views.mostrar_cg,
        name="mostrar_cg"
    ),
    path('investigadores/<int:investigador_id>/constancia',
         views.constancia_sei,
         name="constancia_sei"),
    path(
        'investigadores/premios/categoria-a',
        views.SolicitudCategoriaA.as_view(),
        name = 'premios-categoria-a'
    ),
    path(
        'investigadores/premios/categoria-a/<int:pk>',
        views.UpdateSolicitudCategoriaA.as_view(),
        name = 'update-premios-categoria-a'
    ),
    path(
        'investigadores/premios/categoria-b',
        views.SolicitudCategoriaB.as_view(),
        name='premios-categoria-b'
    ),
    path(
        'investigadores/premios/categoria-b/<int:pk>',
        views.UpdateSolicitudCategoriaB.as_view(),
        name='update-premios-categoria-b'
    ),
    path(
        'investigadores/premios/solicitud-realizada',
        views.solicitud_realizada,
        name="solicitud-realizada"
    ),
    path(
        'investigadores/premios/error/edad',
        views.errorEdad,
        name='error-edad'
    ),
    path(
        "investigadores/premios/solicitud/<int:rev_id>",
        views.exportZipCatA,
        name="export-zip-file"
    ),
    path(
        "investigadores/premios/solicitud-b/<int:rev_id>",
        views.exportZipCatB,
        name="export-zip-file-b"
    ),
    path(
        "investigadores/premios/categoria-a/editar/<int:pk>",
        views.EditarRevisionCatA.as_view(),
        name="asignar-calificacion-cat-a"
    ),
    path(
        "investigadores/premios/categoria-b/editar/<int:pk>",
        views.EditarRevisionCatB.as_view(),
        name="asignar-calificacion-cat-b"
    ),
    path(
        "investigadores/error/<str:error>",
        views.erroresHttp,
        name="investigador-error"
    ),
    path(
        "investigadores/error-cat-b/<str:error>",
        views.erroresHttpCatB,
        name="investigador-error"
    )
    
]
