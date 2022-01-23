from django.urls import include, path
from rest_framework import routers

from .views import CategorieViewSet, GenreViewSet, TitleViewSet

app_name = 'cgt'

router = routers.DefaultRouter()

router.register('categories', CategorieViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
