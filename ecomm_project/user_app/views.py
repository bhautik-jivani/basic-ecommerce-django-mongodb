from django.core.cache import cache

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from user_app.serializers import RoleSerializer, UserRegistrationSerializer, UserLoginSerializer, PermissionSerializer, UserProfileUpdateSerializer
from user_app.models import User, Permission, Role
from user_app.permissions import HasPermission


# Create your views here.
class RoleCreateOrUpdateViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    permission_required = ["*", "view_role", "add_role", "update_role"]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = RoleSerializer

    def get_queryset(self):
        cache.clear()
        queryset = Role.objects.all()
        return queryset
    
    def get_object(self):
        cache.clear()
        id = self.kwargs.get("id")
        try:
            obj = Role.objects.get(id=id)
            return obj
        except Exception:
            raise NotFound('Role does not found')


class PermissionCreateOrUpdateViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    permission_required = ["*", "view_permission", "add_permission", "update_permission"]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = PermissionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        cache.clear()
        queryset = Permission.objects.all()
        return queryset
    
    def get_object(self):
        cache.clear()
        id = self.kwargs.get("id")
        try:
            obj = Permission.objects.get(id=id)
            return obj
        except Exception:
            raise NotFound('Permission does not found')


class LoginViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            refresh = RefreshToken.for_user(user)
            data = {
                'message': 'User loggedin successfully!',
                'name': user.name,
                'email': user.email,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'message': 'User registered successfully!',
                'name': user.name,
                'email': user.email,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    permission_required = ["*", "view_user", "update_user"]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = UserProfileUpdateSerializer
    lookup_field = 'id'

    def get_queryset(self):
        cache.clear()
        queryset = User.objects.all()
        return queryset
    
    def get_object(self):
        cache.clear()
        id = self.kwargs.get("id")
        try:
            obj = User.objects.get(id=id)
            return obj
        except Exception:
            raise NotFound('User Profile does not found')


class ProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    permission_required = ["*", "view_user", "update_user"]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = UserProfileUpdateSerializer
    lookup_field = 'id'

    def get_queryset(self):
        cache.clear()
        queryset = User.objects.all()
        return queryset
    
    def get_object(self):
        cache.clear()
        try:
            obj = User.objects.get(id=self.request.user.id)
            return obj
        except Exception:
            raise NotFound('Profile does not found')