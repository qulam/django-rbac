from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
import django_filters

from core.common.helpers import default_response, api_view

from user.api.serializers import (
    AuthenticationJWTSerializer,
    PermissionSerializer,
    GroupSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    UserProfileSerializer,
)

from user.models import User


class AuthenticationJWTView(TokenObtainPairView):
    serializer_class = AuthenticationJWTSerializer


class GroupsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Group
        fields = ['name']


class GroupsView(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions
    )
    authentication_class = (JWTAuthentication,)
    filter_class = GroupsFilter

    serializer_class = GroupSerializer
    queryset = Group.objects.all().order_by('-id')


class PermissionsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Permission
        fields = ['name']


class PermissionsView(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions
    )
    authentication_class = (JWTAuthentication,)
    filter_class = PermissionsFilter

    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()


class UsersFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth',
            'is_superuser', 'is_admin', 'status', 'groups', 'user_permissions'
        ]


class UsersView(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions
    )
    authentication_class = (JWTAuthentication,)
    filter_class = UsersFilter

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all().order_by('-id')


class UserProfileView(RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions
    )
    authentication_class = (JWTAuthentication,)

    queryset = get_user_model().objects.all()

    def get(self, request):
        UserModel = get_user_model()

        try:
            user_data = UserModel.objects.get(pk=request.user.pk)
            serialized_user = UserProfileSerializer(user_data).data

            response = default_response(
                data=serialized_user,
                status='true',
                status_code=status.HTTP_200_OK,
                message='User profile fetched successfully'
            )
            return Response(response, status=status.HTTP_200_OK)

        except UserModel.DoesNotExist:
            response = default_response(
                data=None,
                status='false',
                status_code=status.HTTP_404_NOT_FOUND,
                message='User profile does not exists'
            )
            return Response(response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'], use_serializer=UserRegistrationSerializer)
@permission_classes((permissions.AllowAny,))
@authentication_classes([])
def api_authentication_register(request):
    serialized = UserRegistrationSerializer(data=request.data)

    if serialized.is_valid():
        created_user = User.objects.create_user(
            first_name=serialized.initial_data['first_name'],
            last_name=serialized.initial_data['last_name'],
            email=serialized.initial_data['email'],
            password=serialized.initial_data['password'],
        )

        response = default_response(
            data=UserRegistrationSerializer(created_user, fields=['id', 'first_name', 'last_name', 'email']).data,
            status='true',
            status_code=status.HTTP_200_OK,
            message='Your register request successfully sent'
        )
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = default_response(
            data=None,
            status='false',
            status_code=status.HTTP_400_BAD_REQUEST,
            message=serialized.errors
        )
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
