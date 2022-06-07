from django.contrib import admin

from .models import User, Chirp
# Register your models here.
admin.site.register(User)
admin.site.register(Chirp)