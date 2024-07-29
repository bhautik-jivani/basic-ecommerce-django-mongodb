from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from rest_framework import serializers

from user_app.models import User, Permission, Role, USER_TYPES

from bson import ObjectId
from bson.errors import InvalidId


class PermissionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)

    def validate_name(self, value):
        try:
            Permission.objects.get(name=value.lower())
            raise serializers.ValidationError(f'{value} permission already exists.')
        except Exception:
            return value.lower()

    def create(self, validated_data):
        obj = Permission.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RoleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    permissions = serializers.ListField(child=serializers.CharField(), allow_empty=True)

    def to_representation(self, instance):
       representation = super().to_representation(instance)
       representation['permissions'] = PermissionSerializer(instance.permissions, many=True).data
       return representation

    def validate_name(self, value):
        try:
            Role.objects.get(name=value.lower())
            raise serializers.ValidationError(f'{value} role already exists.')
        except Exception:
            return value.lower()
        
    def validate_permissions(self, value):
        objs = []
        for permission_id in value:
            try:
                ObjectId(permission_id)
            except (TypeError, InvalidId):
                raise serializers.ValidationError(f"{permission_id} invalid permission.")
            try:
                obj = Permission.objects.get(id=permission_id)
                objs.append(obj)
            except Permission.DoesNotExist:
                raise serializers.ValidationError(f'{permission_id} is invalid permission.')
        return objs
        
    def create(self, validated_data):
        role = Role.objects.create(**validated_data)
        return role
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password', 'write_only': True})
    contact_number = serializers.CharField()
    user_type = serializers.ChoiceField(required=True, choices=USER_TYPES)

    def validate_email(self, value):
        email = value.lower()
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError('Email address already exists')
        except User.DoesNotExist:
            return email
        
    def validate_password(self, value):
        return make_password(value)

    def validate_user_type(self, value):
        if value == "1":
            raise serializers.ValidationError("You are not authorize to add admin role.")
        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password', 'write_only': True})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            obj = User.objects.get(email=email)
            if not obj.is_active:
                raise serializers.ValidationError('User is in-active, Please cotact your administrator to activate your profile.')
            
            if not check_password(password, obj.password):
                raise serializers.ValidationError('Invalid credentials.')
        except User.DoesNotExist:
            raise serializers.ValidationError('Email address not found.')
        
        data['user'] = obj
        return data
    
    
class UserProfileUpdateSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    name = serializers.CharField()
    bio = serializers.CharField()
    profile_picture = serializers.ImageField(read_only=True)
    contact_number = serializers.CharField()
    user_type = serializers.ChoiceField(required=True, choices=USER_TYPES)
    roles = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)

    def to_representation(self, instance):
       representation = super().to_representation(instance)
       representation['roles'] = RoleSerializer(instance.roles, many=True).data
       return representation
    
    def validate_roles(self, value):
        objs = []
        for role_id in value:
            try:
                ObjectId(role_id)
            except (TypeError, InvalidId):
                raise serializers.ValidationError(f"{role_id} invalid role.")
            try:
                obj = Role.objects.get(id=role_id)
                objs.append(obj)
            except Role.DoesNotExist:
                raise serializers.ValidationError(f'{role_id} is invalid role.')
        return objs

    def update(self, instance, validated_data):       
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
