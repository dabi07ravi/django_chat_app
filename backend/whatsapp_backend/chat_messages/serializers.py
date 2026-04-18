from rest_framework import serializers

class SendMessageSerializer(serializers.Serializer):
    chat_id = serializers.CharField()
    content = serializers.CharField()