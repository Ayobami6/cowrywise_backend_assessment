from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book


User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
        
        
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        
        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        return user
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        
        
        
    
