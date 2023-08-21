from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    path('', views.index, name = 'index'),
    path('books/', views.BookListView.as_view(), name = 'books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
]

urlpatterns += [path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),]