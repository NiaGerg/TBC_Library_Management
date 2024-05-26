from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Author, Genre, Book, BookTransaction
from .serializers import AuthorSerializer, GenreSerializer, BookSerializer, BookTransactionSerializer
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, F, Q
from django.core.mail import send_mail
from django.conf import settings
from users.serializers import UserSerializer
from users.models import User


class BookReservation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)

        if book.quantity_in_stock > 0 and not book.reserved:
            book.reserved = True
            book.quantity_in_stock -= 1
            book.save()
            return JsonResponse({"message": "Book reserved successfully"}, status=200)
        else:
            return JsonResponse({"error": "Book not available for reservation"}, status=400)

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)

        if book.reserved:
            book.reserved = False
            book.quantity_in_stock += 1
            book.save()
            return JsonResponse({"message": "Book reservation cancelled"}, status=200)
        else:
            return JsonResponse({"error": "Book is not reserved"}, status=400)


class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetailAPIView(APIView):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)

        serializer = BookSerializer(book)
        return Response(serializer.data)


class BookTransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookTransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_id):
        try:
            transaction = BookTransaction.objects.get(pk=transaction_id)
        except BookTransaction.DoesNotExist:
            return JsonResponse({"error": "Transaction not found"}, status=404)

        transaction.return_date = timezone.now()
        transaction.is_returned = True
        transaction.save()

        book = transaction.book
        book.quantity_in_stock += 1
        book.save()

        return JsonResponse({"message": "Book returned successfully"}, status=200)


class StatisticsAPIView(APIView):
    def get(self, request):
        top_10_books = Book.objects.annotate(transaction_count=Count('booktransaction')).order_by('-transaction_count')[:10]
        books_borrowed_last_year = BookTransaction.objects.filter(issue_date__year=timezone.now().year)
        top_100_books_late_returned = BookTransaction.objects.filter(is_returned=True, return_date__gt=F('due_date')).order_by('-return_date')[:100]
        top_100_users_late_returned = User.objects.annotate(late_returns=Count('booktransaction', filter=Q(booktransaction__return_date__gt=F('booktransaction__due_date')))).order_by('-late_returns')[:100]

        return JsonResponse({
            "top_10_books": BookSerializer(top_10_books, many=True).data,
            "books_borrowed_last_year": BookTransactionSerializer(books_borrowed_last_year, many=True).data,
            "top_100_books_late_returned": BookTransactionSerializer(top_100_books_late_returned, many=True).data,
            "top_100_users_late_returned": UserSerializer(top_100_users_late_returned, many=True).data,
        })


def send_overdue_notification():
    overdue_transactions = BookTransaction.objects.filter(due_date__lt=timezone.now(), is_returned=False)
    for transaction in overdue_transactions:
        user = transaction.user
        book = transaction.book
        send_mail(
            'Overdue Book Notification',
            f'Dear {user.first_name},\n\nYou have an overdue book: {book.title}. Please return it as soon as possible.\n\nThank you.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
