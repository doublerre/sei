from django.urls import path
import administracion.views as views
from django.contrib.auth.views import LogoutView

app_name = 'administracion'

urlpatterns = [
    path(
          '',
          views.dashboard,
          name='dashboard'),
    path(
          'aprobar_perfil/<int:pk>',
          views.aprobar_perfil,
          name='aprobar_perfil'),
    path(
          'aprobar_empresa/<int:pk>',
          views.aprobar_empresa,
          name='aprobar_empresa'),
    path(
          'salir',
          LogoutView.as_view(),
          name='logout'),

    # Usuarios
    path(
          'usuarios/lista',
          views.UsuarioLista.as_view(),
          name='usuarios_lista'),
    path(
          'usuarios/nuevo',
          views.UsuarioNuevo.as_view(),
          name='usuarios_nuevo'),
    path(
          'usuarios/editar/<int:pk>',
          views.UsuarioEditar.as_view(),
          name='usuarios_editar'),
    path(
          'usuarios/eliminar/<int:pk>',
          views.UsuarioEliminar.as_view(),
          name='usuarios_eliminar'),

    # Investigadores
    path(
          'investigadores/lista',
          views.InvestigadorLista.as_view(),
          name='investigadores_lista'),
    path(
          'investigadores/solicitud',
          views.InvestigadorSolicitud.as_view(),
          name='investigadores_solicitud'),
    path(
          'investigadores/nuevo',
          views.InvestigadorNuevo.as_view(),
          name='investigadores_nuevo'),
    path(
          'investigadores/editar/<int:pk>',
          views.InvestigadorEditar.as_view(),
          name='investigadores_editar'),
    path(
          'investigadores/eliminar/<int:pk>',
          views.InvestigadorEliminar.as_view(),
          name='investigadores_eliminar'),
    path(
          'investigadores/perfil/<int:id>',
          views.perfil,
          name='investigadores_perfil'),

    # Empresas
    path(
          'empresas/lista',
          views.EmpresaLista.as_view(),
          name='empresas_lista'),
    path(
          'empresas/solicitud',
          views.EmpresaSolicitud.as_view(),
          name='empresas_solicitud'),
    path(
          'empresas/nuevo',
          views.EmpresaNuevo.as_view(),
          name='empresas_nuevo'),
    path(
          'empresas/editar/<int:pk>',
          views.EmpresaEditar.as_view(),
          name='empresas_editar'),
    path(
          'empresas/eliminar/<int:pk>',
          views.EmpresaEliminar.as_view(),
          name='empresas_eliminar'),

    # Instituciones Educativas
    path(
        'instituciones_educativas/lista',
        views.InstitucionEducativaLista.as_view(),
        name='instituciones_educativas_lista'),
    path(
        'instituciones_educativas/solicitud',
        views.InstitucionEducativaSolicitud.as_view(),
        name='instituciones_educativas_solicitud'),
    path(
        'instituciones_educativas/nuevo',
        views.InstitucionEducativaNuevo.as_view(),
        name='instituciones_educativas_nuevo'),
    path(
        'instituciones_educativas/editar/<int:pk>',
        views.InstitucionEducativaEditar.as_view(),
        name='instituciones_educativas_editar'),
    path(
        'instituciones_educativas/eliminar/<int:pk>',
        views.InstitucionEducativaEliminar.as_view(),
        name='instituciones_educativas_eliminar'),

    # Categorias
    path(
          'categorias/lista',
          views.CategoriaLista.as_view(),
          name='categorias_lista'),
    path(
          'categorias/nuevo',
          views.CategoriaNuevo.as_view(),
          name='categorias_nuevo'),
    path(
          'categorias/editar/<int:pk>',
          views.CategoriaEditar.as_view(),
          name='categorias_editar'),
    path(
          'categorias/eliminar/<int:pk>',
          views.CategoriaEliminar.as_view(),
          name='categorias_eliminar'),

    # Investigaciones
    path(
          'investigaciones/lista',
          views.InvestigacionLista.as_view(),
          name='investigaciones_lista'),
    path(
          'investigaciones/nuevo',
          views.InvestigacionNuevo.as_view(),
          name='investigaciones_nuevo'),
    path(
        'investigaciones/editar/<int:pk>',
        views.InvestigacionEditar.as_view(),
        name='investigaciones_editar'),
    path(
        'investigaciones/eliminar/<int:pk>',
        views.InvestigacionEliminar.as_view(),
        name='investigaciones_eliminar'),

    # Noticias
    path(
          'noticias/lista',
          views.NoticiaLista.as_view(),
          name='noticias_lista'),
    path(
          'noticias/nuevo',
          views.NoticiaNueva.as_view(),
          name='noticias_nuevo'),
    path(
          'noticias/editar/<int:pk>',
          views.NoticiaEditar.as_view(),
          name='noticias_editar'),
    path(
          'noticias/eliminar/<int:pk>',
          views.NoticiaEliminar.as_view(),
          name='noticias_eliminar'),

    # Misc
    path(
          'contacto/editar',
          views.ContactoEditar.as_view(),
          name='contacto'),
    path(
          'acerca_de/editar',
          views.AcercaDeEditar.as_view(),
          name='acerca_de'),
    path(
          'convocatoria/editar',
          views.CambiarEstadoConvocatoria.as_view(),
          name='toggle_convocatoria'),
    path(
          'premios/editar',
          views.FechaPremiosEditar.as_view(),
          name='premios'),
    path(
        'premios/asignar',
        views.AsignarInvestigadores,
        name='investigadores-asignar'),
	path(
		'premios-b/lista',
        views.ListaCategoriaB,
        name='premios-b-lista'
	),
    path(
        'premios-a/lista',
        views.ListaCategoriaA,
        name='premios-a-lista'
	),
    path(
		'premios/ganador-a/<int:id>',
        views.GanadorCatA,
        name='premio-cata-ganador'
	),
    path(
		'premios/ganador-b/<int:id>',
        views.GanadorCatB,
        name='premio-catb-ganador'
	),
    path(
        'premios/comentarios-a/<int:id>',
        views.ComentariosCatA,
        name='comentarios-cat-a'
	),
    path(
        'premios/comentarios-b/<int:id>',
        views.ComentariosCatB,
        name='comentarios-cat-b'
	)
]
