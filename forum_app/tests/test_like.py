from django.contrib.auth.models import User
from forum_app.models import Like, Question
from rest_framework import status
from rest_framework.test import APITestCase

class LikeTests(APITestCase):
    
    # def test_get_like(self):
    #     url = "http://127.0.0.1:8000/api/forum/likes/"
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.question = Question.objects.create(
            author=self.user, title="Test Question", content="Test Content"
        )
        self.url = "/api/forum/likes/"
   
    def test_get_likes_list(self):
        url = "http://127.0.0.1:8000/api/forum/likes/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
    def test_get_single_like(self):
        like = Like.objects.create(user=self.user, question=self.question)
        url = f"/api/forum/likes/{like.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], like.id)