from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from users.permissions import IfAdmin, ReadOnly

from .filters import TitleFilter
from .models import Categorie, Genre, Title
from .serializers import (CategorieSerializer, GenreSerializer,
                          TitleSerializer, TitleSerializerGet)


class MixinView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    pass


class CategorieViewSet(MixinView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = [IfAdmin]

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()


class GenreViewSet(MixinView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = [IfAdmin]

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IfAdmin]

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGet
        else:
            return TitleSerializer
