from django.urls import reverse_lazy
from django.db.models import Q, Prefetch
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView
)
from .forms import BookForm
from .models import (
    Author,
    Book,
    Category,
    Publisher,
    Place,
    Year
)
from dal import autocomplete
from .utils import user_in_group


class ModelAutocomplete(autocomplete.Select2QuerySetView):
    model = None
    name_field = 'name'

    def get_queryset(self):
        if self.model is None:
            raise ValueError("The 'model' attribute must be set on ModelAutocomplete subclasses.")

        if not self.request.user.is_authenticated:
            return self.model.objects.none()

        qs = self.model.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class AuthorAutocomplete(ModelAutocomplete):
    model = Author

class CategoryAutocomplete(ModelAutocomplete):
    model = Category

class PlaceAutocomplete(ModelAutocomplete):
    model = Place

class PublisherAutocomplete(ModelAutocomplete):
    model = Publisher

class YearAutocomplete(ModelAutocomplete):
    model = Year


class UserPassesGroupTest(UserPassesTestMixin):
    request_group = ''
    def test_func(self):
        return user_in_group(self.request.user, self.request_group)

    def handle_no_permission(self):
        raise PermissionDenied

class BookCreateView(LoginRequiredMixin, UserPassesGroupTest, CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("books:book-create")
    request_group = "Add"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = True
        return context



class BookDeleteView(LoginRequiredMixin, UserPassesGroupTest, DeleteView):
    model = Book
    request_group = "Delete"
    success_url = reverse_lazy("books:book-list")
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:
                obj = self.get_object()
                obj.delete()
                return JsonResponse({"message": _("Book deleted successfully")}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({"error": _("Book not found")}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        return super().dispatch(request, *args, **kwargs)

class BookListView(ListView):
    model = Book
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.all()
        search_text = self.request.GET.get("search-field", "").strip()

        if search_text:
            queryset = queryset.filter(
                Q(title__icontains=search_text) |
                Q(author__name__icontains=search_text) |
                Q(publisher__name__icontains=search_text) |
                Q(category__name__icontains=search_text) |
                Q(year__name__icontains=search_text)
            ).distinct()

        categories = self.request.GET.getlist("categories")

        if categories:
            for category_id in categories:
                queryset = queryset.filter(category__id=category_id)

        if categories and search_text:
            queryset = queryset.distinct()


        sort_column = self.request.GET.get("sort", "id")
        order = self.request.GET.get("order", "asc")
        sort_mapping = {
            "author": "author__name",
            "title": "title",
            "publisher": "publisher__name",
            "place": "place__name",
            "year": "year",
            "category": "category__name"
        }

        if sort_column in sort_mapping:
            sort_field = sort_mapping[sort_column]
            if order == "desc":
                sort_field = f"-{sort_field}"
            queryset = queryset.order_by(sort_field)
            print(sort_mapping)
            print(queryset)

        print('Prefetch')
        queryset = queryset.prefetch_related(
            Prefetch('author', queryset=Author.objects.only('name')),
            Prefetch('category', queryset=Category.objects.only('name')),
        ).select_related('publisher', 'place', 'year')
        print(queryset)
        return queryset

    def get(self, request, *args, **kwargs):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            books = self.get_queryset()
            paginate_by = request.GET.get("paginate_by", "10")
            login = request.user.is_authenticated

            if paginate_by == "all":
                page_obj = books
                total_pages = 1
            else:
                paginate_by = int(paginate_by)
                paginator = Paginator(books, paginate_by)
                page_number = request.GET.get("page", 1)
                page_obj = paginator.get_page(page_number)
                total_pages = paginator.num_pages

            data = [
                {
                    "id": book.pk,
                    "title": book.title,
                    "authors": [author.name for author in book.author.all()],
                    "publisher": book.publisher.name if book.publisher else "",
                    "place": book.place.name if book.place else "" ,
                    "year": book.year.name if book.year else "" ,
                    "categories": [category.name for category in book.category.all()],
                    "detail_url": book.get_absolute_url() if login else "",
                }
                for book in page_obj
            ]

            return JsonResponse({
                "books": data,
                "can_edit" : self.request.user.is_superuser or self.request.user.groups.filter(name="Edit").exists(),  
                "has_next": getattr(page_obj, "has_next", lambda: False)(),
                "current_page": getattr(page_obj, "number", 1),
                "total_pages": total_pages
            }, safe=False)
        return super().get(request, *args, **kwargs)
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | {
            "categories": Category.objects.all(),
            "selected_categories": [int(c) for c in self.request.GET.getlist("categories")],
        }
        return context


class BookUpdateView(LoginRequiredMixin, UserPassesGroupTest, UpdateView):
    model = Book
    form_class = BookForm
    request_group = "Edit"
    success_url = reverse_lazy("books:book-list")

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "is_create": False,
            "object": self.get_object(),
        }
