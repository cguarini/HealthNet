from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver







"""
Abstract class that contains all the information used by
all users.
"""
class endUser(models.Model):


    user = models.OneToOneField(User,on_delete=models.CASCADE)

    """
    Personal information, stored in User class:
    user.first_name,user.last_name,user.email,user.username
    """
    #Personal Information
    dateOfBirth=models.CharField(max_length=10, null=True, blank=True)
    #Contact Information
    PhoneNumber=models.IntegerField(null=True, blank=True)
    State=models.CharField(max_length=30, default="", blank=True)
    City=models.CharField(max_length=50, default="", blank=True)
    Address=models.CharField(max_length=50, default="", blank=True)
    ZipCode=models.IntegerField(null=True, blank=True)
    #Emergency Contact
    ECFirstName=models.CharField(max_length=25, default="", blank=True)
    ECLastName=models.CharField(max_length=25, default="", blank=True)
    ECPhoneNumber=models.IntegerField(null=True, blank=True)
    #backend
    isNurse=models.BooleanField(default=False)
    isDoctor=models.BooleanField(default=False)
    isAdministrator=models.BooleanField(default=False)
    isPatient=models.BooleanField(default=False)
    isSecretary=models.BooleanField(default=False)

    """
    Patient Information Field
    """
    Doc = models.TextField(default="", blank=True)
    Prescriptions = models.TextField(max_length=1000, default="",blank=True)
    # INSURANCE INFO
    ProviderID = models.IntegerField(null=True,blank=True)
    PolicyType = models.CharField(max_length=25, default="",blank=True)
    PolicyNumber = models.IntegerField(null=True,blank=True)
    records = models.TextField(max_length=5000, default="", null=True,blank=True)

    """
    Patient Admission Fields
    """
    isAdmitted = models.BooleanField(default=False, blank=True)
    aReason = models.CharField(max_length=100, default="", blank=True)
    aCount = models.IntegerField(default=0, blank=True)
    aTime = models.DateTimeField(null=True, blank=True)

    """
    Employee Information Fields
    """
    OCPhoneNumber = models.IntegerField(null=True,blank=True)
    Patients = models.TextField(default="", blank=True)
    def addPatient(self,user):
        self.Patients.append(user)
        self.save()
    def __str__(self):
        return self.user.last_name+", "+self.user.first_name
    #REQUIRED_FIELDS = ['dateOfBirth','PhoneNumber','State','City',
     #                  'Address','ZipCode']

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        endUser.objects.create(user=instance)

class log(models.Model):
    user=models.ForeignKey('endUser',blank=True,null=True)
    event=models.CharField(max_length=50,default="an event happened")
    date=models.DateField()
    time=models.TimeField()
    def __str__(self):
        return str(self.date)+ " "+str(self.time)+" "+str(self.user)+": "+str(self.event)

class Message(models.Model):
    sender=models.CharField(max_length=50,default='')
    reciever=models.CharField(max_length=50,default='')
    message=models.TextField(max_length=1000,default='',blank=True)
    subject=models.CharField(max_length=100,default='')
    timeSent=models.DateField(null=True)

#do not use this one
class TestResult(models.Model):
    doctor_fn=models.CharField(max_length=50, default='')
    patient_fn=models.CharField(max_length=50, default='')
    pending=models.BooleanField(default=True)
    information=models.CharField(max_length=200, default='', blank=True, null=True)
    results=models.CharField(max_length=200, default='', blank=True, null=True)

class TestResults(models.Model):
    doctor_fn=models.CharField(max_length=50, default='')
    patient_fn=models.CharField(max_length=50, default='')
    pending=models.BooleanField(default=True)
    information=models.CharField(max_length=200, default='', blank=True, null=True)
    results=models.CharField(max_length=200, default='', blank=True, null=True)
    file=models.FileField(upload_to='documents/', null=True)

class doctorRequest(models.Model):
    patient=models.CharField(max_length=50,default='')
    doctor=models.CharField(max_length=50,default='')
    reason=models.TextField(max_length=250,default='',null=True)

class perscription(models.Model):
    patient = models.CharField(max_length=50, default='')
    doctor = models.CharField(max_length=50, default='')
    perscription= models.CharField(max_length=50, default='')
    dose= models.CharField(max_length=50, default='')
    reason = models.TextField(max_length=250, default='', null=True)

class Hospital(models.Model):
    patients=models.TextField(default='')
    doctors=models.TextField(default='')
    nurses=models.TextField(default='')
    secretaries=models.TextField(default='')
    admins=models.TextField(default='')
    Name=models.CharField(max_length=100, default='')
    Address=models.TextField(max_length=300,default='')

