
from django.db import models

# Create your models here.

class BooksDb(models.Model):
    book_name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    published_year = models.IntegerField()
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.book_name


class MembersDb(models.Model):
    member_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=300)
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.member_name


class BorrowDb(models.Model):
    book = models.ForeignKey(BooksDb, on_delete=models.CASCADE)
    member = models.ForeignKey(MembersDb, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    
    STATUS_CHOICES = (
        ("Issued", "Issued"),
        ("Returned", "Returned"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Issued"
    )

    def __str__(self):
        return f"{self.book.book_name} - {self.member.member_name}"
