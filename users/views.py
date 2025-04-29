from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterValidateSerializer, AuthValidateSerializer, ConfirmationSerializer
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode
import random
import string


@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)  # username=admin1, password=123

    if user:
        if not user.is_active:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={'error': 'User account is not activated yet!'})

        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User credentials are wrong!'})


@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username,
                                    password=password,
                                    is_active=False)

    # Create a random 6-digit code
    code = ''.join(random.choices(string.digits, k=6))

    confirmation_code = ConfirmationCode.objects.create(
        user=user,
        code=code
    )

    return Response(status=status.HTTP_201_CREATED,
                    data={
                        'user_id': user.id,
                        'confirmation_code': code
                    })


@api_view(['POST'])
def confirm_user_api_view(request):
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_id = serializer.validated_data['user_id']

    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    ConfirmationCode.objects.filter(user=user).delete()

    return Response(status=status.HTTP_200_OK,
                    data={
                        'message': 'User аккаунт успешно активирован',
                        'key': token.key
                    })