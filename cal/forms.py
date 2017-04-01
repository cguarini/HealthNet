from django import forms
from cal.models import Appointment
from users.models import endUser, User
import datetime




class makeAppointmentForm(forms.ModelForm):

    length=forms.DurationField(widget=forms.TimeInput(attrs={'placeholder': 'ex: 01:30:00', 'class': 'form-control'}),
                               label='Appointment Length', required=True)

    date=forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'ex: 6/30/2039', 'class': 'form-control'}),
                         label='Date of Appointment', required=True)

    begins=forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'ex: 14:45', 'class': 'form-control'}),
                           label='Time Appointment Starts (uses military time)', required=True)

    location=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'This will always be your own hospital',
                                                           'class': 'form-control', 'readonly' : 'True'}),
                             label='Location', required=False,)

    doctorID=forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': '99', 'class': 'form-control'}),
                                label='Doctor ID', required=True)
    patientID=forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': '99', 'class': 'form-control'}),
                                 label='Patient ID', required=True)

    def clean(self):
        docID = self.cleaned_data.get('doctorID')
        patID = self.cleaned_data.get('patientID')
        if len(endUser.objects.filter(id=docID)) == 0:
            raise forms.ValidationError(message="Doctor with that ID does not exist")
        elif not endUser.objects.filter(id=docID)[0].isDoctor:
            raise forms.ValidationError(message="Doctor with that ID does not exist")

        if len(endUser.objects.filter(id=patID)) == 0:
            raise forms.ValidationError(message="Patient with that ID does not exist")
        elif not endUser.objects.filter(id=patID)[0].isPatient:
            raise forms.ValidationError(message="Patient with that ID does not exist")

        doctorAppointments = Appointment.objects.filter(doctorID= self.cleaned_data.get('doctorID'))
        patientAppointments = Appointment.objects.filter(patientID= self.cleaned_data.get('patientID'))

        begins=self.cleaned_data.get('begins')
        date=self.cleaned_data.get('date')
        length = self.cleaned_data.get('length')
        fullTime = datetime.datetime(date.year, date.month, date.day, begins.hour, begins.minute)
        return self.cleaned_data

    class Meta:
        model=Appointment
        fields =['length', 'location']

class editAppointmentForm(forms.ModelForm):

    length=forms.DurationField(widget=forms.TimeInput(attrs={'placeholder': 'ex: 01:30:00', 'class': 'form-control'}),
                               label='Appointment Length', required=True)

    date=forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'ex: 6/30/2039', 'class': 'form-control'}),
                         label='Date of Appointment', required=True)

    begins=forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'ex: 14:45', 'class': 'form-control'}),
                           label='Time Appointment Starts (uses military time)', required=True)

    location=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'This will always be your own hospital',
                                                           'class': 'form-control', 'readonly' : 'True'}),
                             label='Location', required=False)

    class Meta:
        model = Appointment
        fields = ['length', 'location']
