
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import ProtectedError
from django.utils import timezone
from json import loads

from book_app.models import BooksDb, MembersDb, BorrowDb


# BOOKS CRUD

@method_decorator(csrf_exempt, name='dispatch')
class BooksView(View):

    def get(self, request):
        qs = BooksDb.objects.all()

        book_data = []

        for i in qs:
            data = {
                "id": i.id,
                "book_name": i.book_name,
                "author_name": i.author_name,
                "category": i.category,
                "published_year": i.published_year,
                "total_copies": i.total_copies,
                "available_copies": i.available_copies
            }

            book_data.append(data)

        return JsonResponse(book_data, safe=False)

    def post(self, request):
        form_data = loads(request.body)

        book_name = form_data.get('book_name')
        author_name = form_data.get('author_name')
        category = form_data.get('category')
        published_year = form_data.get('published_year')
        total_copies = form_data.get('total_copies')
        available_copies = form_data.get('available_copies')

        if not book_name or not author_name or not category:
            return JsonResponse(
                {"Error": "Required book details are missing"},
                status=400
            )

        if total_copies is None or available_copies is None:
            return JsonResponse(
                {"Error": "Copy details are required"},
                status=400
            )

        if total_copies < 1 or available_copies < 0 or available_copies > total_copies:
            return JsonResponse(
                {"Error": "Invalid book copy details"},
                status=400
            )

        BooksDb.objects.create(
            book_name=book_name,
            author_name=author_name,
            category=category,
            published_year=published_year,
            total_copies=total_copies,
            available_copies=available_copies
        )

        return JsonResponse(
            {"Message": "Book Added Successfully"},
            status=201
        )


@method_decorator(csrf_exempt, name='dispatch')
class BooksRetrieveUpdateDelete(View):

    def get(self, request, pk):
        qs = get_object_or_404(BooksDb, id=pk)

        book_data = {
            "id": qs.id,
            "book_name": qs.book_name,
            "author_name": qs.author_name,
            "category": qs.category,
            "published_year": qs.published_year,
            "total_copies": qs.total_copies,
            "available_copies": qs.available_copies
        }

        return JsonResponse(book_data)

    def put(self, request, pk):
        qs = get_object_or_404(BooksDb, id=pk)
        form_data = loads(request.body)

        total_copies = form_data.get('total_copies')
        available_copies = form_data.get('available_copies')

        if total_copies is None or available_copies is None:
            return JsonResponse(
                {"Error": "Copy details are required"},
                status=400
            )

        if total_copies < 1 or available_copies < 0 or available_copies > total_copies:
            return JsonResponse(
                {"Error": "Invalid book copy details"},
                status=400
            )

        qs.book_name = form_data.get('book_name')
        qs.author_name = form_data.get('author_name')
        qs.category = form_data.get('category')
        qs.published_year = form_data.get('published_year')
        qs.total_copies = total_copies
        qs.available_copies = available_copies

        qs.save()

        return JsonResponse(
            {"Message": "Book Updated Successfully"}
        )

    def delete(self, request, pk):
        qs = get_object_or_404(BooksDb, id=pk)

        try:
            qs.delete()
            return JsonResponse(
                {"Message": "Book Deleted Successfully"}
            )
        except ProtectedError:
            return JsonResponse(
                {"Error": "Cannot delete a book with borrowing records"},
                status=400
            )


# MEMBERS CRUD

@method_decorator(csrf_exempt, name='dispatch')
class MembersView(View):

    def get(self, request):
        qs = MembersDb.objects.all()

        member_data = []

        for i in qs:
            data = {
                "id": i.id,
                "member_name": i.member_name,
                "email": i.email,
                "phone": i.phone,
                "address": i.address,
                "joining_date": i.joining_date
            }

            member_data.append(data)

        return JsonResponse(member_data, safe=False)

    def post(self, request):
        form_data = loads(request.body)

        member_name = form_data.get('member_name')
        email = form_data.get('email')
        phone = form_data.get('phone')
        address = form_data.get('address')

        if not member_name or not email or not phone or not address:
            return JsonResponse(
                {"Error": "All member details are required"},
                status=400
            )

        if MembersDb.objects.filter(email=email).exists():
            return JsonResponse(
                {"Error": "Email already registered"},
                status=400
            )

        MembersDb.objects.create(
            member_name=member_name,
            email=email,
            phone=phone,
            address=address
        )

        return JsonResponse(
            {"Message": "Member Registered Successfully"},
            status=201
        )


@method_decorator(csrf_exempt, name='dispatch')
class MembersRetrieveUpdateDelete(View):

    def get(self, request, pk):
        qs = get_object_or_404(MembersDb, id=pk)

        member_data = {
            "id": qs.id,
            "member_name": qs.member_name,
            "email": qs.email,
            "phone": qs.phone,
            "address": qs.address,
            "joining_date": qs.joining_date
        }

        return JsonResponse(member_data)

    def put(self, request, pk):
        qs = get_object_or_404(MembersDb, id=pk)
        form_data = loads(request.body)

        email = form_data.get('email')

        if MembersDb.objects.filter(email=email).exclude(id=pk).exists():
            return JsonResponse(
                {"Error": "Email already registered"},
                status=400
            )

        qs.member_name = form_data.get('member_name')
        qs.email = email
        qs.phone = form_data.get('phone')
        qs.address = form_data.get('address')

        qs.save()

        return JsonResponse(
            {"Message": "Member Updated Successfully"}
        )

    def delete(self, request, pk):
        qs = get_object_or_404(MembersDb, id=pk)

        try:
            qs.delete()
            return JsonResponse(
                {"Message": "Member Deleted Successfully"}
            )
        except ProtectedError:
            return JsonResponse(
                {"Error": "Cannot delete a member with borrowing records"},
                status=400
            )


# BOOK ISSUE

@method_decorator(csrf_exempt, name='dispatch')
class BorrowView(View):

    def get(self, request):
        qs = BorrowDb.objects.all()

        borrow_data = []

        for i in qs:
            data = {
                "id": i.id,
                "book_id": i.book.id,
                "book_name": i.book.book_name,
                "member_id": i.member.id,
                "member_name": i.member.member_name,
                "issue_date": i.issue_date,
                "return_date": i.return_date,
                "status": i.status
            }

            borrow_data.append(data)

        return JsonResponse(borrow_data, safe=False)

    def post(self, request):
        form_data = loads(request.body)

        book_id = form_data.get('book_id')
        member_id = form_data.get('member_id')

        if book_id is None or member_id is None:
            return JsonResponse(
                {"Error": "Book ID and Member ID are required"},
                status=400
            )

        member = get_object_or_404(MembersDb, id=member_id)

        with transaction.atomic():
            book = get_object_or_404(
                BooksDb.objects.select_for_update(),
                id=book_id
            )

            if book.available_copies <= 0:
                return JsonResponse(
                    {"Error": "Book is not available"},
                    status=400
                )

            book.available_copies -= 1
            book.save()

            BorrowDb.objects.create(
                book=book,
                member=member
            )

        return JsonResponse(
            {"Message": "Book Issued Successfully"},
            status=201
        )


# BORROW DETAILS AND BOOK RETURN

@method_decorator(csrf_exempt, name='dispatch')
class BorrowRetrieveUpdateDelete(View):

    def get(self, request, pk):
        qs = get_object_or_404(BorrowDb, id=pk)

        borrow_data = {
            "id": qs.id,
            "book_id": qs.book.id,
            "book_name": qs.book.book_name,
            "member_id": qs.member.id,
            "member_name": qs.member.member_name,
            "issue_date": qs.issue_date,
            "return_date": qs.return_date,
            "status": qs.status
        }

        return JsonResponse(borrow_data)

    def put(self, request, pk):
        with transaction.atomic():
            qs = get_object_or_404(
                BorrowDb.objects.select_for_update(),
                id=pk
            )

            if qs.status == "Returned":
                return JsonResponse(
                    {"Error": "Book already returned"},
                    status=400
                )

            book = BooksDb.objects.select_for_update().get(id=qs.book_id)

            qs.status = "Returned"
            qs.return_date = timezone.localdate()
            qs.save()

            book.available_copies += 1
            book.save()

        return JsonResponse(
            {"Message": "Book Returned Successfully"}
        )

    def delete(self, request, pk):
        qs = get_object_or_404(BorrowDb, id=pk)

        if qs.status == "Issued":
            return JsonResponse(
                {"Error": "Return the book before deleting its borrowing record"},
                status=400
            )

        qs.delete()

        return JsonResponse(
            {"Message": "Borrowing Record Deleted Successfully"}
        )
