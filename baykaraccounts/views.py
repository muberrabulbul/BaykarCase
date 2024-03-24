from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth import authenticate


from .serializers import UserSerializer, LoginSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Abovementioned actions can be performed by request user or
    by staff on any user.

    password fields applies only to creating new user,
    to change password use change password endopint
    """

    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_active:
            return User.objects.all()
        else:
            return User.objects.filter(username=user)

    def perform_destroy(self, instance):
        """
        Override of destroy method to perform soft delete
        """
        instance.is_active = True
        instance.save()

    def perform_create(self, serializer):
        user = serializer.save()

        token_obtain_view = TokenObtainPairView.as_view()
        request_data = {
            "username": user.username,
            "password": self.request.data.get("password"),
        }
        response = token_obtain_view(self.request._request, data=request_data)
        return response


class CustomLoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse(
                {"error": "Username or password incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)

        return redirect(
            reverse("schema-swagger-ui"),
            Response(
                {
                    "username": user.username,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            ),
        )


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, "signup.html")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return redirect(
            reverse("login"),
            Response(response_data, status=status.HTTP_201_CREATED),
        )
