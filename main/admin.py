from django.contrib import admin
from django import forms

from .models import *


class NotebookCategoryChoiceField(forms.ModelChoiceField):
    pass


class NotebookAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Категория в качестве внешнего ключа """
        if db_field.name == 'category':
            # фильтруем по slug notebooks
            return NotebookCategoryChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Категория в качестве внешнего ключа """
        if db_field.name == 'category':
            # фильтруем по slug smartphones
            return NotebookCategoryChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(NoteBook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartProduct)
