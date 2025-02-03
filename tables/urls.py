from django.urls import path
from .views import (
    AuthorCheckView,
    BookCreateView,
    BookDeleteView,
    BookDetailView,
    BookListView,
    BookSearchView,
    BookUpdateView,
)


app_name = 'books'
urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-view'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('author-check/', AuthorCheckView.as_view(), name='author-check'),
    path('universal-check/', BookSearchView.as_view(), name='universal-check'),
]