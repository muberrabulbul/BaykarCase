from django.contrib.auth import password_validation as validators
from django.contrib.auth.models import User
from django.core import exceptions
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for user that serialize "url", "username", "email",
    "password", "password2" and relation to profile serializer
    """

    url = serializers.HyperlinkedIdentityField(view_name="users-detail")
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=False,
    )
    password2 = serializers.CharField(
        label="Confirm password",
        write_only=True,
        style={"input_type": "password"},
        required=False,
    )

    class Meta:
        model = User
        fields = ("url", "username", "email", "password", "password2")

    def validate_password2(self, value):
        """
        Checks if password2 is the same as password
        """
        data = self.get_initial()
        password = data.get("password")
        password2 = value
        if password != password2:
            raise ValidationError("Passwords must match")
        return super(UserSerializer, self).validate(value)

    def validate_password(self, value):
        """
        Validates password by django validators
        """
        password = value
        errors = dict()
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)
            if errors:
                raise serializers.ValidationError(errors)
        return super(UserSerializer, self).validate(value)

    def create(self, validated_data):
        """
        Creates user and related profile instance
        """
        email = validated_data.get("email")
        username = validated_data.get("username")
        password = validated_data.get("password")

        if not email:
            raise ValidationError({"email": "This field is required."})
        if not username:
            raise ValidationError({"username": "This field is required."})
        if not password:
            raise ValidationError({"password": "This field is required."})

        user = User.objects.create_user(
            email=email, username=username, password=password
        )

        return user

    def update(self, instance, validated_data):
        nested_serializer = self.fields["profile"]
        nested_instance = instance.profile
        nested_data = validated_data.pop("profile")
        nested_serializer.update(nested_instance, nested_data)
        if "password" in validated_data:
            validated_data.pop("password")

        return super(UserSerializer, self).update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Kullanıcı adı veya şifre yanlış.")

        return attrs
