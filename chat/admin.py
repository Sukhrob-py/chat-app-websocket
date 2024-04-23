from django.contrib import admin

# Register your models here.
from .models import Room, Messages

admin.site.register(Room)
admin.site.register(Messages)
