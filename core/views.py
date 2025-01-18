from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignupForm
from django.contrib.auth.models import User
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

class UserCreateView(CreateView):
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("korisnici:korisnik-create")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("korisnici:korisnik-list")
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({"message": "User deleted successfully"}, status=200)
        return super().dispatch(request, *args, **kwargs)

class UserDetailView(LoginRequiredMixin, DetailView):
    queryset = User.objects.all()

class UserListView(LoginRequiredMixin, ListView):
    queryset = User.objects.all()

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("korisnici:korisnik-list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        context['object'] = self.get_object()
        return context