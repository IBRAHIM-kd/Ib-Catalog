from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Book
from django import forms


class ReviewForm(forms.Form):
    """
    Form for reviewing a book
    """

    is_favourite = forms.BooleanField(
        label="Favourite?",
        help_text="In your top 100",
        required=False,
    )

    review = forms.CharField(
        widget=forms.Textarea,
        min_length=300,
        error_messages={
            'required':'Please enter your review',
            'min_length': 'Please write at least 300 characters (you have written %(show_value)s)'
        }
    )


class RenewBookForm(forms.Form):
    """Form for a Book Catalog to renew books."""
    renewal_date = forms.DateField(
            help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        # Check date is in range book catalog allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'cover', 'catagory', 'reviewed_by']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

