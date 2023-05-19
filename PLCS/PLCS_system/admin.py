from django.contrib import admin

# Register your models here.
from PLCS_system.models import *

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Role_Permission)
admin.site.register(User_Permission)
admin.site.register(User_Role)
admin.site.register(Learning_Module)
admin.site.register(Notification)
