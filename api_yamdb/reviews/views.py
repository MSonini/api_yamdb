from rest_framework import viewsets, pagination
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework import filters

from .models import Review, Categorie, Genre, Title
from .permissions import AuthorOrReadOnly, AdminOrReadOnly
from .serializers import (CategorieSerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleSerializerGet)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name', 'year', 'genre__slug', 'category__slug',)

    def get_queryset(self):
        queryset = Title.objects.all()
        # Добыть параметр color из GET-запроса
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
