from django.conf.urls import url
from . import views

urlpatterns = [
    #appointment urls are based on their id
    url(r'^appointments/(?P<pk>[0-9]+)/$', views.AppointmentView, name='appointments'),
    #calendar day urls are based on day, month, and year, of the form 'cal/15/6/2016' for the 15th of June 2016
    url(r'^cal/(?P<day>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]+)/$', views.CalendarDayView, name='calendarDay'),
    #calendar month urls are based on month and year, of the form 'cal/10/2016' for October 2016's calendar
    url(r'^cal/(?P<month>[0-9]+)/(?P<year>[0-9]+)/$', views.CalendarMonthView, name='calendarMonth'),
    #The calendar week url is just like the calendar day url, but with the word week in front of it
    url(r'^cal/week/(?P<day>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]+)/$', views.CalendarWeekView, name='calendarWeek'),
    #making an appointment
    url(r'^cal/makeAppointment/$', view=views.makeAppointment, name='makeAppointment'),
    #redirects to the current month view when just cal is entered
    url(r'^cal/$', view=views.redirectView, name='redirect'),
    #editing an appointment
    url(r'^cal/editAppointment/(?P<pk>[0-9]+)/$', view=views.editAppointment, name='edit appointment'),
    #confirm deleting an appointment
    url(r'^cal/confirmation/(?P<pk>[0-9]+)/$', view=views.deleteAppointment, name='confirm delete'),
    #deletes appointment
    url(r'^cal/delete/(?P<pk>[0-9]+)/$', view=views.delete, name='delete'),
]