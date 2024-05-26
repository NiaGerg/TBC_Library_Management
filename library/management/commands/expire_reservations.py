from django.core.management.base import BaseCommand
from django.utils import timezone
from library.models import Book


class Command(BaseCommand):
    help = 'Expire book reservations after 1 day'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_books = Book.objects.filter(reserved=True, reserved_at__lt=now - timezone.timedelta(days=1))

        for book in expired_books:
            book.reserved = False
            book.reserved_at = None
            book.save()

        self.stdout.write(self.style.SUCCESS('Expired reservations have been released'))
