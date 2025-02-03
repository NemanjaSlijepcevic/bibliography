import { updatePagination } from "./pagination.js";

document.addEventListener("DOMContentLoaded", function () {
    let currentSort = { column: null, order: "asc" };
    const categoryForm = document.getElementById("category-filter-form");
    const paginationContainer = document.getElementById("pagination-container");
    const paginateSelect = document.getElementById("paginateBy");

    document.querySelectorAll("th[data-sort]").forEach(header => {
        header.addEventListener("click", function () {
            const column = this.getAttribute("data-sort");
            if (currentSort.column === column) {
                currentSort.order = currentSort.order === "asc" ? "desc" : "asc";
            } else {
                currentSort.column = column;
                currentSort.order = "asc";
            }
            fetchAndRenderBooks(1);
        });
    });

    if (!categoryForm) {
        console.error("Category filter form not found!");
        return;
    }


    categoryForm.addEventListener("change", function () {
        fetchAndRenderBooks(1);
    });

    paginateSelect.addEventListener("change", function () {
        fetchAndRenderBooks(1);
    });

    paginationContainer.addEventListener("click", function (event) {
        if (event.target.matches(".page-link")) {
            event.preventDefault();
            const page = parseInt(event.target.dataset.page);
            if (!isNaN(page)) {
                fetchAndRenderBooks(page);
            }
        }
    });


    function fetchAndRenderBooks(page = 1) {
        showSpinner();
    
        const params = new URLSearchParams();
        params.set("page", page);
        params.set("paginate_by", document.getElementById("paginateBy").value);
        
        const selectedCategories = getSelectedCategories();
        selectedCategories.forEach(category => params.append("categories", category));

        if (currentSort.column) {
            params.set("sort", currentSort.column);
            params.set("order", currentSort.order);
        }

        fetch(window.location.pathname + "?" + params.toString(), {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
            .then(response => response.json())
            .then(data => {
                updateTable(data.books);
                updatePagination(
                    document.getElementById("pagination-container"),
                    data.has_next,
                    data.current_page,
                    data.total_pages
                );
            })
            .catch(error => console.error("Error fetching books:", error))
            .finally(() => hideSpinner());
    }

    function getSelectedCategories() {
        return Array.from(categoryForm.querySelectorAll("input[name='categories']:checked"))
            .map(input => input.value);
    }

    function showSpinner() {
        document.getElementById("loading-spinner").classList.add("loading");
        document.getElementById("book-table").classList.add("loading");
    }
    
    function hideSpinner() {
        document.getElementById("loading-spinner").classList.remove("loading");
        document.getElementById("book-table").classList.remove("loading");
    }
    

    function updateTable(books) {
        const tbody = document.getElementById("book-table-body");
        tbody.innerHTML = "";

        books.forEach((book, index) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${book.authors.join(", ")}</td>
                <td><a href="${book.detail_url}">${book.title}</a></td>
                <td>${book.publisher}</td>
                <td>${book.place}</td>
                <td>${book.year}</td>
                <td>${book.categories.join(", ")}</td>
            `;

            tbody.appendChild(row);
        });
    }

    fetchAndRenderBooks();
});
