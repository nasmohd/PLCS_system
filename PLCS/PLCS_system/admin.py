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
admin.site.register(User_Project_Like)
admin.site.register(User_Project_Collab)
admin.site.register(Summary)
admin.site.register(Collab_Task)
admin.site.register(Module_Topic)
admin.site.register(User_Project_Collabs_Approved)
admin.site.register(Saved_Project)
admin.site.register(Quiz)
