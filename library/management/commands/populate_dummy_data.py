from django.core.management.base import BaseCommand
from faker import Faker

#I know this imports looks like incorrect but this is the only way for correct data....
from library.models import Author, Genre, Book
from users.models import User


class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Populate users
        for _ in range(10):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                personal_number=fake.unique.random_number(digits=10),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=90),
            )

        # Populate authors
        for _ in range(40):
            Author.objects.create(
                name=fake.name()
            )

        # Populate genres
        for _ in range(5):
            Genre.objects.create(
                name=fake.word()
            )

        # Populate books
        for _ in range(200):
            title = fake.catch_phrase()
            author = Author.objects.order_by('?').first()
            genre = Genre.objects.order_by('?').first()
            date_of_issue = fake.date_this_century()
            quantity_in_stock = fake.random_int(min=1, max=50)
            Book.objects.create(
                title=title,
                author=author,
                genre=genre,
                date_of_issue=date_of_issue,
                quantity_in_stock=quantity_in_stock
            )

        self.stdout.write(self.style.SUCCESS('Dummy data populated successfully'))
