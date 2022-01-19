from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comment, Categorie, Genre, Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, required=False)
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Categorie


class GenreSerializer(serializers.ModelSerializer):
    # ^[-a-zA-Z0-9_]+$

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genre', )
        model = Title
