from django.contrib import admin
from .models.user import User, UserAdmin

admin.site.register(User, UserAdmin)
# Register your models here.
