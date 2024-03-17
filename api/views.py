from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from chat.models import UserChat
from .serializers import UserChatSerializer
from django.http import JsonResponse
from .langchain_utils import answer_user_question
class hello(View):
    def get(self, request):
        return HttpResponse("Hello, World!")


class ChatView(generics.CreateAPIView):
    queryset = UserChat.objects.all() 
    serializer_class = UserChatSerializer
    permission_classes=[IsAuthenticated]
    def perform_create(self, serializer):
        instance = serializer.save()  # Save the instance first
        text = instance.message  # Access the message attribute of the saved instance
        pdf = instance.pdf_file  # Access the pdf_file attribute of the saved instance
        bot_response = answer_user_question(pdf,text)  # Assuming man() is a function that returns bot response
        serializer.save(user=self.request.user,bot_response=bot_response) 


class ChatHistoryView(generics.ListAPIView):
    queryset=UserChat.objects.all()
    serializer_class=UserChatSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return UserChat.objects.filter(user=self.request.user)
    
    
    
    