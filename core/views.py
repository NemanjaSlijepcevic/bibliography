from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SignupForm
from django.contrib.auth.models import User, Group
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView
)

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("users:user-create")
    permission_required = 'auth.change_user'  # Requires 'change_user' permission

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_superuser'] = self.request.user.is_superuser
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_superuser'] = self.request.user.is_superuser
        context['is_create'] = True
        return context

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:user-list")
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({"message": "User deleted successfully"}, status=200)
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("users:user-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_superuser'] = self.request.user.is_superuser
        return kwargs

    def form_valid(self, form):
        form.instance.edited_by = self.request.user

        print(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        context['object'] = self.get_object()
        return context

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied

       