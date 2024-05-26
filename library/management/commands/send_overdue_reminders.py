from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from library.models import BookTransaction


class Command(BaseCommand):
    help = 'Send email reminders for overdue books'

    def handle(self, *args, **kwargs):
        overdue_transactions = BookTransaction.objects.filter(is_returned=False, due_date__lt=timezone.now())

        for transaction in overdue_transactions:
            user = transaction.user
            book = transaction.book
            send_mail(
                'Overdue Book Reminder',
                f'Dear {user.first_name},\n\nThis is a reminder that the book "{book.title}" was due on {transaction.due_date}. Please return it as soon as possible.',
                'niagergidze@gmail.com',
                [user.email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS('Overdue reminders have been sent'))
