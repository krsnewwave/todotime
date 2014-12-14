from django.conf.urls import url
from django.core.urlresolvers import reverse
from todolist import views
from todolist.models import Note
from todolist.views import NoteUpdate, NoteNew, NoteWeeklyView, NoteMonthlyView

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.user_home, name='user_home'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^new/$', NoteNew.as_view(), name='new'),
    url(r'^reset/(?P<note_id>[0-9]+)/$', views.note_reset, name='reset'),
    url(r'^cancel/(?P<note_id>[0-9]+)/$', views.note_cancel, name='cancel'),
    url(r'^done/(?P<note_id>[0-9]+)/$', views.note_done, name='done'),
    url(r'^edit/(?P<pk>[0-9]+)/$', NoteUpdate.as_view(), name='edit'),
    url(r'^delete/(?P<note_id>[0-9]+)/$', views.note_delete, name='delete'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[^/]+)/week/(?P<week>(?:[1-4]+|All))/$',
        views.user_home, name="note_week"),

    # url(r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$', NoteWeeklyView.as_view(), name="note_week"),
    # url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$', NoteMonthlyView.as_view(month_format='%m'),
    # name="note_month"),
]
