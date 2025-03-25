from rest_framework import serializers
from .models import Task, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile']
        extra_kwargs = {'password': {'write_only': True}}


# Serializer for creating a Task.
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'task_type']


# Serializer for assigning tasks to users.
class TaskAssignSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    user_ids = serializers.ListField(child=serializers.IntegerField())


# Serializer for retrieving task details.
class TaskDetailSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'task_type', 'completed_at', 'status', 'assigned_users']
