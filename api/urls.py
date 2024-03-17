from django.urls import path
from .views import hello,ChatView,ChatHistoryView

urlpatterns = [
    path('hello/', hello.as_view(), name='hello'),
    path('chat/',ChatView.as_view(),name='chat'),
    path('chathistory/',ChatHistoryView.as_view(),name='chat-history')
]