"""
URL configuration for librarymanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from book_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', views.BooksView.as_view()),
    path('books/<int:pk>/', views.BooksRetrieveUpdateDelete.as_view()),
    path('members/', views.MembersView.as_view()),
    path('members/<int:pk>/', views.MembersRetrieveUpdateDelete.as_view()),
    path('borrow/', views.BorrowView.as_view()),
    path('borrow/<int:pk>/', views.BorrowRetrieveUpdateDelete.as_view()),
]
