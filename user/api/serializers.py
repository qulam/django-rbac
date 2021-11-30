from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from user.models import User

from core.common.helpers import DynamicFieldsModelSerializer


class AuthenticationJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.pk
        return token


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'codename', 'name')


class GroupSerializer(serializers.ModelSerializer):
    permissions_list = PermissionSerializer(source="permissions", many=True, read_only=True)
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions', 'permissions_list')
        depth = 1


class UserSerializer(DynamicFieldsModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)
    user_permissions_list = PermissionSerializer(source="user_permissions", many=True, read_only=True)
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    groups_list = GroupSerializer(source="groups", many=True, read_only=True)

    class Meta:
        model = get_user_model()
        extra_kwargs = {'password': {'write_only': True}}
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'is_superuser', 'is_admin', 'status',
            'groups', 'groups_list', 'user_permissions', 'user_permissions_list', 'password'
        ]

    def create(self, validated_data):
        """Create and return a new user."""

        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['first_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            date_of_birth=validated_data['date_of_birth'],
            is_superuser=validated_data['is_superuser'],
            is_admin=validated_data['is_admin'],
            status=validated_data['status']
        )

        user.set_password(validated_data['password'])
        user.save()
        user.user_permissions.add(*validated_data['user_permissions'])

        if validated_data['groups'] is not None:
            user.groups.add(*validated_data['groups'])

        return user


class UserProfileSerializer(DynamicFieldsModelSerializer):
    groups = GroupSerializer(many=True)
    user_permissions = PermissionSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'is_superuser', 'is_admin', 'status',
            'groups', 'user_permissions'
        ]


class UserRegistrationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
