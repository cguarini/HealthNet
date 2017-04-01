from django.db import models
from users.models import endUser

import datetime

class Appointment(models.Model):
    """
    The appointment class that all appointments will be made from
    """
    begins = models.DateTimeField(default=datetime.datetime.now())
    doctorID = models.IntegerField(null=True)
    patientID = models.IntegerField(null=True)
    length = models.DurationField(default=datetime.timedelta(minutes = 45))
    location = models.TextField(max_length=80, default="")
    # these attributes may seem redundant but they are needed for my implementation of the calendar views
    day = models.IntegerField(default=datetime.datetime.today().day)
    month = models.IntegerField(default=datetime.datetime.today().month)
    year = models.IntegerField(default=datetime.datetime.today().year)

