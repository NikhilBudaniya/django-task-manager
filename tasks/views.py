from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Task
from .serializers import TaskCreateSerializer, TaskAssignSerializer, TaskDetailSerializer, UserSerializer
from django.utils import timezone
from django.db.models import Count


# API to create a new user.
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to create a new task.
class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to assign a task to one or more users.
class TaskAssignView(APIView):
    def post(self, request):
        serializer = TaskAssignSerializer(data=request.data)
        if serializer.is_valid():
            task_id = serializer.validated_data['task_id']
            user_ids = serializer.validated_data['user_ids']
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

            users = User.objects.filter(id__in=user_ids)
            if not users.exists():
                return Response({'message': 'No users found'}, status=status.HTTP_404_NOT_FOUND)

            # Assign Users to Task
            task.assigned_users.add(*users)
            task.save()
            serializer = TaskDetailSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to get tasks assigned to a user.
class UserTasksView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        tasks = user.assigned_tasks.all()  # Reverse relation from ManyToManyField
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API to get users assigned to a task.
class TaskUsersView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        users = task.assigned_users.all()  # Reverse relation from ManyToManyField
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API to get all tasks.
class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API to get all users.
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API to get a task by ID.
class TaskDetailView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API to get a user by ID.
class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Update task status by ID.
class TaskUpdateView(APIView):
    def patch(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if 'status' in request.data:
            if request.data['status'] not in dict(Task.TASK_STATUS).keys():
                return Response({'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

            task.status = request.data['status']
            if request.data['status'] == 'completed':
                task.completed_at = timezone.now()
                task.status = 'completed'
            else:
                task.status = request.data['status']
            task.save()
            serializer = TaskDetailSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Status not provided'}, status=status.HTTP_400_BAD_REQUEST)


# Update user details by ID.
class UserUpdateView(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update task details by ID.
class TaskUpdateDetailsView(APIView):
    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskCreateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete task by ID.
class TaskDeleteView(APIView):
    def delete(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Delete user by ID.
class UserDeleteView(APIView):
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Filter tasks.
class TaskFilterView(APIView):
    def get(self, request):
        tasks = Task.objects.all()

        status_filter = request.query_params.get('status')
        if status_filter:
            tasks = tasks.filter(status=status_filter)

        task_type_filter = request.query_params.get('task_type')
        if task_type_filter:
            tasks = tasks.filter(task_type=task_type_filter)

        search_term = request.query_params.get('search')
        if search_term:
            tasks = tasks.filter(title__icontains=search_term) | tasks.filter(description__icontains=search_term)

        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Get task statistics.
class TaskStatsView(APIView):
    def get(self, request):
        stats = {
            'total_tasks': Task.objects.count(),
            'by_status': dict(Task.objects.values('status').annotate(count=Count('id')).values_list('status', 'count')),
            'by_type': dict(Task.objects.values('task_type').annotate(count=Count('id')).values_list('task_type', 'count'))
        }
        return Response(stats, status=status.HTTP_200_OK)

# API to assign a user to one or more tasks.
class UserAssignView(APIView):
    def post(self, request):
        serializer = TaskAssignSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            task_ids = serializer.validated_data['task_ids']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            tasks = Task.objects.filter(id__in=task_ids)
            if not tasks.exists():
                return Response({'message': 'No tasks found'}, status=status.HTTP_404_NOT_FOUND)

            # Assign Tasks to User
            user.assigned_tasks.add(*tasks)
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
