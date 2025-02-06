from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserUpdateView,
)


app_name = 'korisnici'
urlpatterns = [
    path('', UserListView.as_view(), name='korisnik-list'),
    path('signup/', UserCreateView.as_view(), name='korisnik-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='korisnik-view'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='korisnik-delete'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='korisnik-update'),
    path('login/', auth_views.LoginView.as_view(), name='korisnik-login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='korisnici:korisnik-login'), name='korisnik-logout'),

]