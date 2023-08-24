from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings
from typing import Any, Dict
from django.views import generic, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

def set_language(request, language_code):
    if language_code in [lang[0] for lang in settings.LANGUAGES]:
        activate(language_code)
        request.session['django_language'] = language_code
    return redirect(request.META.get('HTTP_REFERER', '/'))

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class MyView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_mark_returned'  # Or multiple permissions: ('catalog.can_mark_returned', 'catalog.can_edit')

    def get(self, request, *args, **kwargs):
        # Your view code for the HTTP GET request
        pass

    def post(self, request, *args, **kwargs):
        # Your view code for the HTTP POST request
        pass
