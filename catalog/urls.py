from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    path('', views.index, name = 'index'),
    path('set-language/<str:language_code>/', views.set_language, name='set_language'),
    path('books/', views.BookListView.as_view(), name = 'books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
]
