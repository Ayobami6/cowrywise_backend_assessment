from django.contrib import admin
from .models import User, Book, BorrowedBookLog, Category
# Register your models here.

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Category)

@admin.register(BorrowedBookLog)
class BorrowedBookLogAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'book', 'borrow_date', 'return_date')
