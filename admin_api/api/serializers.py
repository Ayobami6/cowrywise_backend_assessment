from rest_framework import serializers
from .models import Book, Category, BorrowedBookLog, User


class AddBookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=50)
    publisher = serializers.CharField(max_length=50)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'category')
        
        
class GetBookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = "__all__"
        
        
class BorrowedBookSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source="book.title")
    
    class Meta:
        model = BorrowedBookLog
        fields = ("book_title", "borrow_date", "return_date")
        

class GetUserSerializer(serializers.ModelSerializer):
    borrowed_books = BorrowedBookSerializer(many=True)
    
    class Meta:
        model = User
        fields = ("id", "email", "borrowed_books")
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        full_name = instance.full_name
        
        rep["full_name"] = full_name
        
        return rep
