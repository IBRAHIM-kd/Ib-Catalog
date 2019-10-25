from django.shortcuts import render

# Create your views here.

from .models import Book, Author, ReadedBook

def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = ReadedBook.objects.all().count()
    # Available copies of books
    num_instances_available = ReadedBook.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )

from django.views import generic



class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book


class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


class ReadedBookListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = ReadedBook
    paginate_by = 10


class ReadedBookDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = ReadedBook

from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = ReadedBook
    template_name = 'catalog/readedbook_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ReadedBook.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = ReadedBook
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/readedbook_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return ReadedBook.objects.filter(status__exact='o').order_by('due_back')


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

# from .forms import RenewBookForm
from catalog.forms import RenewBookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific ReadedBook by librarian."""
    readed_book = get_object_or_404(ReadedBook, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            readed_book.due_back = form.cleaned_data['renewal_date']
            readed_book.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'readed_book': readed_book,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)



from django.urls import reverse
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View
from django.contrib.auth.decorators import permission_required



from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

from .forms import BookForm, ReviewForm


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2019'}
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


# Classes created for the forms challenge
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['cover', 'title', 'catagory', 'author' ]
    permission_required = 'catalog.can_mark_returned'


def book_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'catalog/book_form.html', {
        'form': form
    })

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['cover', 'title', 'catagory', 'author' ]
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'


class ReadedBookCreate(PermissionRequiredMixin, CreateView):
    model = ReadedBook
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class ReadedBookUpdate(PermissionRequiredMixin, UpdateView):
    model = ReadedBook
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class ReadedBookDelete(PermissionRequiredMixin, DeleteView):
    model = ReadedBook
    success_url = reverse_lazy('readedbooks')
    permission_required = 'catalog.can_mark_returned'

class ReviewList(View):
    """
    List all of the books that we want to review.
    """
    def get(self, request):
        books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('author')

        context = {
            'books': books,
            'form': BookForm,
        }

        return render(request, "catalog/list-to-review.html", context)

    def post(self, request):
        form = BookForm(request.POST)
        books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('author')

        if form.is_valid():
            form.save()
            return redirect('review-books')

        context = {
            'form':form,
            'books':books,
        }
        return render(request,'catalog/list-to-review.html',context)


def review_book(request, pk):
    """
    Review an individual book
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        # process our form
        form = ReviewForm(request.POST)

        if form.is_valid():
            book.is_favourite = form.cleaned_data['is_favourite']
            book.review = form.cleaned_data['review']
            book.reviewed_by = request.user
            book.save()

            return redirect('review-books')

    else:
        form = ReviewForm

    context = {
        'book': book,
        'form':form,
    }

    return render(request, "catalog/review-book.html", context)


from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from catalog.forms import SignUpForm
from catalog.tokens import account_activation_token



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request,'registration/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


def activate_account(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')
    else:
        return render(request, 'registration/account_activation_invalid.html')


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'registration/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})
