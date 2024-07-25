from datetime import timedelta
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .models import UserFavoriteComic 
from .serializers import UserFavoriteComicSerializer
from rest_framework_simplejwt.views import TokenRefreshView



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials'}, status=400)

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token requerido'}, status=400)
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)
            return Response({
                'access': new_access_token,
                'refresh': new_refresh_token
            })
        except Exception as e:
            return Response({'detail': str(e)}, status=400)

class FavoriteComicsView(generics.ListCreateAPIView):
    serializer_class = UserFavoriteComicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserFavoriteComic.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        comic_data = request.data.get('id')  #se espera recibir el ID del cómic como un entero
        
        print('Received data:', request.data)  # verificar el contenido 
        
        if comic_data is None:
            return Response({'detail': 'comic_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verifica si el cómic ya está en favoritos
        if UserFavoriteComic.objects.filter(user=user, comic_id=comic_data).exists():
            return Response({'detail': 'Comic already in favorites'}, status=status.HTTP_400_BAD_REQUEST)

        # Agrega el cómic a favoritos
        serializer = self.get_serializer(data={'user': user.id, 'comic': comic_data})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteComicDeleteView(generics.DestroyAPIView):
    serializer_class = UserFavoriteComicSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        comic = self.kwargs.get('comic')
        return UserFavoriteComic.objects.get(user=user, comic=comic)

class CustomTokenRefreshView(TokenRefreshView):
    pass