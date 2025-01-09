from django.contrib.auth.models import User
from forum_app.models import Like, Question
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

class LikeTests(APITestCase):
    
    # def test_get_like(self):
    #     url = "http://127.0.0.1:8000/api/forum/likes/"
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Text Question', content='Test Content', author=self.user, category='frontend')
        self.url = "http://127.0.0.1:8000/api/forum/likes/"
        
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
   
    def test_get_likes_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
    def test_get_single_like(self):
        like = Like.objects.create(user=self.user, question=self.question)
        url = f"{self.url}{like.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], like.id)
        
    def test_create_like(self):
        self.client.force_authenticate(user=self.user)
        data = {"question": self.question.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.first().user, self.user)
        
    def test_delete_like(self):
        like = Like.objects.create(user=self.user, question=self.question)
        url = f"{self.url}{like.id}/"
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)