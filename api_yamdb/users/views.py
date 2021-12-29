from rest_framework import filters, status, viewsets
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import LimitOffsetPagination


from .models import User
from .permissions import IfAdmin
from .serializers import (ConfirmationCodeSerializer, UserEmailSerializer,
                          UserSerializer)


@api_view(['POST'])
def get_confirmation_code(request):
    serializer = UserEmailSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    if username == 'me':
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.validated_data.get('email')
    user, created = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    message = f'Код подтверждения: {confirmation_code}'
    send_mail(
        user,
        message,
        email,
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
        return Response({'token': str(token.access_token)}, status=status.HTTP_200_OK)

    resp = {'confirmation_code': 'Неверный код подтверждения'}
    return Response(resp, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes =[IfAdmin|IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ('user__username',)
    pagination_class = LimitOffsetPagination 

    def perform_create(self, serializer):
        User.objects.create(**serializer.validated_data)
