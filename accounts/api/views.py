from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from accounts.api.serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserProfileSerializer,
)


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "message": "Your registration was successful,Welcome to our community!",
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(TokenObtainPairView):

    serializer_class = LoginSerializer

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        token = RefreshToken(refresh_token)

        if str(token["user_id"]) != str(request.user.pk):
            return Response(
                {"detail": "Token does not belong to this user."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save()

        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_205_RESET_CONTENT
        )


class UserProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user