from rest_framework import serializers

from .models import Categorie, Genre, Title


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categorie.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerGet(serializers.ModelSerializer):
    category = CategorieSerializer()
    genre = GenreSerializer(many=True)
    #  rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title
