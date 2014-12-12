from django.contrib import admin
from todolist.models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'date_posted', 'date_due')


admin.site.register(Note, NoteAdmin)
