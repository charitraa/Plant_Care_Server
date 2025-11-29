from django.contrib.auth import get_user_model
from rest_framework import serializers
import re

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with all required validations.
    All errors return as {"message": "..."}.
    """
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if not re.match(r'^[a-zA-Z0-9_]{3,30}$', value):
            raise serializers.ValidationError(
                "Username must be 3-30 characters long and contain only letters, numbers, and underscores."
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_password(self, value):
        errors = []
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            errors.append("Password must contain at least one digit.")
        if not re.search(r'[A-Z]', value):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            errors.append("Password must contain at least one special character.")

        if errors:
            raise serializers.ValidationError(" ".join(errors))
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','password']

    def update(self, instance, validated_data):
        # Prevent duplicate emails
        if 'email' in validated_data and User.objects.filter(email=validated_data['email']).exclude(id=instance.id).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        # Prevent duplicate usernames
        if 'username' in validated_data and User.objects.filter(username=validated_data['username']).exclude(id=instance.id).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})

        # Update fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # ⚠️ IMPORTANT: Password handling
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Use set_password to hash

        instance.save()
        return instance