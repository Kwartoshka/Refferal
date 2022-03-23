from django.contrib import admin

# Register your models here.
from .models import ReferralUser, MyToken, ConfirmationCode


@admin.register(ReferralUser)
class ReferralUserAdmin(admin.ModelAdmin):
    pass

@admin.register(MyToken)
class MyTokenAdmin(admin.ModelAdmin):
    pass

@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    pass