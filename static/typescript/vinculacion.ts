
// Datos globales 
interface User {
  username: string,
  latitud: number,
  longitud: number,
  tipoUsuario: string,
  categorias: Array<string>,
  municipio: number,
  url: string,
}

interface ChoicesEvent {
  detail: ChoicesDetail,
}

interface ChoicesDetail {
  label: string,
}

const municipioSelect: HTMLSelectElement = document.getElementById("municipio") as HTMLSelectElement;
var usuarios: Array<User> = [];
var etiquetas: Array<string> = [];
document.getElementsByClassName("choices")[2].addEventListener('addItem', function(event) {etiquetas.push((event as unknown as ChoicesEvent).detail.label); recargarUsuariosMapa()});
document.getElementsByClassName("choices")[2].addEventListener('removeItem', function(event) {etiquetas.splice(etiquetas.indexOf((event as unknown as ChoicesEvent).detail.label), 1); recargarUsuariosMapa()});
var icons: Array<L.Icon> = ["grey", "green", "blue", "violet", "gold"].map((color: string) => {
  return new L.Icon({
      iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
});
var precisionMinima = 2;

function obtenerUsuarios(lista_usuarios: Array<User>): void {
  usuarios = lista_usuarios;
}

//Mapa
var markers: Array<L.Marker> = [];
var mapa = L.map('map', {
  center: L.latLng(22.7613421, -102.5828555),
  zoom: 7,
});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mapa);
var filtros_tipo_usuario: HTMLElement = document.getElementById('filtro_tipo_usuario');

function mostrarUsuariosMapa(): void {
  let filtros: Array<string> = Array.from(filtros_tipo_usuario.children).map((div: HTMLElement) => {
    let input = div.children[0] as HTMLInputElement;
    let label = div.children[1];
    return {
      filtro: label.textContent.trim(),
      activo: input.checked
    };
  }).filter((datos_filtro: { filtro: string, activo: boolean }) => datos_filtro.activo)
    .map((datos_filtro: { filtro: string, activo: boolean }) => datos_filtro.filtro);
  
  let etiquetasRequeridas: Array<string> = etiquetas;
  
  let municipioRequerido = municipioSelect.options[municipioSelect.selectedIndex].value;
  
  let usuarios_filtrados = usuarios.filter((usuario: User) => {
    return filtros.indexOf(usuario.tipoUsuario) != -1;
  });

  if (municipioRequerido !== "") {
    usuarios_filtrados = usuarios_filtrados.filter((usuario: User) => {
      return usuario.municipio == +municipioRequerido;
    })    
  }

  usuarios_filtrados.forEach((usuario: User) => {
    let precision: number = usuario.categorias.map((categoria: string) => {
      if(etiquetasRequeridas.indexOf(categoria) != -1) {
        return 1;
      } else {
        return 0;
      }
    }).reduce((previous: number, current: number) => previous + current, 0);
    
    if (precision > 0) {
      precision = Math.floor((icons.length - 1) * (precision / etiquetasRequeridas.length));
      if (precision >= precisionMinima) {
        crearPinMapa(usuario, precision);
      }
    }
  });
}

function limpiarUsuariosMapa(): void {
  markers.forEach((marker: L.Marker) => mapa.removeLayer(marker));
  markers = [];
}

function recargarUsuariosMapa(): void {
  limpiarUsuariosMapa();
  mostrarUsuariosMapa();
}

function crearPinMapa(usuario: User, precision: number): void {
  let m: L.Marker = L.marker([usuario.latitud, usuario.longitud], {icon: icons[precision]});
  m.addTo(mapa).bindPopup(`
    <h3>${usuario.tipoUsuario}: ${usuario.username}</h3>
    <a href="${usuario.url}" class="btn btn-primary">Ver detalles</a>
    `);
  markers.push(m);
}

//Precision
const precisionInput: HTMLInputElement = document.getElementById("precision") as HTMLInputElement;
const precisionBar: HTMLDivElement = document.getElementById("barra-precision") as HTMLDivElement;

function cambiarPrecision(elementoPrecision: HTMLButtonElement): void {
  precisionMinima = +elementoPrecision.value;
  recargarUsuariosMapa();
  actualizarBarraPrecision();
}

function actualizarBarraPrecision(): void {
  let nivelesPrecision: Array<HTMLButtonElement> = Array.from(precisionBar.children).map((nivelPrecision: HTMLElement) => {
    return nivelPrecision as HTMLButtonElement;
  });
  nivelesPrecision.forEach((nivelPrecision: HTMLButtonElement) => {
    nivelPrecision.classList.remove("activo");
  });
  
  for (let i = 0; i < (nivelesPrecision.length - precisionMinima); i++) {
    nivelesPrecision[i].classList.add("activo");
  }
}
//Recarga
function reescalarMapa(): void {
  setTimeout(function () {
    mapa.invalidateSize(true);
  }, 100);
}

//Areas conocimiento
var areaRequerida: string = "Cualquiera";

function setAreaRequerida(areaConocimiento: string): void {
  areaRequerida = areaConocimiento;
  filtrarAreaConocimiento();
}

function filtrarAreaConocimiento(): void {
  let nodes: HTMLCollection = document.getElementsByClassName("choices__list--dropdown")[1].children[0].children;
  let requerido: boolean = true;
  Array.from(nodes).forEach((nodo: HTMLDivElement) => {
    if (nodo.classList.contains("choices__group")) {
      requerido = nodo.textContent === areaRequerida || areaRequerida === "Cualquiera";
    }

    if (requerido) {
      nodo.classList.remove("oculto");
    } else {
      nodo.classList.add("oculto");
    }
  });
}

actualizarBarraPrecision();
reescalarMapa();