from django.views import generic
from .models import Appointment
from django.template import loader
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import calendar
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from users.models import endUser, Hospital
from django.utils import timezone

def getHospitalID(username):
    for obj in Hospital.objects.all():
        for u in obj.patients.split(","):
            if u == username:
                return obj.id
        for u in obj.doctors.split(","):
            if u == username:
                return obj.id
        for u in obj.nurses.split(","):
            if u == username:
                return obj.id
        for u in obj.secretaries.split(","):
            if u == username:
                return obj.id
        for u in obj.admins.split(","):
            if u == username:
                return obj.id

@login_required()
def AppointmentView(request, pk):
    """
    Users with appropriate permissions can view appointment information
    """


    user = request.user
    if len(Appointment.objects.filter(id=pk)) != 1:
        return redirect('/cal')

    ap = Appointment.objects.filter(id=pk)[0]
    hospitals = (Hospital.objects.filter(id=ap.location))
    hospital = hospitals[0].Name
    if user.enduser.isPatient and (user.enduser.id == ap.patientID):
        return render(request, 'cal/appointment.html', {'appointment' : ap,
                                                        'doctor' : endUser.objects.filter(id=ap.doctorID)[0],
                                                        'patient' : endUser.objects.filter(id=ap.patientID)[0],
                                                        'user' : user,
                                                        'hospital' : hospital})
    elif user.enduser.isDoctor and (user.enduser.id == ap.doctorID):
        return render(request, 'cal/appointment.html', {'appointment' : ap,
                                                        'doctor' : endUser.objects.filter(id=ap.doctorID)[0],
                                                        'patient' : endUser.objects.filter(id=ap.patientID)[0],
                                                        'user' : user,
                                                        'hospital' : hospital})
    elif user.enduser.isSecretary:
        return render(request, 'cal/appointment.html', {'appointment' : ap,
                                                        'doctor' : endUser.objects.filter(id=ap.doctorID)[0],
                                                        'patient' : endUser.objects.filter(id=ap.patientID)[0],
                                                        'user' : user,
                                                        'hospital' : hospital})
    elif user.enduser.isNurse and (ap.begins - timezone.now() < datetime.timedelta(days = 7)):
        return render(request, 'cal/appointment.html', {'appointment' : ap,
                                                        'doctor' : endUser.objects.filter(id=ap.doctorID)[0],
                                                        'patient' : endUser.objects.filter(id=ap.patientID)[0],
                                                        'user' : user,
                                                        'hospital' : hospital})
    else:
        return render(request, 'cal/invalid.html')


@login_required()
def editAppointment(request, pk):
    """
    doctors nurses and secretaries can edit appointments
    """
    user = request.user
    appointment = Appointment.objects.filter(id=pk)[0]

    if user.enduser.isDoctor and (appointment.doctorID == user.enduser.id):
        pass
    elif user.enduser.isSecretary:
        pass
    elif user.enduser.isNurse and (appointment.begins - timezone.now() < datetime.timedelta(days = 7)):
        pass
    else:
        return render(request, 'cal/invalid.html')

    form = editAppointmentForm( initial={'length' : appointment.length, 'location' : appointment.location,
                                            'date' : datetime.date(appointment.begins.year, appointment.begins.month, appointment.begins.day),
                                            'begins' : datetime.time(appointment.begins.hour, appointment.begins.minute)})
    if request.method == "POST":
        form = editAppointmentForm(request.POST)
        if form.is_valid():
            begins=form.cleaned_data['begins']
            date=form.cleaned_data['date']
            fullTime = datetime.datetime(date.year, date.month, date.day, begins.hour, begins.minute)
            length=form.cleaned_data['length']
            location=getHospitalID(user.username)

            appointment.begins = fullTime
            appointment.length = length
            appointment.location = location
            appointment.day = fullTime.day
            appointment.month = fullTime.month
            appointment.year = fullTime.year
            appointment.save()
            return redirect('/appointments/' + str(appointment.id))
    return render(request, 'cal/editAppointment.html', {'appointment' : appointment, 'form' : form,
                                                        'doctor' : endUser.objects.filter(id=appointment.doctorID)[0],
                                                        'patient' : endUser.objects.filter(id=appointment.patientID)[0],
                                                        'user' : user})

@login_required()
def deleteAppointment(request, pk):
    """
    Doctors and patients can cancel their own appointments. Secretaries can cancel any appointment
    """
    user = request.user
    ap = Appointment.objects.filter(id=pk)[0]
    if user.enduser.isPatient and (ap.patientID == user.enduser.id):
        pass
    elif user.enduser.isDoctor and (ap.doctorID == user.enduser.id):
        pass
    elif user.enduser.isSecretary:
        pass
    else:
        return render(request, 'cal/invalid.html')
    return render(request, 'cal/cancelAppointment.html', {'appointment' : ap, 'doctor' : endUser.objects.filter(id=ap.doctorID)[0], 'patient' : endUser.objects.filter(id=ap.patientID)[0]})

def delete(request, pk):
    """
    Used as a confirmation page for deleting an appointment
    """
    user = request.user
    ap = Appointment.objects.filter(id=pk)[0]
    if user.enduser.isPatient and (ap.patientID == user.enduser.id):
        pass
    elif user.enduser.isDoctor and (ap.doctorID == user.enduser.id):
        pass
    elif user.enduser.isSecretary:
        pass
    else:
        return render(request, 'cal/invalid.html')
    ap.delete()
    return redirect('/cal')

@login_required()
def makeAppointment(request):
    """
    Doctors Nurses and Secretaries can make appointments
    """
    user = request.user
    if user.enduser.isPatient:
        return render(request, 'cal/invalid.html')
    elif user.enduser.isDoctor:
        pass
    elif user.enduser.isSecretary:
        pass
    elif user.enduser.isNurse:
        pass
    patients = endUser.objects.filter(isPatient=True)
    doctors = endUser.objects.filter(isDoctor=True)

    if request.method == 'POST':
        form = makeAppointmentForm(request.POST)
        if form.is_valid():
            begins=form.cleaned_data['begins']
            date=form.cleaned_data['date']
            fullTime = datetime.datetime(date.year, date.month, date.day, begins.hour, begins.minute)
            length=form.cleaned_data['length']
            location=getHospitalID(user.username)
            patientID=form.cleaned_data['patientID']
            doctorID=form.cleaned_data['doctorID']


            ap = Appointment.objects.create(begins=fullTime, patientID=patientID, doctorID=doctorID, length=length,
                                            location=location, day=fullTime.day, month=fullTime.month, year = fullTime.year)
            ap.save()
            return redirect('/cal')
        else:
            return render(request, 'cal/makeAppointment.html', {'form':form, 'patients':patients, 'doctors':doctors})

    form = makeAppointmentForm()
    context = {
        'form' : form,
        'patients' : patients,
        'doctors' : doctors
    }
    return render(request, 'cal/makeAppointment.html', context)

@login_required()
def CalendarDayView(request, day, month, year):
    """
    Users with appropriate permissions can view their appointments for a specific day
    """
    user = request.user
    object_list = []
    if user.enduser.isPatient:
        object_list = Appointment.objects.filter(month=month, year=year, day=day, patientID=user.enduser.id)
    elif user.enduser.isDoctor:
        object_list = Appointment.objects.filter(month=month, year=year, day=day, doctorID=user.enduser.id)
    elif user.enduser.isSecretary:
        object_list = Appointment.objects.filter(month=month, year=year, day=day)
    elif user.enduser.isNurse:
        if not datetime.datetime(year=int(year), month=int(month), day=int(day)) - datetime.datetime.now() < datetime.timedelta(days = 7):
            return render(request, 'cal/invalid.html')
        else:
            object_list = Appointment.objects.filter(month=month, year=year, day=day)

    date = [month, day, year]
    template = loader.get_template('cal/calendarDay.html')
    context = {
        'user' : user,
        'object_list' : object_list,
        'date' : date
    }
    return HttpResponse(template.render(context, request))

def CalendarWeekView(request, day, month, year):
    user = request.user
    if not user.enduser.isNurse:
        return render(request, 'cal/invalid.html')
    temp_object_list = Appointment.objects.filter(month=month, year=year)
    object_list = []
    for ap in temp_object_list:
        if ap.begins - timezone.now() < datetime.timedelta(days = 7):
            object_list.append(ap)

    name_list = []
    for ap in object_list:
        doctor = endUser.objects.filter(id = ap.doctorID)
        name = 'doctor: ' + doctor[0].user.last_name + '\n'
        name_list.append( (ap, name) )
    template = loader.get_template('cal/calendarWeek.html')

    #gives me the next 7 days
    today = datetime.datetime.today()
    thisWeek = [today, today + datetime.timedelta(days = 1), today + datetime.timedelta(days = 2),
                       today + datetime.timedelta(days = 3), today + datetime.timedelta(days = 4),
                       today + datetime.timedelta(days = 5), today + datetime.timedelta(days = 6)]

    date = [month, day, year]
    context = {
        'name_list' : name_list,
        'date' : date,
        'thisWeek' : thisWeek
    }
    return HttpResponse(template.render(context, request))


@login_required()
def redirectView(request):
    """
    automatically takes user to the current calendar month view if they type in /cal
    """
    thisMonth = datetime.datetime.now().month
    thisYear = datetime.datetime.now().year
    thisDay = datetime.datetime.now().day
    if request.user.enduser.isNurse:
        return redirect('/cal/week/'  + str(thisDay) + '/' + str(thisMonth) + '/' + str(thisYear))
    else:
        return redirect('/cal/' + str(thisMonth) + '/' + str(thisYear))

class dayAppointment():
    """
    helper object for displaying the calendar.
    CalendarMonthView populates each dayAppointment with all the appointments for a given day
    """
    day = 0
    appointments = []

    def __init__(self, day, appointments):
        self.day = day
        self.appointments = appointments

@login_required()
def CalendarMonthView(request, month, year):
    """
    displays all appointments you have permission to view in the given month
    """
    user = request.user
    object_list = []

    if user.enduser.isPatient:
        object_list = Appointment.objects.filter(month=month, year=year, patientID=user.enduser.id)
    elif user.enduser.isDoctor:
        object_list = Appointment.objects.filter(month=month, year=year, doctorID=user.enduser.id)
    elif user.enduser.isSecretary:
        object_list = Appointment.objects.filter(month=month, year=year)
    elif user.enduser.isNurse:
        temp_object_list = Appointment.objects.filter(month=month, year=year)
        object_list = []
        for ap in temp_object_list:
            if ap.begins - timezone.now() < datetime.timedelta(days = 7):
                object_list.append(ap)
    else:
        return render(request, 'cal/invalid.html')

    #makes a list of all the days that appear in a month's calendar page
    cal = calendar.Calendar(6)
    day_list = list(cal.itermonthdates(int(year), int(month)))

    #a day in the middle of the month. Used to store data about that month which is accessed in the html page
    sampleDay = day_list[15]

    #makes a list of all Sundays and Saturdays, which makes it easier to format the html to start new rows on new weeks
    sunday_list = []
    saturday_list = []
    for i in range(0, len(day_list)):
        if i % 7 == 0:
            sunday_list.append(day_list[i])
        elif i % 7 == 6:
            saturday_list.append(day_list[i])

    #makes a list of dayAppointment objects for each day in the month. Each object has the day it represents,
    #and the list of appointments for that day
    day_appointments_list = []
    i=1
    for day in day_list:
        appointments = []
        if i<7 and day.day >20:        # this if statement fix a bug with edge case appointments being displayed twice
            pass
        elif i > 20 and day.day < 7:
            pass
        else:
            for appt in object_list:
                if appt.day == day.day:
                    appointments.append(appt)
        day_appointments_list.append(dayAppointment(day, appointments))
        i += 1

    #sending all the data to the html file for rendering
    template = loader.get_template('cal/calendarMonth.html')
    context = {
        'user' : user,
        'object_list' : object_list,
        'saturday_list' : saturday_list,
        'sunday_list' : sunday_list,
        'day_list' : day_list,
        'day_appointments_list' : day_appointments_list,
        'sampleDay' : sampleDay,
        'lastMonth' : sampleDay - datetime.timedelta(days=30),
        'nextMonth' : sampleDay + datetime.timedelta(days=30)
    }
    return HttpResponse(template.render(context, request))