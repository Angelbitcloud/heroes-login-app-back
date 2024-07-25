from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserFavoriteComic, Comic

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

class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ['id', 'title', 'image_url', 'description']

class UserFavoriteComicSerializer(serializers.ModelSerializer):
    comic = ComicSerializer()  # Serialize the Comic instance
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Serialize the user as a PK

    class Meta:
        model = UserFavoriteComic
        fields = ['user', 'comic']

    def create(self, validated_data):
        user = self.context['request'].user
        comic_data = validated_data.pop('comic')
        comic = Comic.objects.get(id=comic_data['id'])
        favorite, created = UserFavoriteComic.objects.get_or_create(user=user, comic=comic)
        return favorite
