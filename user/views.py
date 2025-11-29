# views.py
from plant_care.permission import LoginRequiredPermission
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import User, UserCreateSerializer, UserCreateSerializer, UserSerializer, UserUpdateSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"message": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        email = ""
        if username:
            user_data = User.objects.filter(username=username).get()
            if user_data:
                email = user_data.email
        user = authenticate(request, email=email, password=password) 

        if not user or not user.is_active:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)

        response = Response({
            "message": "Login successful",
            "data": serializer.data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)

        # HttpOnly secure cookie
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=True,           # Set False in local dev if no HTTPS
            samesite="Lax",        # Use "None" only if cross-site + secure=True
            max_age=86400            # 5 minutes
        )

        return response
        
class UserCreateView(APIView):
    """
    API view for creating a new user.
    All errors are returned via the custom exception handler as {"message": "..."}.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # <-- will raise DRF ValidationError
        serializer.save()
        return Response(
            {"message": "User created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
class UserMeView(APIView):
    permission_classes = [LoginRequiredPermission]
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserUpdateView(APIView):
    permission_classes = [LoginRequiredPermission]
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)