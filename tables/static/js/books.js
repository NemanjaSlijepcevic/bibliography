import { fetchBooks } from "./fetchBooks.js";
import { updatePagination } from "./pagination.js";

document.addEventListener("DOMContentLoaded", function () {
    const categoryForm = document.getElementById("category-filter-form");
    const paginationContainer = document.getElementById("pagination-container");
    const paginateSelect = document.getElementById("paginateBy");

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
    
        fetchBooks(page, getSelectedCategories(), paginateSelect.value)
            .then(data => {
                updateTable(data.books);
                updatePagination(paginationContainer, data.has_next, data.current_page, data.total_pages);
            })
            .catch(error => {
                console.error("Error fetching books:", error);
            })
            .finally(() => {
                hideSpinner();
            });
    }

    function getSelectedCategories() {
        return Array.from(categoryForm.querySelectorAll("input[name='categories']:checked"))
            .map(input => input.value);
    }

    function showSpinner() {
        document.getElementById("loading-spinner").classList.add("active");
    }
    
    function hideSpinner() {
        document.getElementById("loading-spinner").classList.remove("active");
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
