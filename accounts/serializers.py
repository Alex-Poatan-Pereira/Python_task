from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "password", "nickname", "roles")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            nickname=validated_data["nickname"]
        )
        return user

    def get_roles(self, obj):
        return [{"role": obj.role}]