from django.urls import path
from .views import (BookReservation, BookListAPIView, BookDetailAPIView, BookTransactionAPIView,
                    ReturnBookAPIView, StatisticsAPIView)

urlpatterns = [
    path('books/<int:book_id>/reserve/', BookReservation.as_view(), name='book-reserve'),
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:book_id>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('transactions/', BookTransactionAPIView.as_view(), name='book-transaction'),
    path('transactions/<int:transaction_id>/return/', ReturnBookAPIView.as_view(), name='return-book'),
    path('statistics/', StatisticsAPIView.as_view(), name='statistics'),
]
