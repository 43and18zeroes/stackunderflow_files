from django.contrib.auth.models import User
from django.urls import reverse
from forum_app.models import Answer, Question
from rest_framework import status
from rest_framework.test import APITestCase

class AnswerTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Text Question', content='Test Content', author=self.user, category='frontend')
        self.answer = Answer.objects.create(content='Test Content', author=self.user, question=self.question)
        
        
    def test_answer_list_url(self):
        url = reverse('answer-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    # def test_answer_detail_url(self):
    #     answer_id = 1
    #     url = reverse('answer-detail', kwargs={'pk': answer_id})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 404)  # Wenn kein Eintrag existiert