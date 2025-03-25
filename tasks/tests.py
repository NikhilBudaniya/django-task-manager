from django.urls import reverse
from tasks.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from tasks.models import Task


class BaseAPITestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            email='testuser1@gmail.com',
            password='password123',
            name='Test User 1',
            mobile='1234567890'
        )
        self.user2 = User.objects.create_user(
            email='testuser2@gmail.com',
            password='password123',
            name='Test User 2',
            mobile='1234567890'
        )

        # Create test tasks
        self.task1 = Task.objects.create(
            title='Test Task 1',
            description='Description for test task 1',
            status='pending',
            task_type='feature'
        )

        self.task2 = Task.objects.create(
            title='Test Task 2',
            description='Description for test task 2',
            status='in_progress',
            task_type='bug'
        )

        # Assign users to tasks
        self.task1.assigned_users.add(self.user1)
        self.task2.assigned_users.add(self.user1, self.user2)


# Task API Tests
class TaskAPITestCase(BaseAPITestCase):
    def test_task_list(self):
        """Test fetching all tasks"""
        url = reverse('all_tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_task_detail(self):
        """Test fetching a specific task"""
        url = reverse('task_detail', kwargs={'task_id': self.task1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task 1')

        # Test with invalid task ID
        url = reverse('task_detail', kwargs={'task_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_create(self):
        """Test creating a new task"""
        url = reverse('create_task')
        data = {
            'title': 'New Test Task',
            'description': 'New test task description',
            'status': 'pending',
            'task_type': 'feature'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

        # Test with invalid data
        invalid_data = {
            'title': '',  # Empty title should fail validation
            'status': 'invalid_status'  # Invalid status
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_update(self):
        """Test updating a task's status"""
        url = reverse('update_task', kwargs={'task_id': self.task1.id})
        data = {'status': 'in_progress'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'in_progress')

        # Test with invalid status
        data = {'status': 'invalid_status'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test completing a task
        data = {'status': 'completed'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'completed')
        self.assertIsNotNone(self.task1.completed_at)

    def test_task_delete(self):
        """Test deleting a task"""
        url = reverse('delete_task', kwargs={'task_id': self.task1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

        # Test deleting non-existent task
        url = reverse('delete_task', kwargs={'task_id': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_filter(self):
        """Test filtering tasks"""
        # Filter by status
        url = reverse('filter_tasks') + '?status=pending'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'pending')

        # Filter by task_type
        url = reverse('filter_tasks') + '?task_type=bug'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['task_type'], 'bug')

        # Search by title or description
        url = reverse('filter_tasks') + '?search=test task 1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task 1')


# User API Tests
class UserAPITestCase(BaseAPITestCase):
    def test_user_list(self):
        """Test fetching all users"""
        url = reverse('all_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_detail(self):
        """Test fetching a specific user"""
        url = reverse('user_detail', kwargs={'user_id': self.user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test User 1')

        # Test with invalid user ID
        url = reverse('user_detail', kwargs={'user_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_update(self):
        """Test updating a user"""
        url = reverse('update_user', kwargs={'user_id': self.user1.id})
        data = {'name': 'Updated', 'mobile': '1023456789'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.name, 'Updated')
        self.assertEqual(self.user1.mobile, '1023456789')

        # Test with invalid user ID
        url = reverse('update_user', kwargs={'user_id': 9999})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_delete(self):
        """Test deleting a user"""
        url = reverse('delete_user', kwargs={'user_id': self.user1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

        # Test deleting non-existent user
        url = reverse('delete_user', kwargs={'user_id': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Task Assignment API Tests
class TaskAssignmentTestCase(BaseAPITestCase):
    def test_assign_task(self):
        """Test assigning a task to users"""
        url = reverse('assign_task')
        data = {
            'task_id': self.task1.id,
            'user_ids': [self.user2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.assigned_users.count(), 2)

        # Test with invalid task ID
        data['task_id'] = 9999
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test with invalid user IDs
        data = {
            'task_id': self.task1.id,
            'user_ids': [9999]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_users(self):
        """Test getting users assigned to a task"""
        url = reverse('task_users', kwargs={'task_id': self.task2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Test with invalid task ID
        url = reverse('task_users', kwargs={'task_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_tasks(self):
        """Test getting tasks assigned to a user"""
        url = reverse('user_tasks', kwargs={'user_id': self.user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Test with invalid user ID
        url = reverse('user_tasks', kwargs={'user_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Task Stats API Tests
class TaskStatsTestCase(BaseAPITestCase):
    def test_task_stats(self):
        """Test retrieving task statistics"""
        url = reverse('task_stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tasks'], 2)
        self.assertEqual(len(response.data['by_status']), 2)
        self.assertEqual(len(response.data['by_type']), 2)
        self.assertEqual(response.data['by_status'].get('pending', 0), 1)
        self.assertEqual(response.data['by_status'].get('in_progress', 0), 1)
        self.assertEqual(response.data['by_type'].get('feature', 0), 1)
        self.assertEqual(response.data['by_type'].get('bug', 0), 1)
