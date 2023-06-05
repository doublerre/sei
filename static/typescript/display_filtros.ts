const searchMenu: HTMLElement = document.getElementById('search-side');
const filtroBtnOut: HTMLElement = document.getElementById('filtro-btn-out');


function hideSearchSide(): void {
    searchMenu.classList.add("oculto");
    filtroBtnOut.classList.remove("oculto");
}

function showSearchSide(): void {
    searchMenu.classList.remove("oculto");
    filtroBtnOut.classList.add("oculto");
}
