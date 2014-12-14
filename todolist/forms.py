from django import forms
from django.contrib.auth.models import User
from django.forms.extras import SelectDateWidget
from todolist import DateFilterWidget

from todolist.models import Note


__author__ = 'Dylan'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class NewNoteForm(forms.ModelForm):
    date_due = forms.DateTimeField(widget=SelectDateWidget)

    class Meta:
        model = Note
        fields = ('text', 'is_done', 'is_cancelled', 'date_due')


class UpdateNoteForm(forms.ModelForm):
    date_due = forms.DateTimeField(widget=SelectDateWidget)

    class Meta:
        model = Note
        fields = ('text', 'date_due')


class MonthWeekForm(forms.Form):
    month = forms.DateField(widget=DateFilterWidget)