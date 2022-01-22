from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, pagination, filters, status
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Review, Categorie, Genre, Title, Comment
from .permissions import AuthorOrReadOnly, AdminOrReadOnly, Admin, Moderator
from .serializers import (CategorieSerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleSerializerGet, ConfirmationCodeSerializer,
                          UserEmailSerializer, UserSerializer,
                          SimpleUserSerializer)

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrReadOnly | Admin | Moderator]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        reviews = Review.objects.filter(title__id=title_id)
        return reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly | Admin | Moderator]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        comments = Comment.objects.filter(review__id=review_id)
        return comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class CategorieViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [AdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        queryset = Title.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        year = self.request.query_params.get('year')
        if year is not None:
            queryset = queryset.filter(year=year)
        genre = self.request.query_params.get('genre')
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGet
        else:
            return TitleSerializer


@api_view(['POST'])
def get_confirmation_code(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, created = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    message = f'Код подтверждения: {confirmation_code}'
    send_mail(
        user,
        message,
        'aдминистрация_yamdb@mail.ru',
        [email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)},
            status=status.HTTP_200_OK
        )

    message = {'confirmation_code': 'Неверный код подтверждения'}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [Admin | IsAdminUser]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = pagination.PageNumberPagination

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return UserSerializer
        else:
            return SimpleUserSerializer

    @action(
        methods=['patch', 'get'],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path='me',
        url_name='me'
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)

    def perform_create(self, serializer):
        role = self.request.data.get('role')
        if role is None:
            serializer.save()
        else:
            serializer.save(role=role)
