export function fetchBooks(page = 1, categories = [], paginateBy = 10) {
    const url = new URL(window.location.href);
    url.searchParams.set("page", page);
    url.searchParams.set("paginate_by", paginateBy);
    url.searchParams.delete("categories");

    if (categories.length > 0) {
        categories.forEach(category => url.searchParams.append("categories", category));
    }

    return fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.json());
}
