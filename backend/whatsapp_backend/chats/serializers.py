from rest_framework import serializers

class CreateChatSerializer(serializers.Serializer):
    receiver_id = serializers.CharField()


class CreateGroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    users = serializers.ListField(child=serializers.CharField())

class AddMemberSerializer(serializers.Serializer):
    chat_id = serializers.CharField()
    user_id = serializers.CharField()


class RemoveMemberSerializer(serializers.Serializer):
    chat_id = serializers.CharField()
    user_id = serializers.CharField()