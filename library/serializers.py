from rest_framework import serializers
from .models import Author, Genre, Book, BookTransaction


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'date_of_issue', 'quantity_in_stock']


class BookTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTransaction
        fields = ['id', 'user', 'book', 'issue_date', 'return_date', 'due_date', 'is_returned']
