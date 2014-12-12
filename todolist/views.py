from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.datetime_safe import date
from django.views.generic import UpdateView, CreateView
from django.contrib.auth import authenticate, login, logout

from todolist.forms import UserForm, NewNoteForm, UpdateNoteForm
from todolist.models import Note


def index(request):
    # TODO: after login, displays ALL the user's notes
    notes = Note.objects.order_by('-date_due')
    output = {'notes': notes}

    return render(request, 'todolist/list.html', output)


def register(request):
    """Registers accounts"""
    context = RequestContext(request)
    registered = False

    # POST method
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors)

    # if GET, then we render
    else:
        user_form = UserForm()

    return render_to_response('todolist/register.html',
                              {'user_form': user_form, 'registered': registered}, context)


def login_user(request):
    """Logs in the user"""

    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "Logged in."
                return HttpResponseRedirect('/todolist/')
            else:
                state = "Account not active. Contact admin."
        else:
            state = "Credentials invalid."
        return render_to_response('todolist/auth.html', {'state': state, 'username': username}, context)
    else:
        return render_to_response('todolist/auth.html', {'state': "Please login!", 'username': ""}, context)


@login_required(login_url='/todolist/login/')
def user_home(request):
    """Defines the user's home page. Shows a tabular representation of the user's documents"""
    user = request.user
    user_notes = Note.objects.filter(user_id=user.id)
    # sorted_user_notes = sorted(user_notes, key=lambda note: note.date_posted)
    # Entry.objects.filter(blog_id=4)

    #+1 day rule.
    curr_date = date.today()
    for user_note in user_notes:
        if (not user_note.is_cancelled or not user_note.is_done) and user_note.date_due.date() < curr_date:
            user_note.date_due = curr_date + timedelta(days=1)

    return render(request, 'todolist/list.html',
                  {'notes': sorted(user_notes, key=lambda note: note.date_posted, reverse=True)})


@login_required
def user_logout(request):
    """Defines logout request"""
    logout(request)
    return HttpResponseRedirect('/todolist/')


@login_required
def note_cancel(request, note_id):
    """Defines cancelling a user's notes"""
    try:
        note = Note.objects.get(pk=note_id)
        note.is_cancelled = True
        note.save()
    except Note.DoesNotExist:
        raise Http404

    return HttpResponseRedirect('/todolist/')


@login_required
def note_done(request, note_id):
    """Defines marking done a user's notes"""
    try:
        note = Note.objects.get(pk=note_id)
        note.is_done = True
        note.save()
    except Note.DoesNotExist:
        raise Http404

    return HttpResponseRedirect('/todolist/')


@login_required
def note_reset(request, note_id):
    """Defines resetting the status of a user's notes"""
    try:
        note = Note.objects.get(pk=note_id)
        note.is_done = False
        note.is_cancelled = False
        note.save()
    except Note.DoesNotExist:
        raise Http404

    return HttpResponseRedirect('/todolist/')


@login_required
def note_delete(request, note_id):
    """Defines deleting a note"""
    try:
        note = Note.objects.get(pk=note_id)
        note.delete()
    except Note.DoesNotExist:
        raise Http404

    return HttpResponseRedirect('/todolist/')


@login_required
def note_new(request):
    context = RequestContext(request)
    if request.method == 'POST':
        note_form = NewNoteForm(data=request.POST)
        if note_form.is_valid():
            new_note = Note()
            new_note.text = note_form.cleaned_data['text']
            new_note.is_cancelled = False
            new_note.is_done = False
            new_note.date_posted = date.today()
            new_note.date_due = note_form.cleaned_data['date_due']
            new_note.save()

            return HttpResponseRedirect('/todolist/')
        else:
            print(note_form.errors)

    else:
        note_form = NewNoteForm()
    return render_to_response('todolist/new_note.html', {'form': note_form}, context)


class NoteNew(CreateView):
    model = Note
    fields = ['text', 'date_due']
    form_class = NewNoteForm
    template_name_suffix = "_create_form"

    def form_valid(self, form):
        note = form.save(commit=False)
        note.user = self.request.user
        note.save()
        return HttpResponseRedirect('/todolist/')


class NoteUpdate(UpdateView):
    model = Note
    fields = ['text', 'date_due']
    template_name_suffix = "_update_form"
    form_class = UpdateNoteForm
    success_url = '/todolist/'




