from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)  

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)