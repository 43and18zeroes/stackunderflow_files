from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from forum_app.models import Question
from forum_app.api.serializers import QuestionSerializer
from rest_framework.authtoken.models import Token     
        
class QuestionTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Text Question', content='Test Content', author=self.user, category='frontend')
        # self.client = APIClient()
        # self.client.login(username='testuser', password='testpassword')
        
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    
    def test_list_post_question(self):
        url = reverse('question-list')
        data = {'title':'Question1',
                'content':'1Content',
                'author': self.user.id,
                'category':'frontend'}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def test_detail_question(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        response = self.client.get(url)
        expected_data = QuestionSerializer(self.question).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_data)
        self.assertJSONEqual(response.content, expected_data)
        self.assertContains(response, 'title')
        
        self.question = Question.objects.create(title='Text Question', content='Test Content', author=self.user, category='frontend')
        self.assertEqual(Question.objects.count(), 2)
        # self.assertEqual(Question.objects.get().author, self.user)