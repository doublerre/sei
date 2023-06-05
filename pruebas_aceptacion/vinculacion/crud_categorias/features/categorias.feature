Característica: categorias para la organización
    Yo como administrador quiero tener diferentes 
    categorías para ordenar los diferentes recursos
    y sea más facil su busqueda

    Escenario: Ingresar una nueva categoría correctamente
    Dado que deseo ingresar una nueva categoría como administrador con el usuario "guz" y password "admin"
    Cuando coloque el nombre "Prueba" el area y la descripación "Esto es una prueba" y envíe el formulario 
    Entonces se mostrará un mensaje que diga "Categoría registrada correctamente"

    Escenario: Eliminar categoría correctamente.
    Dado que deseo eliminar la categotía "Prueba" logeo como administrador "guz" con la password "admin"
    Cuando presione el botón "eliminar"
    Entonces la categoría será removida de la lista.

    Escenario: Editar categoría correctamente
    Dado que deseo modificar una categoría logeo como administrador "guz" con la password "admin" en la categoria "3"
    Cuando llene el formulario con el nombre "Prueba modificar" y la descripación "Descripción modificada" y lo envié 
    Entonces se mostrará el mensaje "Categoría actualizada correctamente"
    
    Escenario: Consultar la lista de categorías existentes.
    Dado que deseo mirar las categorías que existen logeo como administrador "guz" con la password "admin"
    Cuando vaya a la lista en "/administracion/categorias/lista"
    Entonces se mostrara todas las categorías existentes.

 