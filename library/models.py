from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    date_of_issue = models.DateField()
    quantity_in_stock = models.PositiveIntegerField()
    reserved = models.BooleanField(default=False)
    reserved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class BookTransaction(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.due_date = self.issue_date + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Book Transaction"
        verbose_name_plural = "Book Transactions"
