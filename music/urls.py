from django.urls import path
from .views import ListSongsView, LoginView, LogoutView, RegisterUsersView, ListUsersView

urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('users/', ListUsersView.as_view(), name="users-all"),
    path('login/', LoginView.as_view(), name="auth-login"),
    path('logout/', LogoutView.as_view(), name="auth-logout"),
    path('register/', RegisterUsersView.as_view(), name="auth-register"),
]
