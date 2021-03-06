from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

from django.urls import reverse  # To generate URLS by reversing URL patterns


class Book(models.Model):

    CATAGORY_CHOICES =[
	('Science book', 'Science books'),
	('English book', 'English books'),
	('Biology book', 'Biology books'),
	]
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='books/covers/', null=True,blank=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    catagory = models.CharField(max_length=200, choices=CATAGORY_CHOICES)
    review = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')
    date_reviewed = models.DateTimeField(blank=True,null=True)
    is_favourite = models.BooleanField(default=False, verbose_name="Favourite?")

    def display_catagory(self):
        """Creates a string for the Catagory. This is required to display catagory in Admin."""
        return ', '.join([catagory.name for catagory in self.catagory.all()[:3]])

    display_catagory.short_description = 'Catagory'

    def get_absolute_url(self):
        """Returns the url to access a particular readed book."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a borrower


class ReadedBook(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed and read from the from the books Catalog Application)."""
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('readedbook-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)



@receiver(post_save, sender=User)
def update_user (sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)
    instance.user.save()
