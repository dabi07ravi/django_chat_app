from rest_framework import serializers

class CreateChatSerializer(serializers.Serializer):
    receiver_id = serializers.CharField()