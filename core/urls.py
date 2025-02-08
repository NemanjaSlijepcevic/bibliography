from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)


app_name = 'users'
urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('login/', auth_views.LoginView.as_view(), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='users:user-login'), name='user-logout'),

]