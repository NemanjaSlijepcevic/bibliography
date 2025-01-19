from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from .forms import BookForm
from .models import Author, Book, Category


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy("books:book-create")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("books:book-list")
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({"message": "Book deleted successfully"}, status=200)
        return super().dispatch(request, *args, **kwargs)

class BookDetailView(DetailView):
    queryset = Book.objects.all()

class BookListView(ListView):

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', 10)

    def get_queryset(self):
        queryset = Book.objects.all()
        categories = self.request.GET.getlist('categories')
        authors = self.request.GET.getlist('authors')
        
        if categories:
            print(categories)
            queryset = (
                queryset.filter(category__id__in=categories)
                .annotate(num_categories=Count('category'))
                .filter(num_categories=len(categories))
            )
            print(queryset)

        if authors:
            queryset = (
                queryset.filter(author__id__in=authors)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['categories'] = Category.objects.all()
        context['selected_authors'] = [int(a) for a in self.request.GET.getlist('authors')]
        context['selected_categories'] = [int(c) for c in self.request.GET.getlist('categories')]
        return context

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("books:book-list")
    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        context['object'] = self.get_object()
        return context
