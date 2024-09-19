from rest_framework import serializers
from .models import Book, Category


class AddBookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=50)
    publisher = serializers.CharField(max_length=50)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'category')
        
        
