from django.urls import path
from .views import RegisterView, LoginView, CurrentUserView, FavoriteComicsView, FavoriteComicDeleteView
from .views import CustomTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('favorites/', FavoriteComicsView.as_view(), name='favorite_comics'),
    path('favorites/<int:comic_id>/', FavoriteComicDeleteView.as_view(), name='remove_favorite'),
    path('refresh-token/', CustomTokenRefreshView.as_view(), name='refresh_token'),  # Nueva ruta para refrescar token
]
