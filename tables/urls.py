from django.urls import path
from .views import (
    AuthorAutocomplete,
    PublisherAutocomplete,
    CategoryAutocomplete,
    PlaceAutocomplete,
    YearAutocomplete,
    BookCreateView,
    BookDeleteView,
    BookDetailView,
    BookListView,
    BookUpdateView,
)


app_name = 'books'
urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-view'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('author-autocomplete/', AuthorAutocomplete.as_view(create_field='name', validate_create=True), name='author-autocomplete'),
    path('publisher-autocomplete/', PublisherAutocomplete.as_view(create_field='name', validate_create=True), name='publisher-autocomplete'),
    path('category-autocomplete/', CategoryAutocomplete.as_view(create_field='name', validate_create=True), name='category-autocomplete'),
    path('place-autocomplete/', PlaceAutocomplete.as_view(create_field='name', validate_create=True), name='place-autocomplete'),
    path('year-autocomplete/', YearAutocomplete.as_view(create_field='name', validate_create=True), name='year-autocomplete'),
]