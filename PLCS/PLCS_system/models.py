from django.db import models

from datetime import datetime, timedelta

# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length=15)
	last_name = models.CharField(max_length=15)
	email = models.CharField(max_length=45)
	password = models.CharField(max_length=15)

	status = models.IntegerField (default=1)
	date_of_registration = models.DateTimeField(default = datetime.today())
	last_login = models.DateTimeField(default  = datetime.today())

	profile_img = models.TextField(default='')

	learning_interests = models.TextField(default='')
	project_interests = models.TextField(default='')

	user_activity_tags = models.TextField(default='')

	user_description = models.TextField(default='I am a new user to this system')

	class Meta:
		db_table = "User"


	def __str__(self):
		return "id = {}, f_name = {}, email = {}, status = {}".format(self.id, self.first_name, self.email, self.status)


class Project (models.Model):
	project_id = models.CharField (max_length=15)
	project_title = models.CharField (max_length=300)
	project_description = models.TextField()
	project_DOR = models.DateTimeField(default = datetime.today())
	project_budget = models.IntegerField (default=1)

	project_skills = models.TextField(default='')
	project_collaborators = models.IntegerField (default=1)
	accepted_project_collaborators = models.IntegerField (default=1)
	project_deadline = models.DateTimeField(default = '')

	project_images = models.TextField(default='')
	project_files = models.TextField(default='')

	user_project = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	last_updated = models.DateTimeField(default = datetime.today())
	status = models.IntegerField(default=1)

	def __str__(self):
		return "id = {}, title = {}, status = {}".format(self.id, self.project_title, self.status)


class Permission (models.Model):
	permission_action = models.CharField (max_length=50, default='')

	def __str__(self):
		return "id = {}, action = {}".format(self.id, self.permission_action)


class Role (models.Model):
	role_name = models.CharField (max_length=15, default='normal user')
	role_description = models.CharField (max_length=150, default='normal user')
	
	def __str__(self):
		return "id = {}, role = {}".format(self.id, self.role_name)


class Role_Permission (models.Model):
	role = models.ForeignKey(Role, on_delete=models.CASCADE)
	permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
	
	def __str__(self):
		return "role = {}, permission = {}".format(self.role, self.permission)


class User_Permission (models.Model):
	user_p = models.ForeignKey(User, on_delete=models.CASCADE)
	permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
	
	def __str__(self):
		return "role = {}, permission = {}".format(self.user_p, self.permission)


class User_Role (models.Model):
	user_x = models.ForeignKey(User, on_delete=models.CASCADE)
	role_x = models.ForeignKey(Role, on_delete=models.CASCADE)
	
	def __str__(self):
		return "role = {}, permission = {}".format(self.user_x, self.role_x)


class Learning_Module (models.Model):
	module_title = models.CharField (max_length=50, default='')
	module_description = models.TextField(default='')
	module_tags = models.TextField(default='')

	module_creator = models.ForeignKey(User, on_delete=models.CASCADE)
	module_DOR = models.DateTimeField(default  = datetime.today())
	
	def __str__(self):
		return "title = {}, User = {}".format(self.module_title, self.module_creator)


class Notification (models.Model):
	notification_title = models.CharField (max_length=50, default='')
	notification_content = models.TextField(default='')
	notification_type = models.CharField (max_length=50, default='')

	notification_status = models.IntegerField (default=1)
	notification_link_to = models.CharField (max_length=50, default='')
	notification_date = models.DateTimeField(default  = datetime.today())

	notification_recipient = models.ForeignKey(User, on_delete=models.CASCADE)

	project_applied_to = models.CharField (max_length=50, default='')
	
	def __str__(self):
		return "id = {}, content = {}".format(self.id, self.notification_content)


class User_Project_Like (models.Model):	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	
	def __str__(self):
		return "id = {}, user = {}".format(self.id, self.user)


class User_Project_Collab (models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	collab_request_msg = models.TextField(default='')
	status = models.IntegerField(default=1)
	
	def __str__(self):
		return "id = {}, user = {}, project = {}".format(self.id, self.user, self.project)