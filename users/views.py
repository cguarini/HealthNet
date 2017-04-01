from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required, PermissionDenied
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate  # maybe works
import datetime
import HealthNet.settings
from .forms import *
from . import models
import random


def getDate():
    return datetime.datetime.now()


def logEvent(user, event):
    """
    :param user: The enduser object of the user doing the action
    :param event: A string describing the event happening
    :return:
    """
    models.log.objects.create(user=user,
                              event=event,
                              date=str(datetime.datetime.now().date()),
                              time=str(datetime.datetime.now().time()))


def contact(request):
    return render(request, 'users/contact.html')


def reporterror(request):
    return render(request, 'users/reporterror.html')


def feedback(request):
    return render(request, 'users/feedback.html')


def terms(request):
    return render(request, 'users/terms.html')


@login_required(login_url='login')
def showActivityLog(request):
    """
    Shows the event log to administrators, if user is not admin,
    will instead render invalid.
    :param request:
    :return:
    """
    user = request.user
    loop = []
    for obj in models.log.objects.all():
        try:
            loop.append(str(obj))
        except:
            pass
    loop.reverse()

    if user.enduser.isAdministrator:
        return render(request, 'users/activityLog.html', {'loop': loop, 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': getDate()})


def patientView(request):
    """
    Login as the patient John Doe.
    Used to debug, should be removed in final release.
    :param request:
    :return:
    """
    user = User.objects.get(username='JD95')
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user.save()
    login(request, user)
    logEvent(event="Logged In", user=user.enduser)
    return redirect('home')


def DoctorView(request):
    """
    Login as the doctor Richard Johnson
    Used to debug, should be removed in final release.
    :param request:
    :return:
    """
    user = User.objects.get(username='rj75')
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user.save()
    login(request, user)
    logEvent(event="Logged In", user=user.enduser)
    return redirect('home')
    # return render(request,"users/doctorProfile.html",{'user':user})


def NurseView(request):
    """
    Login as the nurse Judith Barnes
    Used to debug, should be removed in final release
    :param request:
    :return:
    """
    user = User.objects.get(username='jb85')
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user.save()
    login(request, user)
    logEvent(event="Logged In", user=user.enduser)
    return redirect('home')


def adminView(request):
    """
    Login as the administrator JT
    Used to debug, should be removed in the final release
    :param request:
    :return:
    """
    user = User.objects.get(username='jt05')
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user.save()
    login(request, user)
    logEvent(event="Logged In", user=user.enduser)
    return redirect('home')


def secretaryView(request):
    user = User.objects.get(username='secretary')
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user.save()
    login(request, user)
    logEvent(event="Logged In", user=user.enduser)
    return redirect('home')


@login_required(login_url='login')
def registerEmployee(request):
    """
    Used by administrators to register employees.
    Administrator must enter all information regarding the employee.
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = make_password(form.cleaned_data['password1'])
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            PhoneNumber = form.cleaned_data['PhoneNumber']
            Address = form.cleaned_data['Address']
            State = form.cleaned_data['State']
            City = form.cleaned_data['City']
            ZipCode = form.cleaned_data['ZipCode']
            ECFirstName = form.cleaned_data['ECFirstName']
            ECLastName = form.cleaned_data['ECLastName']
            ECPhoneNumber = form.cleaned_data['ECPhoneNumber']
            isAdministrator = form.cleaned_data['isAdministrator']
            isNurse = form.cleaned_data['isNurse']
            isDoctor = form.cleaned_data['isDoctor']
            isSecretary = form.cleaned_data['isSecretary']

            hosp = form.cleaned_data['Hospital']

            newEmployee = User.objects.create(username=username,
                                              password=password,
                                              first_name=first_name,
                                              last_name=last_name,
                                              email=email)
            """
            newPatient.username = username
            newPatient.password = password
            newPatient.first_name = first_name
            newPatient.last_name = last_name
            newPatient.email = email
            """
            newEmployee.save()
            prof = newEmployee.enduser
            prof.PhoneNumber = PhoneNumber
            prof.Address = Address
            prof.State = State
            prof.City = City
            prof.ZipCode = ZipCode
            prof.ECFirstName = ECFirstName
            prof.ECLastName = ECLastName
            prof.ECPhoneNumber = ECPhoneNumber
            prof.isAdministrator = isAdministrator
            prof.isDoctor = isDoctor
            prof.isNurse = isNurse
            prof.isSecretary = isSecretary
            prof.isPatient = False

            newEmployee.enduser = prof
            newEmployee.enduser.save()
            newEmployee.save()

            hospi = models.Hospital.objects.get(Name=hosp)
            if isDoctor:
                hospi.doctors += "," + username
            if isNurse:
                hospi.nurses += "," + username
            if isSecretary:
                hospi.secretaries += "," + username
            if isAdministrator:
                hospi.admins += "," + username
            hospi.save()

            logEvent(event="registered as " + newEmployee.username + ".", user=newEmployee.enduser)
            return redirect('home')
    else:
        form = EmployeeRegistrationForm()
    Hospitals = []
    for hosp in models.Hospital.objects.all():
        Hospitals.append(hosp.Name)
    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['Hospitals'] = Hospitals
    token['user'] = user
    token['d'] = getDate()
    return render_to_response('users/employeeRegistration.html', token)


def login_view(request):
    """
    Used to login, uses the LoginForm in users/forms.py
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        if not (username and password):
            return None, "Please enter a username and password"
        user = authenticate(username=username, password=password)
        if user:
            # log action
            try:
                profile = User.objects.get(username=username)
                print('something')
                logEvent(event="Logged In", user=profile.enduser)
            except:
                pass
            login(request, user)

    return render(request, 'users/login.html', {{'d': getDate()}})


@login_required(login_url='login')
def home(request):
    """
    Displays the home screen of the user, changes dynamically
    based on what type of user is viewing.
    :param request:
    :return:
    """
    user = request.user
    return render(request, "users/home.html", {'user': user, 'Hospital': getHospital(user.username), 'd': getDate()})


def index(request):
    """
    The home page of the website, used to access registration and login screens.
    :param request:
    :return:
    """
    if User.objects.all():
        return render(request, 'users/index.html', {'d': getDate()})
    else:
        return redirect('setup')


@login_required(login_url='login')
def profile(request):
    user = request.user
    prof = user.enduser
    if user.is_authenticated():
        profile = user
        if prof.isPatient:
            return render(request, "users/patientProfile.html", {'user': user, 'd': getDate()})
        elif prof.isNurse:
            return render(request, "users/nurseProfile.html", {'user': user, 'd': getDate()})
        elif prof.isAdministrator:
            return render(request, "users/adminProfile.html", {'user': user, 'd': getDate()})
        elif prof.isDoctor:
            return render(request, "users/doctorProfile.html", {'user': user, 'd': getDate()})
        else:
            return render(request, "users/baseProfile.html", {'user': user, 'd': getDate()})

    else:
        raise PermissionDenied


@login_required(login_url='login')
def editProfile(request):
    user = request.user
    if request.method == 'POST':
        form = editUserProfile(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data.get('email')
            user.enduser.PhoneNumber = form.cleaned_data.get('PhoneNumber')
            user.enduser.State = form.cleaned_data.get('State')
            user.enduser.City = form.cleaned_data['City']
            user.enduser.Address = form.cleaned_data['Address']
            user.enduser.ZipCode = form.cleaned_data['ZipCode']
            user.enduser.ECPhoneNumber = form.cleaned_data['ECPhoneNumber']
            user.enduser.ECLastName = form.cleaned_data['ECLastName']
            user.enduser.ECFirstName = form.cleaned_data['ECFirstName']
            user.save()
            user.enduser.save()
            logEvent(event="edited their profile", user=user.enduser)
            return redirect('/home')
    else:
        form = editUserProfile(
            initial={'username': user.username,
                     'password': user.password,
                     'first_name': user.first_name,
                     'last_name': user.last_name,
                     'email': user.email,
                     'PhoneNumber': user.enduser.PhoneNumber,
                     'Address': user.enduser.Address,
                     'State': user.enduser.State,
                     'City': user.enduser.City,
                     'ZipCode': user.enduser.ZipCode,
                     'ECFirstName': user.enduser.ECFirstName,
                     'ECLastName': user.enduser.ECLastName,
                     'ECPhoneNumber': user.enduser.ECPhoneNumber,
                     'dateOfBirth': user.enduser.dateOfBirth,
                     'ProviderID': user.enduser.ProviderID,
                     'PolicyType': user.enduser.PolicyType,
                     'PolicyNumber': user.enduser.PolicyNumber,
                     'records': user.enduser.records
                     })
    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['d'] = getDate()
    token['user'] = user
    return render(request, "users/editBaseProfile.html", token)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = make_password(form.cleaned_data['password1'])
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            PhoneNumber = form.cleaned_data['PhoneNumber']
            Address = form.cleaned_data['Address']
            State = form.cleaned_data['State']
            City = form.cleaned_data['City']
            ZipCode = form.cleaned_data['ZipCode']
            ECFirstName = form.cleaned_data['ECFirstName']
            ECLastName = form.cleaned_data['ECLastName']
            ECPhoneNumber = form.cleaned_data['ECPhoneNumber']
            dateOfBirth = form.cleaned_data['dateOfBirth']

            ProviderID = form.cleaned_data['ProviderID']
            PolicyType = form.cleaned_data['PolicyType']
            PolicyNumber = form.cleaned_data['PolicyNumber']
            records = form.cleaned_data['records']

            hosp = form.cleaned_data['Hospital']

            newPatient = User.objects.create(username=username,
                                             password=password,
                                             first_name=first_name,
                                             last_name=last_name,
                                             email=email)
            """
            newPatient.username = username
            newPatient.password = password
            newPatient.first_name = first_name
            newPatient.last_name = last_name
            newPatient.email = email
            """
            newPatient.save()
            prof = newPatient.enduser
            prof.PhoneNumber = PhoneNumber
            prof.Address = Address
            prof.State = State
            prof.City = City
            prof.ZipCode = ZipCode
            prof.ECFirstName = ECFirstName
            prof.ECLastName = ECLastName
            prof.ECPhoneNumber = ECPhoneNumber
            prof.dateOfBirth = dateOfBirth

            prof.ProviderID = ProviderID
            prof.PolicyType = PolicyType
            prof.PolicyNumber = PolicyNumber
            prof.records = records
            prof.isPatient = True
            newPatient.enduser = prof
            newPatient.enduser.save()
            newPatient.save()

            hospi = models.Hospital.objects.get(Name=hosp)
            hospi.patients += "," + username
            hospi.save()

            logEvent(event="registered as " + newPatient.username + ".", user=newPatient.enduser)
            request.user = newPatient
            return redirect('home')
    else:
        form = RegisterForm()
        Hospitals = []
        for hosp in models.Hospital.objects.all():
            Hospitals.append(hosp.Name)
        token = {}
        token.update(csrf(request))
        token['form'] = form
        token['Hospitals'] = Hospitals
        token['d'] = getDate()
        return render_to_response('users/registration/register_revamp.html', token)


@login_required(login_url='login')
def specialtyScreen(request):
    user = request.user
    patients = []
    doctors = []
    for obj in User.objects.all():
        try:
            if obj.enduser.isPatient:
                patients.append(obj)
            elif obj.enduser.isDoctor:
                doctors.append(obj)
        except:
            pass
    context = {'user': user, 'patients': patients, 'doctors': doctors, 'd': getDate()}

    if user.enduser.isPatient:
        return render(request, 'users/patientScreen.html', context)
    elif user.enduser.isNurse:
        return render(request, 'users/nurseScreen.html', context)
    elif user.enduser.isDoctor:
        """context['yourPatients']=user.enduser.Patients"""
        return render(request, 'users/doctorScreen.html', context)
    elif user.enduser.isAdministrator:
        return render(request, 'users/adminScreen.html', context)
    elif user.enduser.isSecretary:
        return render(request, 'users/secretaryScreen.html', context)
    else:
        return redirect('login')


@login_required(login_url='login')
def admitPatient(request):
    user = request.user
    profile = user.enduser
    if profile.isNurse or profile.isDoctor:
        patients = []
        for obj in User.objects.all():
            try:
                if obj.enduser.isPatient:
                    patients.append(obj)
            except:
                pass
        if request.method == 'POST':
            form = admitPatientForm(request.POST)
            if form.is_valid():
                patient = form.cleaned_data['patient']
                reason = form.cleaned_data['reason']
                try:
                    pat = User.objects.get(username=patient)
                    pat.enduser.isAdmitted = True
                    pat.enduser.aReason = reason
                    count = pat.enduser.aCount + 1
                    pat.enduser.aCount = count
                    pat.enduser.aTime = datetime.datetime.now()
                    pat.save()
                    pat.enduser.save()
                    logEvent(event="was admitted by " + user.first_name + " " + user.last_name, user=pat.enduser)
                except:
                    pass  # show an error?
                return redirect('admit')
        else:
            form = admitPatientForm()
        return render(request, 'users/admit.html', {'form': form, 'patients': patients, 'd': getDate(), 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def requestDoctor(request):
    user = request.user
    doctors = []
    for obj in User.objects.all():
        try:
            if obj.enduser.isDoctor:
                if getHospital(obj.username) == getHospital(user.username):
                    doctors.append(obj)
        except:
            pass
    form = doctorRequestForm(request.POST)
    patients = []
    doctors = []
    patUsers = user.enduser.Patients.split(",")
    docUsers = user.enduser.Doc.split(",")
    patstoret = []
    doctoret = []
    for obj in User.objects.all():
        try:
            if obj.enduser.isPatient:
                patients.append(obj)
            elif obj.enduser.isDoctor:
                doctors.append(obj)
        except:
            pass
    requests = []
    if user.enduser.isDoctor:
        for obj in models.doctorRequest.objects.all():
            if obj.doctor == user.username:
                requests.append(obj)
    user = request.user
    r_size = len(requests)
    if user.enduser.isDoctor:
        if len(patUsers) > 0:
            for pat in patUsers:
                try:
                    p = User.objects.get(username=pat)
                    patstoret.append(p)
                except:
                    pass
    if user.enduser.isPatient:
        if len(docUsers) > 0:
            for doc in docUsers:
                try:
                    d = User.objects.get(username=doc)
                    doctoret.append(d)
                except:
                    pass
    if request.method == 'POST':
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            patient = user.username
            reason = form.cleaned_data['reason']
            if getHospital(doctor) == getHospital(patient):
                try:
                    doctorRequest.objects.create(doctor=doctor, patient=patient, reason=reason)
                    logEvent(event='requested doctor ' + doctor, user=user.enduser)
                    return redirect('home')
                except:
                    errors = []
                    errors.append("You messed up")
                    return render(request, 'users/requestDoc.html',
                                  {'form': form, 'd': getDate(), 'doctors': doctors, 'errors': errors, 'user': user})
            else:
                errors = []
                errors.append("You messed up")
                return render(request, 'users/requestDoc.html', {'form': form, 'd': getDate(), 'doctors': doctors, 'errors': errors, 'user': user})

    form = doctorRequestForm()
    return render(request, 'users/requestDoc.html', {'form': form, 'd': getDate(),'patients': patients, 'user': user, 'doctors': doctors,
                                                               'requests': requests, 'r_size': r_size,
                                                               'patUsers': patUsers,
                                                               'patstoret': patstoret, 'docUsers': docUsers,
                                                               'doctoret': doctoret})


@login_required(login_url='login')
def requests(request):
    user = request.user
    requests = []
    for obj in models.doctorRequest.objects.all():
        try:
            if obj.doctor == user.username:
                requests.append(obj)
        except:
            pass
    return render(request, 'users/requests.html', {'requests': requests, 'd': getDate(), 'user': user})


@login_required(login_url='login')
def patientDirectory(request):
    user = request.user
    profile = user.enduser
    patients = []
    doctors = []
    patUsers = user.enduser.Patients.split(",")
    docUsers = user.enduser.Doc.split(",")
    patstoret = []
    doctoret = []
    for obj in User.objects.all():
        try:
            if obj.enduser.isPatient:
                if getHospital(obj.username) == getHospital(user.username):
                    patients.append(obj)
            elif obj.enduser.isDoctor:
                if getHospital(obj.username) == getHospital(user.username):
                    doctors.append(obj)
        except:
            pass
    requests = []
    if user.enduser.isDoctor:
        for obj in models.doctorRequest.objects.all():
            if obj.doctor == user.username:
                requests.append(obj)
    user = request.user
    r_size = len(requests)
    if user.enduser.isDoctor:
        if len(patUsers) > 0:
            for pat in patUsers:
                try:
                    p = User.objects.get(username=pat)
                    patstoret.append(p)
                except:
                    pass
    if user.enduser.isPatient:
        if len(docUsers) > 0:
            for doc in docUsers:
                try:
                    d = User.objects.get(username=doc)
                    doctoret.append(d)
                except:
                    pass
    if user.enduser.isDoctor or user.enduser.isNurse or user.enduser.isSecretary or user.enduser.isPatient:
        return render(request, "users/patientDirectory.html", {'patients': patients, 'user': user, 'doctors': doctors,
                                                               'requests': requests, 'r_size': r_size,
                                                               'patUsers': patUsers,
                                                               'patstoret': patstoret, 'docUsers': docUsers,
                                                               'doctoret': doctoret,
                                                               'd': getDate()})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewPatientProfile(request, patientPK):
    user = request.user
    account = User.objects.get(pk=patientPK)
    profile = account.enduser
    if user.enduser.isDoctor or user.enduser.isNurse:
        if profile.isPatient:
            return render(request, "users/viewMedicalInfo.html", {'user': user, 'account': account, 'd': getDate()})
        else:
            return render(request, "users/invalid.html", {'d': getDate(), 'user': user})
    else:
        return render(request, "users/invalid.html", {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewTest(request, testPK):
    user = request.user
    test = models.TestResults.objects.get(pk=testPK)
    form = testForm(initial={'doctor': test.doctor_fn,
                             'patient': test.patient_fn,
                             'pending': test.pending,
                             'information': test.information,
                             'results': test.results,
                             'file': test.file, })
    return render(request, "users/Tests/viewTest.html", {'user': user, 'test': test, 'd': getDate(), 'form': form})


@login_required(login_url='login')
def addToPatients(request):
    user = request.user
    profile = user.enduser
    patients = []
    userPats = user.enduser.Patients.split(',')
    for obj in User.objects.all():
        try:
            if obj.enduser.isPatient:
                patients.append(obj)
        except:
            pass
    if user.enduser.isDoctor:
        if request.method == 'POST':
            form = addToPatientsForm(request.POST)
            if form.is_valid():
                patient = form.cleaned_data['patient']
                try:
                    pat = User.objects.get(username=patient)
                    if not patient in userPats:
                        user.enduser.Patients += "," + patient
                        pat.enduser.Doc += "," + user.username

                        user.enduser.save()
                        user.save()
                        pat.enduser.save()
                        pat.save()

                        logEvent(profile,
                                 'Added ' + pat.first_name + " " + pat.last_name + " as " + user.first_name + " " + user.last_name + "'s patient")
                    return redirect('directory')
                except:
                    return redirect('addToPatients')
        else:
            form = addToPatientsForm()
            return render(request, "users/addToPatients.html", {'form': form, 'patients': patients, 'd': getDate(), 'user': user})
    else:
        render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


def getHospital(username):
    for obj in models.Hospital.objects.all():

        if username in obj.patients.split(","):
            return obj.Name
        if username in obj.doctors.split(","):
            return obj.Name
        if username in obj.nurses.split(","):
            return obj.Name
        if username in obj.secretaries.split(","):
            return obj.Name
        if username in obj.admins.split(","):
            return obj.Name


@login_required(login_url='login')
def sendMessage(request):
    user = request.user
    errors = []
    if request.method == 'POST':
        form = sendMessageForm(request.POST)
        if form.is_valid():
            try:
                recip = User.objects.get(username=form.cleaned_data['reciever'])
                """
                Permissions
                """
                if user.enduser.isDoctor:
                    if recip.username in user.enduser.Patients.split(","):
                        models.Message.objects.create(sender=user.username, reciever=form.cleaned_data['reciever'],
                                                      message=form.cleaned_data['message'],
                                                      subject=form.cleaned_data['subject'],
                                                      timeSent=datetime.date.today())
                        return redirect('Inbox')  # should redirect to messaging system
                    if recip.enduser.isNurse or recip.enduser.isSecretary:
                        if getHospital(recip.username) == getHospital(user.username):
                            models.Message.objects.create(sender=user.username, reciever=form.cleaned_data['reciever'],
                                                          message=form.cleaned_data['message'],
                                                          subject=form.cleaned_data['subject'],
                                                          timeSent=datetime.date.today())
                            return redirect('Inbox')  # should redirect to messaging system
                elif user.enduser.isNurse:
                    if getHospital(recip.username) == getHospital(user.username):
                        models.Message.objects.create(sender=user.username, reciever=form.cleaned_data['reciever'],
                                                      message=form.cleaned_data['message'],
                                                      subject=form.cleaned_data['subject'],
                                                      timeSent=datetime.date.today())
                        return redirect('Inbox')  # should redirect to messaging system
                elif user.enduser.isPatient:
                    if recip.username in user.enduser.Doc.split(","):
                        models.Message.objects.create(sender=user.username, reciever=form.cleaned_data['reciever'],
                                                      message=form.cleaned_data['message'],
                                                      subject=form.cleaned_data['subject'],
                                                      timeSent=datetime.date.today())
                        return redirect('Inbox')  # should redirect to messaging system
                elif user.enduser.isSecretary:
                    if getHospital(recip.username) == getHospital(user.username):
                        models.Message.objects.create(sender=user.username, reciever=form.cleaned_data['reciever'],
                                                      message=form.cleaned_data['message'],
                                                      subject=form.cleaned_data['subject'],
                                                      timeSent=datetime.date.today())
                        return redirect('Inbox')  # should redirect to messaging system
                elif user.enduser.isAdministrator:
                    models.Message.objects.create(sender=user.username, reciever=form.cleaned_data['reciever'],
                                                  message=form.cleaned_data['message'],
                                                  subject=form.cleaned_data['subject'],
                                                  timeSent=datetime.date.today())
                    return redirect('Inbox')  # should redirect to messaging system
                else:
                    render(request, 'users/invalid.html', {'d': getDate()})
                errors.append("You do not have permission to send a message to that user.")
                return render(request, 'users/sendMessage.html', {'form': form, 'errors': errors, 'd': getDate(), 'user': user})
            except:
                errors.append("Username does not exist")
                return render(request, 'users/sendMessage.html', {'form': form, 'errors': errors, 'd': getDate(), 'user': user})
        else:
            form = sendMessageForm()
            return render(request, 'users/sendMessage.html',
                          {'form': form, 'errors': errors, 'd': getDate(), 'user': user})  # need to add html
    else:
        form = sendMessageForm()
        return render(request, 'users/sendMessage.html', {'form': form, 'errors': errors, 'd': getDate(), 'user': user})


@login_required(login_url='login')
def Inbox(request):
    user = request.user
    profile = user.enduser
    if request.method == 'POST':
        form = sendMessageForm(request.POST)
        if form.is_valid():
            models.Message.objects.create(sender=user.username, reciever=form.cleaned_data['reciever'],
                                          message=form.cleaned_data['message'], subject=form.cleaned_data['subject'],
                                          timeSent=datetime.date.today())
            form = sendMessageForm()
    else:
        form = sendMessageForm()
    messages = []
    for letter in Message.objects.all():
        if letter.reciever == user.username:
            messages.append(letter)
    messages.reverse()
    return render(request, 'users/Inbox.html', {'user': user, 'messages': messages, 'form': form, 'd': getDate()})


@login_required(login_url='login')
def messagingCenter(request):
    user = request.user
    return render(request, 'Messaging.html', {'user': user, 'd': getDate()})


@login_required(login_url='login')
def Outbox(request):
    user = request.user
    profile = user.enduser
    if request.method == 'POST':
        form = sendMessageForm(request.POST)
        if form.is_valid():
            models.Message.objects.create(sender=user.username, reciever=form.cleaned_data['reciever'],
                                          message=form.cleaned_data['message'], subject=form.cleaned_data['subject'],
                                          timeSent=datetime.date.today())
            form = sendMessageForm()
    else:
        form = sendMessageForm()
    messages = []
    for letter in Message.objects.all():
        if letter.sender == user.username:
            messages.append(letter)
    messages.reverse()
    return render(request, 'users/Outbox.html', {'user': user, 'messages': messages, 'form': form, 'd': getDate()})


@login_required(login_url='login')
def viewMessage(request, messagePK):
    messages = []
    user = request.user

    letter = Message.objects.get(pk=messagePK)
    messages.append(letter)

    return render(request, 'users/viewMessage.html', {'user': user, 'messages': messages, 'd': getDate()})


@login_required(login_url='login')
def viewRequest(request, requestPK):
    user = request.user
    r = models.doctorRequest.objects.get(pk=requestPK)
    return render(request, 'users/viewRequest.html', {'user': user, 'r': r, 'd': getDate()})


@login_required(login_url='login')
def deleteRequest(request, requestPK):
    user = request.user
    r = get_object_or_404(models.doctorRequest, pk=requestPK).delete()
    return HttpResponseRedirect('/myRequests')


@login_required(login_url='login')
def acceptRequest(request, requestPK):
    user = request.user
    r = models.doctorRequest.objects.get(pk=requestPK)
    try:
        pat = User.objects.get(username=r.patient)
        user.enduser.Patients += "," + r.patient.username
        pat.enduser.Doc += "," + user.username
        logEvent(event="accepted a patient request", user=user.enduser)
        logEvent(event="was accepted by a doctor", user=pat.enduser)
    except:
        pass
    return deleteRequest(request, requestPK)


@login_required(login_url='login')
def editTest(request, testPK):
    user = request.user
    test = models.TestResults.objects.get(pk=testPK)
    if request.method == 'POST':
        form = testForm(request.POST, request.FILES)
        if form.is_valid():
            test.doctor_fn = form.cleaned_data['doctor']
            test.patient_fn = form.cleaned_data['patient']
            test.pending = form.cleaned_data['pending']
            test.information = form.cleaned_data['information']
            test.results = form.cleaned_data['results']
            try:
                test.file = request.FILES['file']
            except:
                pass
            test.save()
            logEvent(user=user.enduser, event="updated a test")
            return render(request, 'users/Tests/viewTest.html', {'user': user, 'test': test, 'd': getDate()})
        else:
            return redirect('home')
    else:
        form = testForm(initial={'doctor': test.doctor_fn,
                                 'patient': test.patient_fn,
                                 'pending': test.pending,
                                 'information': test.information,
                                 'results': test.results,
                                 'file': test.file, })
    return render(request, 'users/Tests/editTest.html', {'user': user, 'form': form, 'test': test, 'd': getDate()})


@login_required(login_url='login')
def updateMedicalInfo(request, patientPK):
    user = request.user
    profile = user.enduser
    try:
        patient = User.objects.get(pk=patientPK)
    except:
        return render(request, "users/invalid.html", {'d': getDate(), 'user': user})  # should add a message to this url....
    if profile.isDoctor or profile.isNurse:
        if request.method == 'POST':
            form = updateMedicalForm(request.POST)
            if form.is_valid():
                prof = patient.enduser
                prof.records = form.cleaned_data['records']
                prof.ProviderID = form.cleaned_data['ProviderID']
                prof.PolicyType = form.cleaned_data['PolicyType']
                prof.PolicyNumber = form.cleaned_data['PolicyNumber']
                logEvent(event="updated medical information", user=user.enduser)
                patient.enduser = prof
                patient.enduser.save()
                patient.save()
                return render(request, 'users/viewMedicalInfo.html', {'user': user, 'account': patient, 'd': getDate()})
            else:
                return redirect('home')
        else:
            form = updateMedicalForm(initial={
                'records': patient.enduser.records,
                'ProviderID': patient.enduser.ProviderID,
                'PolicyType': patient.enduser.PolicyType,
                'PolicyNumber': patient.enduser.PolicyNumber
            })
            return render(request, "users/updateMedicalInfo.html", {'form': form, 'patient': patient, 'd': getDate(), 'user': user})


@login_required(login_url='login')
def createTest(request):
    user = request.user
    if request.method == 'POST':
        form = testForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                models.TestResults.objects.create(doctor_fn=form.cleaned_data['doctor'],
                                              patient_fn=form.cleaned_data['patient'],
                                              pending=form.cleaned_data['pending'],
                                              information=form.cleaned_data['information'],
                                              results=form.cleaned_data['results'],
                                              file=request.FILES['file'])
            else:
                models.TestResults.objects.create(doctor_fn=form.cleaned_data['doctor'],
                                              patient_fn=form.cleaned_data['patient'],
                                              pending=form.cleaned_data['pending'],
                                              information=form.cleaned_data['information'],
                                              results=form.cleaned_data['results'])
            logEvent(event="created a test.", user=request.user.enduser)
            return redirect('myTests')
        else:
            return render(request, 'users/Tests/submitTest.html', {'form': form, 'user': user})
    else:
        form = testForm()
        return render(request, 'users/Tests/submitTest.html', {'form': form, 'd': getDate(), 'user': user})


@login_required(login_url='login')
def testCenter(request):
    user = request.user
    profile = user.enduser
    tests = []
    if profile.isPatient:
        for item in models.TestResults.objects.all():
            try:
                if item.patient_fn == user.username:
                    tests.append(item)
            except:
                pass
        return render(request, 'users/Tests/myTests.html', {'tests': tests, 'patient': True, 'd': getDate(), 'user': user})
    elif profile.isDoctor:
        for item in models.TestResults.objects.all():
            try:
                if item.doctor_fn == user.username:
                    tests.append(item)
            except:
                pass
        return render(request, 'users/Tests/myTests.html', {'tests': tests, 'patient': False, 'd': getDate(), 'user': user})


@login_required(login_url='login')
def discharge(request):
    user = request.user
    profile = user.enduser
    if profile.isDoctor:
        patients = []
        for obj in User.objects.all():
            try:
                if obj.enduser.isPatient and obj.enduser.isAdmitted:
                    patients.append(obj)
            except:
                pass
        if request.method == 'POST':
            form = dischargePatientForm(request.POST)
            if form.is_valid():
                patient = form.cleaned_data['patient']

                try:
                    pat = User.objects.get(username=patient)
                    pat.enduser.isAdmitted = False
                    pat.save()
                    pat.enduser.save()
                    logEvent(event="was discharged by " + user.first_name + " " + user.last_name, user=pat.enduser)
                except:
                    pass

                return redirect('discharge')
        else:
            form = dischargePatientForm()
        return render(request, 'users/discharge.html', {'form': form, 'patients': patients, 'd': getDate(), 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def admissions(request):
    user = request.user
    profile = user.enduser
    if profile.isNurse or profile.isDoctor:
        patients = []
        for obj in User.objects.all():
            try:
                if obj.enduser.isPatient and obj.enduser.isAdmitted:
                    patients.append(obj)
            except:
                pass
        user = request.user
        if user.enduser.isDoctor or user.enduser.isNurse:
            return render(request, "users/admissions.html", {'patients': patients, 'd': getDate(), 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(),'user':user})


@login_required(login_url='login')
def viewAdmitted(request):
    user = request.user
    profile = user.enduser
    if profile.isNurse or profile.isDoctor:
        patients = []
        for obj in User.objects.all():
            try:
                if obj.enduser.isPatient and obj.enduser.isAdmitted:
                    patients.append(obj)
            except:
                pass
        user = request.user
        if user.enduser.isDoctor or user.enduser.isNurse:
            return render(request, "users/admitted.html", {'patients': patients, 'd': getDate(), 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def persriptionScreen(request):
    user = request.user
    profile = user.enduser
    perscriptions = []
    if profile.isDoctor:
        for script in models.perscription.objects.all():
            if script.doctor == user.username:
                perscriptions.append(script)
            perscriptions.reverse()
    elif profile.isPatient:
        for script in models.perscription.objects.all():
            if script.patient == user.username:
                perscriptions.append(script)
        perscriptions.reverse()
    if profile.isDoctor:
        patients = []
        for obj in User.objects.all():
            try:
                if obj.enduser.isPatient and obj.enduser.isAdmitted:
                    patients.append(obj)
            except:
                pass
        user = request.user
        return render(request, "users/perscriptions.html",
                      {'patients': patients, 'user': user, 'perscriptions': perscriptions, 'd': getDate(), 'user': user})
    elif profile.isPatient:
        return render(request, 'users/perscriptions.html',
                      {'user': user, 'perscriptions': perscriptions, 'd': getDate(), 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def perscribe(request):
    user = request.user
    profile = user.enduser

    if profile.isDoctor:
        if request.method == 'POST':
            form = perscribeForm(request.POST)
            if form.is_valid():
                doctor = user.username
                patient = form.cleaned_data['patient']
                perscription = form.cleaned_data['perscription']
                dose = form.cleaned_data['dose']
                reason = form.cleaned_data['reason']
                logEvent(event="prescribed " + patient + " " + perscription + " " + dose + "because " + reason,
                         user=profile)
                models.perscription.objects.create(doctor=doctor, patient=patient, perscription=perscription
                                                   , dose=dose, reason=reason)
                return redirect('perscriptions')
            return render(request, 'users/perscribe.html', {'d': getDate(), 'user': user})
        else:
            form = perscribeForm()
            return render(request, 'users/perscribe.html', {'form': form, 'd': getDate(), 'user': user})
    return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewPerscriptions(request):
    user = request.user
    profile = user.enduser
    perscriptions = []
    if profile.isDoctor:
        for script in models.perscription.objects.all():
            if script.doctor == user.username:
                perscriptions.append(script)
        return render(request, 'users/perscriptionList.html',
                      {'perscriptions': perscriptions, 'user': user, 'd': getDate(), 'user': user})
    elif profile.isPatient:
        for script in models.perscription.objects.all():
            if script.patient == user.username:
                perscriptions.append(script)
        return render(request, 'users/perscriptionList.html',
                      {'perscriptions': perscriptions, 'user': user, 'd': getDate(), 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewPerscription(request, perscriptionPK):
    perscriptions = []
    user = request.user
    script = perscription.objects.get(pk=perscriptionPK)
    perscriptions.append(script)
    if script.doctor == user.username or script.patient == user.username:

        return render(request, 'users/viewPerscription.html',
                      {'user': user, 'perscriptions': perscriptions, 'd': getDate()})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def deletePerscription(request, perscriptionPK):
    user = request.user
    profile = user.enduser
    if profile.isDoctor:
        try:
            script = models.perscription.objects.get(pk=perscriptionPK)
            script.delete()
            logEvent(user=profile, event='deleted ' + script.perscription + ' perscription for ' + script.patient)
        except:
            pass
        return redirect('perscriptions')
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewRequests(request):
    user = request.user
    profile = user.enduser
    if profile.isDoctor:
        requests = doctorRequest.objects.filter(doctor=user.username)
        return render(request, 'users/requests.html', {'user': user, 'requests': requests, 'd': getDate})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def createHospital(request):
    """
    Allows administrators to add new hospitals to the network
    :param request:
    :return:
    """
    user = request.user
    profile = user.enduser
    if profile.isAdministrator:
        if request.method == 'POST':
            form = createHospitalForm(request.POST)
            if form.is_valid():
                Name = form.cleaned_data['Name']
                Address = form.cleaned_data['Address']
                logEvent(user=profile, event='Added ' + Name + " to the HealthNet network.")
                models.Hospital.objects.create(Name=Name, Address=Address)
                return redirect('hospitalCenter')
            return render(request, 'users/Hospital/addHospital.html', {'d': getDate(), 'user': user, 'form': form})
        else:
            form = createHospitalForm()
            return render(request, 'users/Hospital/addHospital.html', {'form': form, 'd': getDate(), 'user': user})
    return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def hospitalCenter(request):
    """
    Much like messaging center, is the center for all tools dealing with hospitals
    @author: Chris Guarini
    :param request:
    :return:
    """
    user = request.user
    profile = user.enduser
    if profile.isAdministrator:
        return render(request, 'users/Hospital/hospitalCenter.html', {'d': getDate(), 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewHospitals(request):
    """
    Only viewable by administrators
    Shows all current hospitals in the network, allows for editing and moving of staff/patients
    :@author: Chris Guarini
    :param request:
    :return:
    """
    user = request.user
    profile = user.enduser
    if profile.isAdministrator:
        hospitals = []
        try:
            for hospital in Hospital.objects.all():
                hospitals.append(hospital)
        except:
            pass
        context = {'hospitals': hospitals, 'd': getDate(), 'user': user}
        return render(request, 'users/Hospital/viewHospitals.html', context)


@login_required(login_url='login')
def viewHospital(request, HospitalPK):
    """
    Shows information of a given hospital with the PK HospitalPK
    :param request:
    :param HospitalPK: the PK of the hospital
    :return:
    """
    user = request.user
    profile = user.enduser
    hospital = Hospital.objects.get(pk=HospitalPK)
    if profile.isAdministrator:
        return render(request, "users/Hospital/viewHospital.html", {'hospital': hospital, 'd': getDate(), 'user': user})


@login_required(login_url='login')
def viewHospital(request, HospitalPK):
    """
    Shows information of a given hospital with the PK HospitalPK
    :param request:
    :param HospitalPK: the PK of the hospital
    :return:
    """
    user = request.user
    profile = user.enduser
    hospital = Hospital.objects.get(pk=HospitalPK)
    if profile.isAdministrator:
        return render(request, "users/Hospital/viewHospital.html", {'hospital': hospital, 'd': getDate(), 'user': user})
    return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewPatients(request, HospitalPK):
    user = request.user
    profile = user.enduser
    if profile.isAdministrator:
        hospital = Hospital.objects.get(pk=HospitalPK)
        usernames = hospital.patients.split(',')
        users = []
        number = 0
        name = 'Patients'
        for username in usernames:
            try:
                account = User.objects.get(username=username)
                users.append(account)
            except:
                pass
        context = {'users': users, 'name': name, 'hospital': hospital, 'number': number, 'd': getDate(), 'user': user}
        return render(request, 'users/Hospital/viewUsers.html', context)
    return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewDoctors(request, HospitalPK):
    user = request.user
    profile = user.enduser
    if profile.isAdministrator:
        hospital = Hospital.objects.get(pk=HospitalPK)
        usernames = hospital.doctors.split(',')
        users = []
        number = 1
        name = 'Doctors'
        for username in usernames:
            try:
                account = User.objects.get(username=username)
                users.append(account)
            except:
                pass
        context = {'users': users, 'name': name, 'hospital': hospital, 'number': number, 'd': getDate()}
        return render(request, 'users/Hospital/viewUsers.html', context)
    return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewNurses(request, HospitalPK):
    user = request.user
    profile = user.enduser
    if profile.isAdministrator:
        hospital = Hospital.objects.get(pk=HospitalPK)
        usernames = hospital.nurses.split(',')
        users = []
        number = 10
        name = 'Nurses'
        for username in usernames:
            try:
                account = User.objects.get(username=username)
                users.append(account)
            except:
                pass
        context = {'users': users, 'name': name, 'hospital': hospital, 'number': number, 'd': getDate()}
        return render(request, 'users/Hospital/viewUsers.html', context)
    return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def viewSecretaries(request, HospitalPK):
    user = request.user
    profile = user.enduser
    if profile.isAdministrator:
        hospital = Hospital.objects.get(pk=HospitalPK)
        usernames = hospital.secretaries.split(',')
        users = []
        number = 11
        name = 'Secretaries'
        for username in usernames:
            try:
                account = User.objects.get(username=username)
                users.append(account)
            except:
                pass
        context = {'users': users, 'name': name, 'hospital': hospital, 'number': number, 'd': getDate()}
        return render(request, 'users/Hospital/viewUsers.html', context)
    return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


@login_required(login_url='login')
def transfer(request, HospitalPK, number):
    user = request.user
    profile = user.enduser
    hospital = Hospital.objects.get(pk=HospitalPK)
    accounts = ''
    if number == '0':
        accounts = hospital.patients
    elif number == '1':
        accounts = hospital.doctors
    elif number == '10':
        accounts = hospital.nurses
    elif number == '11':
        accounts = hospital.secretaries
    if profile.isAdministrator:
        if request.method == 'POST':
            form = transferForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']

                try:
                    user = User.objects.get(username=username)
                    accountArray = accounts.split(',')

                    if username in accountArray:
                        print('username in accounts')
                    else:
                        print('username not in accounts')
                        removeUser(username)
                        accounts += "," + username
                        if number == '0':
                            print('hit this')
                            hospital.patients = accounts
                        elif number == '1':
                            hospital.doctors = accounts
                        elif number == '10':
                            hospital.nurses = accounts
                        elif number == '11':
                            hospital.secretaries = accounts
                        hospital.save()
                        logEvent(profile,
                                 'transfered ' + user.first_name + " " + user.last_name + " : " + user.username + " to " + hospital.Name)
                    return redirect('viewHospital')
                except:
                    return redirect('transfer')
            else:
                print(form.cleaned_data['username'])
                return render(request, 'users/Hospital/transfer.html',
                              {'form': form, 'hospital': hospital, 'd': getDate(), 'user': user})
        else:

            form = transferForm()
            return render(request, "users/Hospital/transfer.html", {'form': form, 'hospital': hospital, 'd': getDate(), 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': getDate(), 'user': user})


def removeUser(user):
    hospitals = Hospital.objects.all()
    account = User.objects.get(username=user)
    profile = account.enduser
    for hospital in hospitals:
        patients = hospital.patients
        patientList = patients.split(',')
        doctors = hospital.doctors
        doctorList = doctors.split(',')
        nurses = hospital.nurses
        nurseList = nurses.split(',')
        secretaries = hospital.secretaries
        secretaryList = secretaries.split(',')
        if user in patientList:
            patientList.remove(user)
            text = ''
            for obj in patientList:
                text += obj + ','
            hospital.patients = text
            logEvent(profile, "Was transfered from " + hospital.Name)
        if user in doctorList:
            doctorList.remove(user)
            text = ''
            for obj in patientList:
                text += obj + ','
            hospital.doctors = text
            logEvent(profile, "Was transfered from " + hospital.Name)
        if user in nurseList:
            nurseList.remove(user)
            text = ''
            for obj in nurseList:
                text += obj + ','
            hospital.nurses = text
            logEvent(profile, "Was transfered from " + hospital.Name)
        if user in secretaryList:
            secretaryList.remove(user)
            text = ''
            for obj in secretaryList:
                text += obj + ','
            hospital.secretaries = text
            logEvent(profile, "Was transfered from " + hospital.Name)
        hospital.save()


def setup(request):
    if User.objects.all():
        return redirect('index')
    else:
        return render(request, 'users/setup/setup.html', {'d': getDate()})


def setup_registerAdmin(request):
    if User.objects.all():
        return redirect('index')
    if request.method == 'POST':
        form = setup_AdminRegistrationForm(request.POST)
        if form.is_valid():
            print('hit valid')
            username = form.cleaned_data['username']
            password = make_password(form.cleaned_data['password1'])
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            PhoneNumber = form.cleaned_data['PhoneNumber']
            Address = form.cleaned_data['Address']
            State = form.cleaned_data['State']
            City = form.cleaned_data['City']
            ZipCode = form.cleaned_data['ZipCode']
            ECFirstName = form.cleaned_data['ECFirstName']
            ECLastName = form.cleaned_data['ECLastName']
            ECPhoneNumber = form.cleaned_data['ECPhoneNumber']

            newEmployee = User.objects.create(username=username,
                                              password=password,
                                              first_name=first_name,
                                              last_name=last_name,
                                              email=email)
            """
            newPatient.username = username
            newPatient.password = password
            newPatient.first_name = first_name
            newPatient.last_name = last_name
            newPatient.email = email
            """
            newEmployee.save()
            prof = newEmployee.enduser
            prof.PhoneNumber = PhoneNumber
            prof.Address = Address
            prof.State = State
            prof.City = City
            prof.ZipCode = ZipCode
            prof.ECFirstName = ECFirstName
            prof.ECLastName = ECLastName
            prof.ECPhoneNumber = ECPhoneNumber
            prof.isAdministrator = True
            prof.isPatient = False

            newEmployee.enduser = prof
            newEmployee.enduser.save()
            newEmployee.save()
            logEvent(event="performed first time setup", user=newEmployee.enduser)
            return redirect('setupHospital')
        print('invalid')
        print(form.errors)
    else:
        form = setup_AdminRegistrationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['d'] = getDate()

    return render_to_response('users/setup/registerAdmin.html', token)


def setup_registerHospital(request):
    if Hospital.objects.all():
        return redirect('index')
    else:
        if request.method == 'POST':
            form = createHospitalForm(request.POST)
            if form.is_valid():
                Name = form.cleaned_data['Name']
                Address = form.cleaned_data['Address']
                models.Hospital.objects.create(Name=Name, Address=Address)
                return redirect('index')
            return render(request, 'users/Hospital/addHospital.html', {'d': getDate()})
        else:
            form = createHospitalForm()
            return render(request, 'users/Hospital/addHospital.html', {'form': form, 'd': getDate()})


@login_required(login_url='login')
def compileStatistics(request):
    """
    Creates and shows healthNet statistics
    :param request:
    :return:
    """
    user = request.user
    profile = user.enduser
    if profile.isAdministrator:
        logEvent(profile, 'Accessed System Statistics.')
        descriptions = []
        statistics = []

        ##Number of users
        descriptions.append('Network Wide User Statistics')
        statistics.append('----------------')
        descriptions.append('Total number of users: ')
        descriptions.append('Total number of Patients: ')
        descriptions.append('Total number of Nurses: ')
        descriptions.append('Total Number of Docotrs: ')
        descriptions.append('Total Number of Secretaries: ')
        descriptions.append('Total Number of Administrators: ')
        number = 0
        doc = 0
        nurse = 0
        sec = 0
        pat = 0
        admin = 0
        for obj in User.objects.all():
            if obj.enduser.isAdministrator:
                admin += 1
            if obj.enduser.isDoctor:
                doc += 1
            if obj.enduser.isPatient:
                pat += 1
            if obj.enduser.isNurse:
                nurse += 1
            if obj.enduser.isSecretary:
                sec += 1
            number += 1
        statistics.append(number)
        statistics.append(pat)
        statistics.append(nurse)
        statistics.append(doc)
        statistics.append(sec)
        statistics.append(admin)

        ##Hospital Statistics
        descriptions.append('Hospital Statistics')
        statistics.append('----------------------')
        number = 0
        admitted = 0
        pat = 0
        nurse = 0
        doc = 0
        sec = 0
        for obj in Hospital.objects.all():
            descriptions.append('Hospital Name: ')
            statistics.append(obj.Name)
            patients = obj.patients
            patients = patients.split(',')
            for patient in patients:
                try:
                    user = User.objects.get(patient)
                    if user.enduser.isAdmitted:
                        admitted += 1
                    pat += 1
                except:
                    pass
            for nurses in obj.nurses.split(','):
                if nurses == '':
                    pass
                else:
                    nurse += 1
            for doctor in obj.doctors.split(','):
                if doctor == '':
                    pass
                else:
                    doc += 1
            for secretary in obj.secretaries.split(','):
                if secretary == '':
                    pass
                else:
                    secretary += 1
            descriptions.append('Total Number of Hospital Patients: ')
            statistics.append(pat)
            descriptions.append('Number of Admitted Patients: ')
            statistics.append(admitted)
            descriptions.append('Number of Nurses: ')
            statistics.append(nurse)
            descriptions.append('Number of Doctors: ')
            statistics.append(doc)
            descriptions.append('Number of Secretaries: ')
            statistics.append(sec)
            number += 1
        descriptions.append("Total Number of Hospitals: ")
        statistics.append(number)

        ##Messaging Statistics
        descriptions.append('Messaging Statistics')
        statistics.append('--------------------------')
        number = 0
        for message in Message.objects.all():
            number += 1
        descriptions.append('Number of Messages Sent: ')
        statistics.append(number)

        ##Prescriptions
        descriptions.append('Prescription Statistics')
        statistics.append('------------------')
        number = 0
        doctor = {}
        patient = {}
        drug = {}
        mostkey = ''
        mostvalue = 0
        for script in perscription.objects.all():
            if drug.get(script.perscription):
                drug[script.perscription] = drug.get(script.perscription) + 1
            else:
                drug[script.perscription] = 1
            if doctor.get(script.doctor):
                doctor[script.doctor] = doctor.get(script.doctor) + 1
            else:
                doctor[script.doctor] = 1
            if patient.get(script.patient):
                patient[script.patient] = patient.get(script.patient) + 1
            else:
                patient[script.patient] = 1
            number += 1
        descriptions.append('Total Number of Prescriptions: ')
        statistics.append(number)
        # drug
        for key in drug.keys():
            if drug.get(key) > mostvalue:
                mostkey = key
                mostvalue = drug.get(key)
        descriptions.append('Most Common Prescription: ')
        statistics.append(mostkey)
        descriptions.append('Number of Times Prescribed: ')
        statistics.append(mostvalue)

        # doctor
        mostkey = ''
        mostvalue = 0
        for key in doctor.keys():
            if doctor.get(key) > mostvalue:
                mostkey = key
                mostvalue = doctor.get(key)
        descriptions.append('Doctor with Most Prescriptions: ')
        statistics.append(mostkey)
        descriptions.append('Amount of Prescriptions: ')
        statistics.append(mostvalue)

        # patient
        mostkey = ''
        mostvalue = 0
        for key in patient.keys():
            if patient.get(key) > mostvalue:
                mostkey = key
                mostvalue = patient.get(key)
        descriptions.append('Patient with Most Prescriptions: ')
        statistics.append(mostkey)
        descriptions.append('Amount of Prescriptions: ')
        statistics.append(mostvalue)

        # render
        counter = []
        for i in range(0, len(descriptions)):
            counter.append(i)
        context = {'descriptions': descriptions, 'statistics': statistics, 'counter': counter, 'd': getDate(), 'user': user}

        return render(request, 'users/Statistics.html', context)
    else:
        return render(request, 'users/invalid.html', {'d': getDate()})


##DEBUG VIEW


def createPatient(username, firstName, lastName, email):
    newPatient = User.objects.create(username=username, first_name=firstName, last_name=lastName, email=email,
                                     password='pass321')
    newPatient.save()
    prof = newPatient.enduser
    prof.PhoneNumber = random.randint(5550000000, 5559999999)
    prof.Address = str(random.randint(1, 9999)) + ' Main Street'
    prof.State = 'New York'
    prof.City = 'Rochester'
    prof.ZipCode = 14623
    prof.ECFirstName = 'Robert'
    prof.ECLastName = 'Tables'
    prof.ECPhoneNumber = random.randint(5550000000, 5559999999)
    prof.dateOfBirth = str(random.randint(1, 12)) + '-' + str(random.randint(1, 29)) + '-' + str(
        random.randint(1930, 2001))

    prof.ProviderID = random.randint(111111111, 9999999999)
    prof.PolicyType = 'HMO'
    prof.PolicyNumber = random.randint(1111111111, 9999999999)
    prof.records = 'Had the swine flu in 2007'
    prof.isPatient = True

    hosp=Hospital.objects.all()
    hospital=hosp[0]
    hospital.patients+=(','+username)
    hospital.save()

    newPatient.enduser = prof
    newPatient.enduser.save()
    newPatient.save()
    logEvent(event="registered as " + newPatient.username + ".", user=newPatient.enduser)


def createDoctor(username, first_name, last_name, email):
    newPatient = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email,
                                     password='pass321')
    newPatient.save()
    prof = newPatient.enduser
    prof.PhoneNumber = random.randint(5550000000, 5559999999)
    prof.Address = str(random.randint(1, 9999)) + ' Main Street'
    prof.State = 'New York'
    prof.City = 'Rochester'
    prof.ZipCode = 14623
    prof.ECFirstName = 'Robert'
    prof.ECLastName = 'Tables'
    prof.ECPhoneNumber = random.randint(5550000000, 5559999999)
    prof.dateOfBirth = str(random.randint(1, 12)) + '-' + str(random.randint(1, 29)) + '-' + str(
        random.randint(1930, 2001))
    prof.isDoctor = True

    hosp = Hospital.objects.all()
    hospital = hosp[0]
    hospital.doctors += (',' + username)
    hospital.save()

    newPatient.enduser = prof
    newPatient.enduser.save()
    newPatient.save()
    logEvent(event="registered as " + newPatient.username + ".", user=newPatient.enduser)


def createNurse(username, first_name, last_name, email):
    newPatient = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email,
                                     password='pass321')
    newPatient.save()
    prof = newPatient.enduser
    prof.PhoneNumber = random.randint(5550000000, 5559999999)
    prof.Address = str(random.randint(1, 9999)) + ' Main Street'
    prof.State = 'New York'
    prof.City = 'Rochester'
    prof.ZipCode = 14623
    prof.ECFirstName = 'Robert'
    prof.ECLastName = 'Tables'
    prof.ECPhoneNumber = random.randint(5550000000, 5559999999)
    prof.dateOfBirth = str(random.randint(1, 12)) + '-' + str(random.randint(1, 29)) + '-' + str(
        random.randint(1930, 2001))
    prof.isNurse = True

    hosp = Hospital.objects.all()
    hospital = hosp[0]
    hospital.nurses += (',' + username)
    hospital.save()

    newPatient.enduser = prof
    newPatient.enduser.save()
    newPatient.save()
    logEvent(event="registered as " + newPatient.username + ".", user=newPatient.enduser)


def createSecretary(username, first_name, last_name, email):
    newPatient = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email,
                                     password='pass321')
    newPatient.save()
    prof = newPatient.enduser
    prof.PhoneNumber = random.randint(5550000000, 5559999999)
    prof.Address = str(random.randint(1, 9999)) + ' Main Street'
    prof.State = 'New York'
    prof.City = 'Rochester'
    prof.ZipCode = 14623
    prof.ECFirstName = 'Robert'
    prof.ECLastName = 'Tables'
    prof.ECPhoneNumber = random.randint(5550000000, 5559999999)
    prof.dateOfBirth = str(random.randint(1, 12)) + '-' + str(random.randint(1, 29)) + '-' + str(
        random.randint(1930, 2001))
    prof.isSecretary = True

    hosp = Hospital.objects.all()
    hospital = hosp[0]
    hospital.secretaries += (',' + username)
    hospital.save()

    newPatient.enduser = prof
    newPatient.enduser.save()
    newPatient.save()
    logEvent(event="registered as " + newPatient.username + ".", user=newPatient.enduser)


def createAdmin(username, first_name, last_name, email):
    newPatient = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email,
                                     password='pass321')
    newPatient.save()
    prof = newPatient.enduser
    prof.PhoneNumber = random.randint(5550000000, 5559999999)
    prof.Address = str(random.randint(1, 9999)) + ' Main Street'
    prof.State = 'New York'
    prof.City = 'Rochester'
    prof.ZipCode = 14623
    prof.ECFirstName = 'Robert'
    prof.ECLastName = 'Tables'
    prof.ECPhoneNumber = random.randint(5550000000, 5559999999)
    prof.dateOfBirth = str(random.randint(1, 12)) + '-' + str(random.randint(1, 29)) + '-' + str(
        random.randint(1930, 2001))
    prof.isAdministrator = True

    hosp = Hospital.objects.all()
    hospital = hosp[0]
    hospital.admins += (',' + username)
    hospital.save()

    newPatient.enduser = prof
    newPatient.enduser.save()
    newPatient.save()
    logEvent(event="registered as " + newPatient.username + ".", user=newPatient.enduser)


def createMessage():
    """
    Creates a random message between two users
    :return:
    """
    usernames = []
    for user in User.objects.all():
        usernames.append(user.username)
    sender = usernames[random.randint(0, len(usernames) - 1)]
    reciever = usernames[random.randint(0, len(usernames) - 1)]
    timesent=datetime.date.today()
    message = models.Message.objects.create(sender=sender, reciever=reciever, subject='Test', timeSent=timesent,
                                            message='This is a test message from a test profile')
    message.save()
    logEvent(user=User.objects.get(username=sender).enduser, event='sent a message to ' + reciever)


def createPerscriptions():
    """
    Creates random perscriptions between two users
    :return:
    """
    patientUsernames = []
    doctorUsernames = []
    num = random.randint(0, 5)
    drug = ''
    if num == 0:
        drug = 'Tylenol'
    if num == 1:
        drug = 'Xanax'
    if num == 2:
        drug = 'Adderall'
    if num == 3:
        drug = 'Amoxycillin'
    if num == 4:
        drug = 'Ibuprofen'
    if num==5:
        drug = 'Thalidomide'
    for user in User.objects.all():
        if user.enduser.isDoctor:
            doctorUsernames.append(user.username)
        if user.enduser.isPatient:
            patientUsernames.append(user.username)
    patient = patientUsernames[random.randint(0, len(patientUsernames) - 1)]
    doctor = doctorUsernames[random.randint(0, len(doctorUsernames) - 1)]
    dose = str(random.randint(50, 500)) + 'mg/day'
    newScript = models.perscription.objects.create(patient=patient, doctor=doctor, dose=dose, perscription=drug,
                                                   reason='This is a test perscription that was randomly created')
    newScript.save()
    logEvent(user=User.objects.get(username=doctor).enduser, event='Perscribed ' + drug + " to " + patient)


def addRandomPatient():
    """
    adds a random patient to a random doctor.
    :return:
    """
    patientUsernames = []
    doctorUsernames = []
    for user in User.objects.all():
        if user.enduser.isDoctor:
            doctorUsernames.append(user.username)
        if user.enduser.isPatient:
            patientUsernames.append(user.username)
    doctor = doctorUsernames[random.randint(0, len(doctorUsernames) - 1)]
    patient = patientUsernames[random.randint(0, len(patientUsernames) - 1)]
    doc = User.objects.get(username=doctor)
    pat = User.objects.get(username=patient)
    patprofile=pat.enduser
    profile = doc.enduser
    if patient in profile.Patients.split(','):
        pass
    else:
        profile.Patients += (','+ patient)
        patprofile.Doc+=(','+doctor)
    doc.enduser = profile
    doc.enduser.save()
    doc.save()
    pat.enduser.save()
    pat.save()
    logEvent(user=User.objects.get(username=doctor).enduser, event='added ' + patient + ' as a patient')


def populateHealthNet():
    # Create profiles
    try:
        createPatient('jsmith', 'John', 'Smith', 'jsmith@gmail.com')
        createPatient('JD95', 'Jack', 'Trevor', 'JT@gmail.com')
        createPatient('ga432', 'George', 'Arron', 'ga432@gmail.com')
        createPatient('jjones', 'John', 'Jones', 'jjones@gmail.com')
        createPatient('cvkln', 'Calvin', 'Keiper', 'cvkln@gmail.com')
        createPatient('yutvs', 'Yuri', 'Gregorin', 'yuvsa@gmail.com')
        createPatient('urqvs', 'Uniqua', 'Velize', 'urqvs@gmail.com')
        createPatient('yslvna', 'Hugo', 'Slavia', 'yslavia@gmail.com')
        createPatient('uqwqv', 'Urmeil', 'Anderson', 'Umas@gmail.com')
        createPatient('tzasf', 'Timothy', 'Gaines', 'tgaines@gmail.com')
        createPatient('tydfa', 'Try', 'djfa', 'tgsa@gmail.com')
        createPatient('patient', 'Peter', 'Piper', 'operq@gmail.com')
    except:
        pass
    try:
        createNurse('jsmitty', 'Jackie', 'Smitty', 'jsmith@gmail.com')
        createNurse('jb85', 'Judith', 'Barnes', 'aaeir@gmail.com')
        createNurse('qwerw', 'Quincy', 'Adams', 'JQA@gmail.com')
        createNurse('nurse', 'George', 'Washington', 'FNDFATH123@gmail.com')
        createNurse('jadmas', 'John', 'Adams', 'FNDFATH456@gmail.com')
        createDoctor('rj75', 'Richard', 'Johnson', 'RJOHNSON@gmail.com')
        createDoctor('doctor', 'Gregory', 'House', 'housemd@gmail.com')
        createDoctor('jwilson', 'James', 'Wilson', 'jwilsonMD@gmail.com')
        createDoctor('eforeman', 'Eric', 'Foreman', 'efore@gmail.com')
        createDoctor('rchase', 'Robert', 'Chase', 'rchase@gmail.com')
        createDoctor('acameron', 'Allison', 'Cameron', 'acameron@gmail.com')
    except:
        pass
    try:
        createSecretary('pjack', 'Perter', 'Jackson', 'pjack@gmail.com')
        createSecretary('hmarry', 'Holly', 'Marry', 'twofirstnames@gmail.com')
        createSecretary('jgeorge', 'John', 'George', 'jgeorge@gmail.com')
        createSecretary('jermi', 'Jennifer', 'Hewitt', 'jermi@gmail.com')
        createSecretary('secretary', 'John', 'Depp', 'jdepp@gmail.com')
        createAdmin('jt05', 'Jack', 'Travis', 'jt05@gmail.com')
        createAdmin('jdoe', 'John', 'Doe', 'doejo@gmail.com')
        createAdmin('bilb', 'William', 'Billy', 'willbill@gmail.com')
        createAdmin('lcuddy', 'Lisa', 'Cuddy', 'lcuddy@gmail.com')
        createAdmin('aadams', 'Amy', 'Adams', 'aadams@gmail.com')
    except:
        pass

    for i in range(0, 250):
        createMessage()
    for i in range(0, 50):
        createPerscriptions()
    for i in range(0, 50):
        addRandomPatient()


@login_required(login_url='login')
def confirmPopulateHealthNet(request):
    return render(request, 'users/setup/Populus.html')


@login_required(login_url='login')
def populateHealthnet(request):
    populateHealthNet()
    return redirect('home')
