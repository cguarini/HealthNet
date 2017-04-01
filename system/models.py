from django.db import models
import time
from django.db import models
from abc import ABCMeta,abstractmethod
from django.contrib.auth.models import Permission, User, AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
"""
"""
#edit account permissions
"""
class editPermissions(models.Model):
    account=user
    def changeTarget(self)
        user.permissions = !user.permissions
        
""""""
Private Message
contains To/From, text of message, and timestamp
recipient & sender can see PMs from account page
""""""
class privateMsg(object):
    def __init__(self,recipient,msg_text):
        recipient = models.CharField(max_length=15,default="")+", "
        +models.CharField(max_length=15,default="")
        sender = models.ForeignKey(this.User, on_delete=models.CASCADE)
        msg_text = models.TextField()
        timestamp = time.gmtime()
        sent = False

    def send(self)
        if (sent = False && users.contains(recipient)):
            recipient = models.ForeignKey(users[recipient], on_delete=models.CASCADE)


    
""""""
Compiles statistics of activity log
@param: start(dateField) -
"""
"""

class Statistics(models.Model):
    def __init__(self):
        FrequencyX = 0
        FrequencyY = 0
        log = Log
        while(log.has_next()):
            event = log.get_event
            if (event = X):
                FrequencyX++
            elif (event = Y):
                FrequencyY++
            else:
                pass
            log = log.get_next
        }

    def __str__(self):
        stats = ""
        stats += "Number of X: " + FrequencyX
        stats += "\nNumber of Y: " + FrequencyY
        return stats



"""
"""
Simple linked list for use as activity log
Records time of creation
@param: event (str)-description of event
        previousEvent(linkedActivityLog)-link to the list
        when(seconds)-time of creation
"""


class linkedActivityLog(object):

    def __init__(self,user,event,previousEvent):
        self.user=user
        self.event=event
        self.previousEvent=previousEvent
        self.when=time.gmtime()

    def get_event(self):
        return self.event

    def get_when(self):
        return self.when

    def get_next(self):
        return self.previousEvent

    def set_next(self, new_event):
        self.previousEvent=new_event

    def has_next(self):
        return (self.get_next != None)

    def __str__(self):
        if self.user!=None:
            return (self.user.username+"-"+self.event)
        else:
            return ("log was created")

"""
The actual activity log
This records all activity in the hospital
Must be called when an action is done.
"""

class activityLog(models.Model):
    Log=None
    def createLog(self):
        self.Log=linkedActivityLog(event="Log created",previousEvent=None, user=None)
        self.save()

    def logEvent(self,event,user):
        newEvent=linkedActivityLog(event=event,previousEvent=self.Log,user=user)
        self.Log=newEvent
        self.save()

    def printLog(self):
        pointer=self.Log
        while(pointer!=None):
            print(pointer)
            pointer=pointer.get_next()



# Create your models here.
