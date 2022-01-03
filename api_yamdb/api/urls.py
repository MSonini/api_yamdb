from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (ReviewViewSet, CommentViewSet, UserViewSet,
                    get_confirmation_code, get_jwt_token)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', get_confirmation_code, name='get_confirmation_code'),
    path('token/', get_jwt_token, name='get_jwt_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
