from django.contrib import admin

# Register your models here.

from .models import Author, Catagory, Book, ReadedBook

"""Minimal registration of Models.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(ReadedBook)
admin.site.register(Catagory)
"""

admin.site.register(Catagory)


class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Administration object for Author models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields),
       grouping the date fields horizontally
     - adds inline addition of books in author view (inlines)
    """
    list_display = ('last_name',
                    'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]


class ReadedsBookInline(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = ReadedBook


class BookAdmin(admin.ModelAdmin):
    """Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of book instances in book view (inlines)
    """
    list_display = ('cover''title', 'author', 'catagory')
    inlines = [ReadedsBookInline]


admin.site.register(Book, BookAdmin)


@admin.register(ReadedBook)
class ReadedBookAdmin(admin.ModelAdmin):
    """Administration object for ReadedBook models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
     - grouping of fields into sections (fieldsets)
    """
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
