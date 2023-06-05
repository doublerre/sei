const searchMenu = document.getElementById('search-side');
const filtroBtnOut = document.getElementById('filtro-btn-out');
function hideSearchSide() {
    searchMenu.classList.add("oculto");
    filtroBtnOut.classList.remove("oculto");
}
function showSearchSide() {
    searchMenu.classList.remove("oculto");
    filtroBtnOut.classList.add("oculto");
}
