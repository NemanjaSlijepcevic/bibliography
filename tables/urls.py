from django.urls import path
from .views import (
    AuthorAutocomplete,
    BookCreateView,
    BookDeleteView,
    BookDetailView,
    BookListView,
    BookUpdateView,
    create_author
)


app_name = 'books'
urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-view'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('author-autocomplete/', AuthorAutocomplete.as_view(), name='author-autocomplete'),
    path('create-author/', create_author, name='create-author'),

]