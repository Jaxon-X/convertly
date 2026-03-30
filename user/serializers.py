
from user.models import CustomUser
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_email_verified']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_email_verified': {'read_only': True},
        }

    def validate_password(self, value):
        if len(value) < 8 :
            raise serializers.ValidationError(" The password must be greater than or equal to 8 characters.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=True)
    password = serializers.CharField(max_length=128, write_only=True, allow_blank=True)







