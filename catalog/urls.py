from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required




from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
	path('readedbooks/', views.ReadedBookListView.as_view(), name='readedbooks'),
    path('readedbook/<int:pk>', views.ReadedBookDetailView.as_view(), name='readedbook-detail'),
]

urlpatterns += [
    path('readedbook/create/', views.ReadedBookCreate.as_view(), name='readedbook_create'),
    path('readedbook/<int:pk>/update/', views.ReadedBookUpdate.as_view(), name='readedbook_update'),
    path('readedbook/<int:pk>/delete/', views.ReadedBookDelete.as_view(), name='readedbook_delete'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),  # Added for challenge
]


# Add URLConf for librarian to renew a book.
urlpatterns += [
    path('book/<int:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]


# Add URLConf to create, update, and delete authors
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]

# Add URLConf to create, update, and delete books
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]


urlpatterns += [
   path(r'^signup/$',  views.signup, name='signup'),
   path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
   path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
   path(r'^review/$', login_required(views.ReviewList.as_view()), name='review-books'),
   path(r'^review/(?P<pk>[-\w]+)/$', views.review_book, name='review-book'),
]

