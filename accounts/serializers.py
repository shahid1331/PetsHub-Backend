from rest_framework import serializers
from .models import RegisterUser
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = RegisterUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'password',
            'confirmPassword'
        ]
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def validate_phone(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits")
        return value

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        return RegisterUser.objects.create_user(**validated_data)
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data['user'] = user
        return data