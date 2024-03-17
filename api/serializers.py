from rest_framework import serializers
from chat.models import UserChat

class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ('id','user','message','timestamp','pdf_file','bot_response')
        
