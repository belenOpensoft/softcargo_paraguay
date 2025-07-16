"""
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from login.models import Account
from django.contrib.auth.models import User


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Datos para envio de email'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline,)

admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)
"""


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from login.models import Account, AccountEmail


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Datos de cuenta'
    show_change_link = True


class AccountEmailInline(admin.TabularInline):
    model = AccountEmail
    extra = 1
    verbose_name_plural = 'Emails adicionales'


class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, AccountEmailInline)


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
