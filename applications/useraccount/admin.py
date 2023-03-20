from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(AdditionalInfo)
admin.site.register(Wallet)
admin.site.register(Follow)
admin.site.register(Subscribe)