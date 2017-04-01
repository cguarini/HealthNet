from django import forms
from users.models import endUser, Message, TestResult, perscription, doctorRequest, Hospital
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        username = forms.CharField(label="Username", max_length=30,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
        password = forms.CharField(label="Password", max_length=30,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'password'}))


class editUserProfile(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@example.com',
                                                            'class': 'form-control'}), label='Email Address',
                             required=True)
    PhoneNumber = forms.RegexField(label='Phone Number',
                                   min_length=10,
                                   max_length=10,
                                   regex=r'[0-9]+',
                                   widget=forms.TextInput(attrs={'placeholder': '##########', 'class': 'form-control'}),
                                   required=True)
    State = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
                            label='State', required=True)
    City = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}), label='City',
                           required=True)
    Address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g.(123 Awesome Ave)',
                                                            'class': 'form-control'}), label='Address', required=True)
    ZipCode = forms.RegexField(label='Zip Code',
                               min_length=5,
                               max_length=5,
                               regex=r'[0-9]+',
                               widget=forms.TextInput(attrs={'placeholder': '#####', 'class': 'form-control'}),
                               required=True)
    ECFirstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                  label='Emergency Contact First Name',
                                  max_length=30)
    ECLastName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                 label='Emergency Contact Last Name',
                                 max_length=30)
    ECPhoneNumber = forms.RegexField(label='Emergency Contact Phone Number',
                                     max_length=10,
                                     min_length=10,
                                     regex=r'[0-9]+',
                                     widget=forms.TextInput(attrs={'placeholder': '##########',
                                                                   'class': 'form-control'}))

    class Meta:
        model = endUser
        fields = ['email',
                  'dateOfBirth', 'PhoneNumber', 'State', 'City',
                  'Address', 'ZipCode', 'ECFirstName', 'ECLastName',
                  'ECPhoneNumber']


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control'}), label='Username')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password Again',
                                                                  'class': 'form-control'}),
                                label='Retype Password')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                 label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                label='Last Name')
    dateOfBirth = forms.CharField(widget=forms.DateInput(attrs={'placeholder': 'MM-DD-YYYY', 'class': 'form-control'}),
                                  label='Date of Birth',
                                  max_length=10)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@example.com',
                                                            'class': 'form-control'}), label='Email Address')

    # Personal info
    PhoneNumber = forms.RegexField(label='Phone Number',
                                   min_length=10,
                                   max_length=10,
                                   regex=r'[0-9]+',
                                   widget=forms.TextInput(attrs={'placeholder': '##########', 'class': 'form-control'}))
    Address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g.(123 Awesome Ave)',
                                                            'class': 'form-control'}), label='Address')
    City = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}), label='City')
    State = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
                            label='State')
    ZipCode = forms.RegexField(label='Zip Code',
                               min_length=5,
                               max_length=5,
                               regex=r'[0-9]+',
                               widget=forms.TextInput(attrs={'placeholder': '#####', 'class': 'form-control'}))

    ProviderID = forms.IntegerField(label='ProviderID',
                                    widget=forms.TextInput(attrs={'placeholder': '##########',
                                                                  'class': 'form-control'}))
    PolicyType = forms.CharField(label='Policy Type',
                                 widget=forms.TextInput(attrs={'placeholder': "My Awesome Policy",
                                                               'class': 'form-control'}),
                                 max_length=25)
    PolicyNumber = forms.IntegerField(label='Policy Number',
                                      widget=forms.TextInput(attrs={'placeholder': '##########',
                                                                    'class': 'form-control'})
                                      )
    records = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Broke funny bone',
                                                           'class': 'form-control'}),
                              max_length=5000,
                              label='Medical Records')
    ECFirstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                  label='Emergency Contact First Name',
                                  max_length=30)
    ECLastName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                 label='Emergency Contact Last Name',
                                 max_length=30)
    ECPhoneNumber = forms.RegexField(label='Emergency Contact Phone Number',
                                     max_length=10,
                                     min_length=10,
                                     regex=r'[0-9]+',
                                     widget=forms.TextInput(attrs={'placeholder': '##########',
                                                                   'class': 'form-control'}))
    Hospital = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Im Dying Help! Hospital',
                                                             'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(message='Username: ' + username + 'taken. Please select a different username.')

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("The passwords do not match")
        return self.cleaned_data

    def clean_Hospital(self):
        hosp = self.cleaned_data.get('Hospital')
        try:
            Hospital.objects.get(Name=hosp)
            return hosp
        except Hospital.DoesNotExist:
            raise forms.ValidationError(message='Hospital: ' + hosp + ', is not in our database.')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'PhoneNumber', 'Address', 'City',
                  'State', 'ZipCode', 'ECFirstName', 'ECLastName', 'ECPhoneNumber']


class EmployeeRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
                               label='Username')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password Again', 'class': 'form-control'}),
        label='Retype Password')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                 label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                label='Last Name')
    dateOfBirth = forms.CharField(widget=forms.DateInput(attrs={'placeholder': 'MM-DD-YYYY', 'class': 'form-control'}),
                                  label='Date of Birth',
                                  max_length=10)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'example@example.com', 'class': 'form-control'}),
        label='Email Address')

    # Personal info
    PhoneNumber = forms.RegexField(label='Phone Number',
                                   min_length=10,
                                   max_length=10,
                                   regex=r'[0-9]+',
                                   widget=forms.TextInput(attrs={'placeholder': '##########', 'class': 'form-control'}))
    Address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g.(123 Awesome Ave)', 'class': 'form-control'}),
        label='Address')
    City = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}), label='City')
    State = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
                            label='State')
    ZipCode = forms.RegexField(label='Zip Code',
                               min_length=5,
                               max_length=5,
                               regex=r'[0-9]+',
                               widget=forms.TextInput(attrs={'placeholder': '#####', 'class': 'form-control'}))
    ECFirstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                  label='Emergency Contact First Name',
                                  max_length=30)
    ECLastName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                 label='Emergency Contact Last Name',
                                 max_length=30)
    ECPhoneNumber = forms.RegexField(label='Emergency Contact Phone Number',
                                     max_length=10,
                                     min_length=10,
                                     regex=r'[0-9]+',
                                     widget=forms.TextInput(
                                         attrs={'placeholder': '##########', 'class': 'form-control'}))

    Hospital = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Im Dying Help! Hospital',
                                                             'class': 'form-control'}))

    # backend
    isNurse = forms.BooleanField(label='Nurse: ', required=False)
    isDoctor = forms.BooleanField(label='Doctor: ', required=False)
    isAdministrator = forms.BooleanField(label='Administrator', required=False)
    isSecretary = forms.BooleanField(label='Secretary', required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(message='Username: ' + username + 'taken. Please select a different username.')

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("The passwords do not match")
        return self.cleaned_data

    def clean_Hospital(self):
        hosp = self.cleaned_data.get('Hospital')
        try:
            Hospital.objects.get(Name=hosp)
            return hosp
        except Hospital.DoesNotExist:
            raise forms.ValidationError(message='Hospital: ' + hosp + ', is not in our database.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email',
                  'password1', 'password2',
                  'PhoneNumber', 'State', 'City',
                  'Address', 'ZipCode', 'ECFirstName', 'ECLastName',
                  'ECPhoneNumber', 'isSecretary', 'isNurse', 'isDoctor', 'isAdministrator']


class admitPatientForm(forms.ModelForm):
    patient = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'xyz99',
                                                            'class': 'form-control'}), max_length=50)
    reason = message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Reason text here.', 'class': 'form-control'}),
        required=False)

    class Meta:
        model = User
        fields = ['patient', 'reason']


class dischargePatientForm(forms.ModelForm):
    patient = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'xyz99',
                                                            'class': 'form-control'}), max_length=50)

    class Meta:
        model = User
        fields = ['patient']


class addToPatientsForm(forms.ModelForm):
    patient = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'xyz99',
                                                            'class': 'form-control'}), max_length=50)

    class Meta:
        model = User
        fields = ['patient']


class updateMedicalForm(forms.ModelForm):
    # INSURANCE INFO
    records = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Medical Info', 'class': 'form-control'}),
                              required=False)
    ProviderID = forms.IntegerField(label='ProviderID',
                                    widget=forms.TextInput(attrs={'placeholder': '##########',
                                                                  'class': 'form-control'}), required=False)
    PolicyType = forms.CharField(label='Policy Type',
                                 widget=forms.TextInput(attrs={'placeholder': "My Awesome Policy",
                                                               'class': 'form-control'}),
                                 max_length=25, required=False)
    PolicyNumber = forms.IntegerField(label='Policy Number',
                                      widget=forms.TextInput(attrs={'placeholder': '##########',
                                                                    'class': 'form-control'}), required=False)

    class Meta:
        model = endUser
        fields = ['records']


class sendMessageForm(forms.ModelForm):
    reciever = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'user123', 'class': 'form-control'}),
                               max_length=50)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Message text here.', 'class': 'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Message Subject',
                                                            'class': 'form-control'}),
                              max_length=100)

    class Meta:
        model = Message
        fields = ['reciever', 'subject', 'message']


class testForm(forms.ModelForm):
    doctor = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'John', 'class': 'form-control'}),
                             max_length=50)
    patient = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'John', 'class': 'form-control'}),
                              max_length=50)
    pending = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), required=False)
    information = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Information here.', 'class':
        'form-control'}), required=False)
    results = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Results here.', 'class':
        'form-control'}), required=False)
    file = forms.FileField(required=False)

    class Meta:
        model = TestResult
        fields = ['doctor', 'patient', 'pending', 'information', 'results', 'file']


class perscribeForm(forms.ModelForm):
    patient = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'xyz99',
                                                            'class': 'form-control'}),
                              max_length=100)
    perscription = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Prescription',
                                                                 'class': 'form-control'}),
                                   max_length=100)
    dose = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Dose',
                                                         'class': 'form-control'}),
                           max_length=100)
    reason = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Reason', 'class': 'form-control'}))

    class Meta:
        model = perscription
        fields = ['patient', 'perscription', 'dose', 'reason']


class doctorRequestForm(forms.ModelForm):
    doctor = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'xyz99',
                                                           'class': 'form-control'}), max_length=50)
    reason = message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Reason text here.', 'class': 'form-control'}),
        required=False)

    def clean_doctor(self):
        doctor = self.cleaned_data.get('doctor')
        doctors = []
        for obj in User.objects.all():
            if obj.enduser.isDoctor:
                doctors.append(obj.username)
        if not doctor in doctors:
            raise forms.ValidationError(message='Doctor: ' + doctor + ', is not in our database.')
        return doctor

    class Meta:
        model = User
        fields = ['doctor', 'reason']


class createHospitalForm(forms.ModelForm):
    Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Hospital Place',
                                                           'class': 'form-control'}), max_length=50)
    Address = message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': '123 Awesome Ave...', 'class': 'form-control'}),
        required=False)

    class Meta:
        model = Hospital
        fields = ['Name', 'Address']


class transferForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'xyz99',
                                                             'class': 'form-control'}), max_length=50)

    class Meta:
        model = Hospital
        fields = ['username']

class setup_AdminRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
                               label='Username')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password Again', 'class': 'form-control'}),
        label='Retype Password')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                 label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                label='Last Name')
    dateOfBirth = forms.CharField(widget=forms.DateInput(attrs={'placeholder': 'MM-DD-YYYY', 'class': 'form-control'}),
                                  label='Date of Birth',
                                  max_length=10)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'example@example.com', 'class': 'form-control'}),
        label='Email Address')

    # Personal info
    PhoneNumber = forms.RegexField(label='Phone Number',
                                   min_length=10,
                                   max_length=10,
                                   regex=r'[0-9]+',
                                   widget=forms.TextInput(attrs={'placeholder': '##########', 'class': 'form-control'}))
    Address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g.(123 Awesome Ave)', 'class': 'form-control'}),
        label='Address')
    City = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}), label='City')
    State = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
                            label='State')
    ZipCode = forms.RegexField(label='Zip Code',
                               min_length=5,
                               max_length=5,
                               regex=r'[0-9]+',
                               widget=forms.TextInput(attrs={'placeholder': '#####', 'class': 'form-control'}))
    ECFirstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                  label='Emergency Contact First Name',
                                  max_length=30)
    ECLastName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                 label='Emergency Contact Last Name',
                                 max_length=30)
    ECPhoneNumber = forms.RegexField(label='Emergency Contact Phone Number',
                                     max_length=10,
                                     min_length=10,
                                     regex=r'[0-9]+',
                                     widget=forms.TextInput(
                                         attrs={'placeholder': '##########', 'class': 'form-control'}))


    # backend
    isNurse = forms.BooleanField(label='Nurse: ', required=False)
    isDoctor = forms.BooleanField(label='Doctor: ', required=False)
    isAdministrator = forms.BooleanField(label='Administrator', required=False)
    isSecretary = forms.BooleanField(label='Secretary', required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(message='Username: ' + username + 'taken. Please select a different username.')

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("The passwords do not match")
        return self.cleaned_data

    def clean_Hospital(self):
        hosp = self.cleaned_data.get('Hospital')
        try:
            Hospital.objects.get(Name=hosp)
            return hosp
        except Hospital.DoesNotExist:
            raise forms.ValidationError(message='Hospital: ' + hosp + ', is not in our database.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email',
                  'password1', 'password2',
                  'PhoneNumber', 'State', 'City',
                  'Address', 'ZipCode', 'ECFirstName', 'ECLastName',
                  'ECPhoneNumber', 'isSecretary', 'isNurse', 'isDoctor', 'isAdministrator']
