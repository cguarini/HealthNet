#!python
# log/urls.py
from django.conf.urls import patterns, url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^profile$',views.profile, name='profile'),
    url(r'^profile/edit/$', views.editProfile,name='UpdateProfile'),
    url(r'^$', views.index, name='index'),#This points to the home page
    url(r'^patient/$',views.patientView, name='patient'),
    url(r'^nurse/$',views.NurseView, name='nurse'),
    url(r'^doctor/$',views.DoctorView, name='doctor'),
    url(r'^adminview/$',views.adminView,name='adminview'),
    url(r'^secretaryview/$', views.secretaryView,name='secretaryview'),
    url(r'^tools/$',views.specialtyScreen,name='tools'),
    url(r'^employeeregistration/$',views.registerEmployee,name='registerEmployee'),

    #Admissions and Discharge urls
    url(r'^admission/$',views.admissions,name='admissions'),
    url(r'^admissions/admit/$',views.admitPatient,name='admit'),
    url(r'^admissions/discharge/$',views.discharge,name='discharge'),
    url(r'^admissions/admitted/$',views.viewAdmitted,name='admitted'),

    url(r'^log/$',views.showActivityLog,name='log'),

    #Doctor Requests
    url(r'^tools/patient/request',views.requestDoctor,name='request'),
    url(r'^tools/doctor/requests',views.viewRequests, name='requests'),
    url(r'^tools/doctor/request/accept/(?P<pk>[0-9]+)',view=views.acceptRequest,name='acceptRequest'),

    url(r'^directory',views.patientDirectory,name='directory'),
    url(r'^accounts/patientProfile/(?P<patientPK>[0-9]+)',view=views.viewPatientProfile,name='patientProfile'),
    url(r'^accounts/updateMedicalInfo/(?P<patientPK>[0-9]+)',view=views.updateMedicalInfo,name='updateMedicalInfo'),
    url(r'^tools/addToPatients/$',view=views.addToPatients,name='addToPatients'),
    url(r'^messaging/sendmessage/$',view=views.sendMessage,name='SendMessage'),
    url(r'^messaging/sentMessages/$',view=views.Outbox,name='OutBox'),
    url(r'^messaging/inbox/$',view=views.Inbox,name='Inbox'),
    url(r'^messaging/$',view=views.messagingCenter,name='messagingCenter'),
    url(r'^messaging/message/(?P<messagePK>[0-9]+)',view=views.viewMessage,name='viewMessage'),
    url(r'^makeTest/$', view=views.createTest, name='makeTest'),
    url(r'^myTests/$', view=views.testCenter, name='myTests'),
    url(r'^myRequests/$',view=views.requests, name="requests"),
    url(r'^viewTest/(?P<testPK>[0-9]+)',view=views.viewTest,name='viewTest'),
    url(r'^editTest/(?P<testPK>[0-9]+)',view=views.editTest,name='editTest'),
#Request Stuff
    url(r'^viewRequest/(?P<requestPK>[0-9]+)',view=views.viewRequest,name='viewRequest'),
    url(r'^deleteRequest/(?P<requestPK>[0-9]+)', view=views.deleteRequest, name='deleteRequest'),
    url(r'^acceptRequest/(?P<requestPK>[0-9]+)', view=views.acceptRequest, name='acceptRequest'),
# Registration URLs
    url(r'^accounts/register/$', views.register, name='register'),

    #Perscription URLs
    url(r'^perscriptions/$',views.persriptionScreen,name='perscriptions'),
    url(r'^perscriptions/perscribe/$',views.perscribe,name='perscribe'),
    url(r'^perscriptions/viewPerscriptions/$',views.viewPerscriptions,name='viewPerscriptions'),
    url(r'^perscriptions/viewPerscription/(?P<perscriptionPK>[0-9]+)',views.viewPerscription,name='viewPerscription'),
    url(r'^perscriptions/deletePerscription/(?P<perscriptionPK>[0-9]+)',views.deletePerscription,name='deletePerscription'),

    #Hospital URLS
    url(r'^tools/addHospital/$',view=views.createHospital,name='createHospital'),
    url(r'^tools/hospitalCenter/$',view=views.hospitalCenter,name='hospitalCenter'),
    url(r'^tools/hospitalCenter/viewHospitals/$',view=views.viewHospitals,name='viewHospitals'),
    url(r'^tools/hospitalCenter/(?P<HospitalPK>[0-9]+)/$',view=views.viewHospital,name='viewHospital'),
    url(r'^tools/hospitalCenter/(?P<HospitalPK>[0-9]+)/patients', view=views.viewPatients, name='viewPatients'),
    url(r'^tools/hospitalCenter/(?P<HospitalPK>[0-9]+)/doctors', view=views.viewDoctors, name='viewDoctors'),
    url(r'^tools/hospitalCenter/(?P<HospitalPK>[0-9]+)/nurses', view=views.viewNurses, name='viewNurses'),
    url(r'^tools/hospitalCenter/(?P<HospitalPK>[0-9]+)/secretaries', view=views.viewSecretaries, name='viewSecretaries'),
    url(r'^tools/hospitalCenter/(?P<HospitalPK>[0-9]+)/(?P<number>[0-9]+)', view=views.transfer,name='transfer'),




    #Fun URLs
    url(r'^contact_us/$', views.contact,name="contact"),
    url(r'^report_error/$', views.reporterror,name="reporterror"),
    url(r'^feedback/$',views.feedback,name="feedback"),
    url(r'^terms/$', views.terms,name="terms"),

    #First Time Setup
    url(r'^setup/$',views.setup,name='setup'),
    url(r'^setup/admin/$',views.setup_registerAdmin,name='setupAdmin'),
    url(r'^setup/hospital/$',views.setup_registerHospital,name='setupHospital'),

    #System Statistics
    url(r'^tools/admin/statistics/$',view=views.compileStatistics,name='stats'),

    #DEBUG
    url(r'^tools/admin/debug/$', view=views.confirmPopulateHealthNet, name='debug'),
    url(r'^tools/admin/populus/IAMGOD/$', view=views.populateHealthnet,name='populus'),

]
