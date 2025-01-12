from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .throttling import QuestionThrottle, QuestionGetThrottle, QuestionPostThrottle
from forum_app.models import Like, Question, Answer
from rest_framework import viewsets, generics, permissions
from rest_framework.throttling import ScopedRateThrottle

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'question-scope'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_throttles(self):
    #     if self.action == 'list' or self.action == 'retriev':
    #         return [QuestionGetThrottle()]
        
    #     if self.action == 'create':
    #         return [QuestionPostThrottle()]
        
    #     return []
        

class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]