function toggleMenu(element) {
    var parent = element.parentElement;
    Array.from(parent.childNodes).forEach(function (item) {
        item.classList.add("menu-item-show");
    });
}
