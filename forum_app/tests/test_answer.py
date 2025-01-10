from django.contrib.auth.models import User
from django.urls import reverse
from forum_app.models import Answer, Question
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

class AnswerTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Text Question', content='Test Content', author=self.user, category='frontend')
        self.answer = Answer.objects.create(content='Test Content', author=self.user, question=self.question)
        
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        
    def test_answer_list_url(self):
        url = reverse('answer-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_answer_detail_url(self):
        url = reverse('answer-detail', kwargs={'pk': self.answer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)