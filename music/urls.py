from django.urls import path
from .views import ListSongsView, LoginView, LogoutView, RegisterUsersView, ListUsersView, UTIDetailView, ListCreateUTIView, UTIDeleteView, IdView, UserView

urlpatterns = [
    #path('info/', IdView.as_view(), name="personal-info"),
    path('info/', UserView.as_view(), name="personal-info"),
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('users/', ListUsersView.as_view(), name="users-all"),
    path('login/', LoginView.as_view(), name="auth-login"),
    path('logout/', LogoutView.as_view(), name="auth-logout"),
    path('register/', RegisterUsersView.as_view(), name="auth-register"),
    path('tokenInfo/', ListCreateUTIView.as_view(), name="uti-all"),
    path('tokenInfo/<int:userID>/', UTIDetailView.as_view(), name="uti-detail"),
    path('deleteTokenInfo/<int:pk>/', UTIDeleteView.as_view(), name="uti-delete"),
]
