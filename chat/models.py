from django.db import models

from django.contrib.auth.models import User

class UserChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    bot_response=models.TextField(null=True)
    

    


