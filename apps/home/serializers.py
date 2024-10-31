# serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['sender', 'recipient', 'title', 'message', 'timestamp', 'read', 'notification_type']
