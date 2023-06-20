from django.contrib.auth import get_user_model, authenticate
from django.db.models import QuerySet

from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import (
    RegisterSerializer, LoginSerializer, PasswordResetSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """Class for User registration"""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Method for user registration
        :param request: rest framework Request class instance
        :type request: Request
        :param args: additional arguments
        :type args: list
        :param kwargs: additional key word arguments
        :type kwargs: dict
        :return: rest framework Response class instance
        :rtype: Response
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        response_data = {
            "detail": "User successfully created.",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.CreateAPIView):
    """Class for User login"""

    serializer_class = LoginSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Method for user login
        :param request: rest framework Request class instance
        :type request: Request
        :param args: additional arguments
        :type args: list
        :param kwargs: additional key word arguments
        :type kwargs: dict
        :return: rest framework Response class instance
        :rtype: Response
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)
        if user is None:
            response_data = {'detail': 'Invalid email or password.'}
            return Response(
                data=response_data, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        response_data = {
            'detail': 'User successfully logged in.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data=response_data, status=status.HTTP_200_OK)


class UserChangePasswordView(generics.UpdateAPIView):
    """Class for password reset"""

    serializer_class = PasswordResetSerializer
    model = User
    permission_classes = (IsAuthenticated, )

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Method for user login
        :param request: rest framework Request class instance
        :type request: Request
        :param args: additional arguments
        :type args: list
        :param kwargs: additional key word arguments
        :type kwargs: dict
        :return: rest framework Response class instance
        :rtype: Response
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = user.check_password(
            serializer.validated_data["old_password"]
        )
        if not old_password:
            response_data = {
                "detail": "Wrong old password."
            }
            return Response(
                data=response_data, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.data.get("new_password"))
        user.save()
        response_data = {
            "detail": "Password changed successfully.",
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
