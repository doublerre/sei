function toggleMenu(element: HTMLElement): void {
  let parent: HTMLUListElement = element.parentElement as HTMLUListElement;
  Array.from(parent.children).forEach(function(item: HTMLElement) {
    if (!item.classList.contains("toggle-menu")) {
      if (item.classList.contains("menu-item-show")) {
        item.classList.remove("menu-item-show");
      } else {
        item.classList.add("menu-item-show");
      }
    }
  });
}
