from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from library.models import Book, BookTransaction


class Command(BaseCommand):
    help = 'Notify users when a reserved book becomes available'

    def handle(self, *args, **kwargs):
        available_books = Book.objects.filter(reserved=False, quantity_in_stock__gt=0)

        for book in available_books:
            transactions = BookTransaction.objects.filter(book=book, is_returned=True).order_by('-return_date')[:10]
            for transaction in transactions:
                user = transaction.user
                send_mail(
                    'Book Availability Notification',
                    f'Dear {user.first_name},\n\nThe book "{book.title}" is now available. You can reserve it.',
                    'niagergidze@gmail.com',
                    [user.email],
                    fail_silently=False,
                )

        self.stdout.write(self.style.SUCCESS('Availability notifications have been sent'))
