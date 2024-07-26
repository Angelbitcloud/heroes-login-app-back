from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserFavoriteComics

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],  # Utilizar email como username
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class UserFavoriteComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteComics
        fields = ['user', 'comics_list']
