from django.contrib import admin

from .models import Appointment

class ItemAdmin(admin.ModelAdmin):
    #allows admins to make appointments and edit all fields of them
    #NOTE, THE USER MUST MANUALLY MAKE SURE 'day', 'month', AND 'year' MATCH THE DATE IN 'begins'
    #(I will probably fix that before R2, but it works for now. Call it an Evolutionary Prototype)
    fieldsets = [
        (None, {'fields': ['begins']}),
        (None, {'fields': ['length']}),
        (None, {'fields': ['day']}),
        (None, {'fields': ['month']}),
        (None, {'fields': ['year']}),
        (None, {'fields': ['location']})
    ]
    list_display = ('begins', 'day', 'month', 'year', 'length', 'location')

admin.site.register(Appointment, ItemAdmin)