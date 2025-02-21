
from user.models import CustomUser
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'passowd':{'write_only':True}}

    def validata_password(self, value):
        if len(value) < 8 :
            raise serializers.ValidationError(" The password must be greater than or equal to 8 characters.")
        return value

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







