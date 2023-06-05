function toggleMenu(element) {
    let parent = element.parentElement;
    Array.from(parent.children).forEach(function (item) {
        if (!item.classList.contains("toggle-menu")) {
            if (item.classList.contains("menu-item-show")) {
                item.classList.remove("menu-item-show");
            }
            else {
                item.classList.add("menu-item-show");
            }
        }
    });
}
