from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Review, Comment, Categorie, Genre, Title

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Categorie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


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
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'category',
                  'genre', 'description', 'rating',)
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class TitleSerializerGet(serializers.ModelSerializer):
    category = CategorieSerializer(allow_null=False)
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'category',
                  'genre', 'description', 'rating')
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    title = TitleSerializer(required=False)

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        author = request.user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        title = get_object_or_404(Title, id=title_id)
        if (Review.objects.filter(author=author, title=title).exists()
           and request.method == 'POST'):
            raise serializers.ValidationError(
                'You alredy have review on this title.')
        return super().validate(data)


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким email уже существует!')
        ]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким username уже существует!'
            )
        ]
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким email уже существует!')
        ]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким username уже существует!'
            )
        ]
    )


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)