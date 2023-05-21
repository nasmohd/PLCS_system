from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect

# from PLCS_system.models import User
from django.core.cache import cache

from PLCS_system.models import *

from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login

from django.contrib import messages #import messages
# import date

#Delete session after some time passes

from ast import literal_eval

from django.core.paginator import Paginator


# Create your views here.
def login(request):
	# return HttpResponse ("Hello")
	return render (request, "login.html")
	# return HttpResponse ("Hello")


def register(request):
	# return HttpResponse ("Hello")
	return render (request, "register.html")


# def login_user(request, user):
def login_user(request):
	session_val = check_session(request, 'url_to_redirect_to')

	# if user:
	# 	return redirect ('/dashboard')

	if (session_val == 'session_true'):
		return redirect ('/dashboard')

	else:
		if request.method == "POST":
			#GET PERMISSIONS OF THIS USER


			email_input = request.POST["email"]
			password_input = request.POST["password"]

			check_DB_user_details = User.objects.filter(email = email_input)
			if (check_DB_user_details.exists()):
				if (check_DB_user_details[0].password == password_input):

					#Create Session for User
					request.session['email'] = check_DB_user_details[0].email
					request.session['roles_n_permissions'] = get_roles_permissions(request, check_DB_user_details[0].id)
					request.session['user_id'] = check_DB_user_details[0].id
					request.session['user_names'] = [check_DB_user_details[0].first_name, check_DB_user_details[0].last_name]
					# request.session['roles'] = request.session['roles_n_permissions'][0]
					# request.session['permissions'] = request.session['roles_n_permissions'][1]

					# return HttpResponse (request.session['roles_n_permissions'])

					# request.session['permissions'] = get_permissions(request, check_DB_user_details[0].id)
					# return HttpResponse (request.session['roles_n_permissions'])


					# if ('User' in request.session['roles_n_permissions'][0]):
					# 	return HttpResponse('Yk')


					return redirect('/dashboard') 
					# return HttpResponse (check_DB_user_details[0].password)

				else:
					return redirect('/')

			else:
				return redirect('/') 

		return redirect('/')


def dashboard(request):
	session_val = check_session(request, 'url_to_redirect_to')

	get_all_users = User.objects.exclude(status = 2).order_by('-date_of_registration')

	roles_n_permissions = request.session['roles_n_permissions']

	if (session_val == 'session_true'):
		return render (request, "admin_dashboard.html", {'all_users': get_all_users, 'roles_n_permissions': roles_n_permissions})
		# return render (request, "dashboard.html")

	else:
		return redirect ('/')


def register_user(request):
	# return HttpResponse("Hey")

	if request.method == "POST":

		first_name_input = request.POST["first_name"]
		last_name_input = request.POST["last_name"]
		email_input = request.POST["email"]
		password_input = request.POST["password"]
		confirm_password_input = request.POST["confirm_password"]

		#If email does not exist/ User is not registered yet
		if not (User.objects.filter(email=email_input).exists()):
			user = User()
			user.first_name = first_name_input
			user.last_name = last_name_input
			user.email = email_input
			user.password = password_input
			user.save()

			user_role = User_Role()
			user_role.user_x = user

			role_of_user = Role.objects.get(role_name = 'User')
			user_role.role_x = role_of_user
			user_role.save()

			user = authenticate(request, email=email_input, password = password_input)
			# return HttpResponse (user)
			# login_user(request, user)

			#return HttpResponseRedirect('/dashboard')
			return redirect('/dashboard')

		else:
			return redirect('/register')



		# user = User()
		# user.first_name = first_name_input
		# user.last_name = last_name_input
		# user.email = email_input
		# user.password = password_input
		# user.save()

		# return redirect('../login_user')

		# return HttpResponse (password_input)


#Check if session is set
def check_session(request, url_to_redirect_to):
	if 'email' in request.session: #Session is set
		# return redirect (url_to_redirect_to)
		return 'session_true'

	else:
		return 'session_false'
		# return redirect ('../')

def logout(request):
	del request.session['email']

	return redirect("/")


#Admin Functionalities
#1. Create and delete user accounts
#2. 


def disable_user (request, user_id):
	user_to_disable = User.objects.get(id=user_id)
	found_status = user_to_disable.status

	if (found_status == 1):
		user_to_disable.status = 0

	if (found_status == 0):
		user_to_disable.status = 1

	user_to_disable.save()

	return redirect ('/dashboard')


def delete_user (request, user_id):
	user_to_delete = User.objects.get(id=user_id)

	#Re-Active account
	if (user_to_delete.status == 2):
		user_to_delete.status = 1
	
	else:
		#status 2 means account has been deleted
		user_to_delete.status = 2

	user_to_delete.save()

	return redirect ('/dashboard')


# Project Management
def view_projects(request):
	roles_permissions = request.session['roles_n_permissions']
	current_user = request.session['user_id']
	user_names = request.session['user_names']

	if ('Administrator' in roles_permissions[0]):
		# return HttpResponse ('admin')

		get_all_projects = Project.objects.all().order_by('-project_DOR')

		    # Paginate the data
		# paginator = Paginator(get_all_projects, 5)  # Change 10 to the desired number of items per page
		# page_number = request.GET.get('page')
		# page_obj = paginator.get_page(page_number)

		# get_all_projects = page_obj


		for obj in get_all_projects:
			column_value = obj.project_skills
			if column_value:
				list_value = literal_eval(column_value)
				obj.project_skills = list_value
				obj.save()


		active_all_projects = Project.objects.filter(status = 1).order_by('-project_DOR')

		# get_all_projects = Project.objects.all().order_by('-project_DOR')
		# return HttpResponse (project_added_status)

		#all registered projects
		all_projects_count = Project.objects.all().order_by('-project_DOR').count()


		#Count how many projects are active
		active_project_count = Project.objects.filter(status = 1).count()

		#Count how many projects have been deleted
		deleted_project_count = Project.objects.filter(status = 2).count()

		#Count how many projects have been completed
		completed_project_count = Project.objects.filter(status = 3).count()

		return render (request, "project_page.html", {'all_projects': get_all_projects,
			'active_projects' : active_all_projects, 'roles_n_permissions': roles_permissions,
			'projects_summary': [all_projects_count, active_project_count, deleted_project_count, completed_project_count],
			'user_names': user_names})


	if ('User' in roles_permissions[0]):
		user_x = User.objects.get (id = current_user)
		get_all_projects = Project.objects.filter(user_project = user_x).order_by('-project_DOR')

		active_all_projects = Project.objects.filter(status = 1, user_project = user_x).order_by('-project_DOR')


		for obj in get_all_projects:
			column_value = obj.project_skills
			if column_value:
				list_value = literal_eval(column_value)
				obj.project_skills = list_value
				obj.save()


		# get_all_projects = Project.objects.all().order_by('-project_DOR')
		# return HttpResponse (project_added_status)

		#all registered projects
		all_projects_count = Project.objects.filter(user_project = user_x).order_by('-project_DOR').count()


		#Count how many projects are active
		active_project_count = Project.objects.filter(status = 1, user_project = user_x).count()

		#Count how many projects have been deleted
		deleted_project_count = Project.objects.filter(status = 2, user_project = user_x).count()

		#Count how many projects have been completed
		completed_project_count = Project.objects.filter(status = 3, user_project = user_x).count()

		return render (request, "project_page.html", {'all_projects': get_all_projects, 
			'active_projects' : active_all_projects,
			'projects_summary': [all_projects_count, active_project_count, deleted_project_count, completed_project_count], 
			'user_names':user_names, 'current_user': current_user})



import re
import os
from shutil import copyfileobj
from django.conf import settings

def add_project(request):
	# skills = request.POST['skills_required']
	# skills_list = skills.split(", ")

	# return HttpResponse (skills_list[2])
	uploaded_image1 = None
	uploaded_image2 = None
	uploaded_image3 = None

	if request.method == "POST":
		current_user = request.session['user_id']

		# if 'image1' in request.FILES or 'image2' in request.FILES or 'image3' in request.FILES:
		project_images = ['x.pdf', 'x.pdf', 'x.pdf']
		if 'image1' in request.FILES:
			image1 = request.FILES['image1'].name
			uploaded_image1 = request.FILES.get('image1')
			project_images[0] = image1
			# project_images.append(image1)
			
		if 'image2' in request.FILES:
			image2 = request.FILES['image2'].name
			uploaded_image2 = request.FILES.get('image2')
			project_images[1] = image2
			# project_images.append(image2)

		if 'image3' in request.FILES:
			image3 = request.FILES['image3'].name
			uploaded_image3 = request.FILES.get('image3')
			project_images[2] = image3
			# project_images.append(image3)



		project_files = ['x.jpg', 'x.jpg', 'x.jpg']
		if 'file1' in request.FILES:
			file1 = request.FILES['file1'].name
			uploaded_file1 = request.FILES.get('file1')
			project_files[0] = file1
			# project_files.append(file1)
			
		if 'file2' in request.FILES:
			file2 = request.FILES['file2'].name
			uploaded_file2 = request.FILES.get('file2')
			project_files[1] = file2
			# project_images.append(file2)

		if 'file3' in request.FILES:
			file3 = request.FILES['file3'].name
			uploaded_file3 = request.FILES.get('file3')
			project_files[2] = file3
			# project_files.append(file3)
		
        
		# Construct the path to the new image file
		# new_file_path = 'C:\\Users\\Nassor\\Desktop\\Project II implementation\\PLCS\\PLCS_system\\static\\project_imgs' + image1
		# Get the destination path and filename for the copied image
		# destination_path = 'C:\\Users\\Nassor\\Desktop\\Project II implementation\\PLCS\\PLCS_system\\static\\project_imgs'

		project_title = request.POST["project_title"]
		project_description = request.POST["project_description"]

		num_collaborators = request.POST["num_collaborators"]
		project_budget = request.POST["project_budget"]
		project_budget = re.sub(r'[^a-zA-Z0-9\s]+', '', project_budget) #Get non alpha-numeric

		project_deadline = request.POST["project_deadline"]


		last_project = Project.objects.all().order_by('-project_DOR')

		if (last_project.exists()):
			num = last_project[0].id + 1
			num = str(num)

		else:
			num = "1"

		project = Project()
		project.project_id = 'PLCS' + num


		#COPY THE IMAGE TO THE PROJECT DIRECTORY 'static/project_imgs'
		for index, i in enumerate(project_images):
			destination_path = settings.STATIC_ROOT

			# Construct the full destination path
			destination_fullpath = os.path.join(destination_path, i)

			pj = ['x', 'x', 'x']

			# Copy the uploaded image to the destination directory
			with open(destination_fullpath, 'wb') as destination_file:
				
				if ((index == 0) and project_images[0] != 'x.pdf'):
					source_file = uploaded_image1.file
					pj[0] = 'y'

				if ((index == 1) and (project_images[1] != 'x.pdf')):
					source_file = uploaded_image2.file
					pj[1] = 'y'

				if ((index == 2) and (project_images[2] != 'x.pdf')):
					source_file = uploaded_image3.file
					pj[2] = 'y'

				copyfileobj(source_file, destination_file)
				destination_file.close()

			img_extension = os.path.splitext(i)[1]

			# Rename the file
			img_count = index+1
			new_name = 'PLCS' + num + "#img" + str(img_count) + img_extension

			project_images[index] = new_name
			
			# Construct the full path to the file
			full_path = os.path.join(destination_path, i)

			# Rename the file
			os.rename(full_path, os.path.join(destination_path, new_name))




		#COPY THE FILE TO THE PROJECT DIRECTORY 'static/project_files'
		for index, i in enumerate(project_files):
			destination_path = settings.STATIC_ROOT2

			# Construct the full destination path
			destination_fullpath = os.path.join(destination_path, i)

			# Copy the uploaded image to the destination directory
			with open(destination_fullpath, 'wb') as destination_file:
				
				if ((index == 0) and (project_files[0] != 'x.jpg')):
					source_file = uploaded_file1.file

				if ((index == 1) and (project_files[1] != 'x.jpg')):
					source_file = uploaded_file2.file

				if ((index == 2) and (project_files[2] != 'x.jpg')):
					source_file = uploaded_file3.file

				copyfileobj(source_file, destination_file)
				destination_file.close()

			file_extension = os.path.splitext(i)[1]

			# Rename the file
			file_count = index+1
			new_name = 'PLCS' + num + "#file" + str(file_count) + file_extension

			project_files[index] = new_name
			
			# Construct the full path to the file
			full_path = os.path.join(destination_path, i)

			# Rename the file
			os.rename(full_path, os.path.join(destination_path, new_name))



		project.project_title = project_title
		project.project_description = project_description
		project.project_DOR = datetime.today()

		project.project_images = project_images
		project.project_files = project_files

		project.status = 1

		project.project_budget = project_budget
		project.project_collaborators = num_collaborators

		skills = request.POST['skills_required']
		skills_list = skills.split(", ")

		project.project_skills = str(skills_list)

		input_format = '%d-%m-%Y'
		output_format = '%Y-%m-%d %H:%M:%S'

		# Parse the input date string to a datetime object
		input_date = datetime.strptime(project_deadline, input_format)

		# Convert the datetime object to a string in the desired format
		project_deadline = input_date.strftime(output_format)

		project.project_deadline = project_deadline
		project.user_project = User.objects.get(id = current_user)

		project.save()
		messages.success(request, 'Contact request submitted successfully.')

		project_added_success_msg = "Project has been added"

		return redirect ('/view_projects', project_added_msg = project_added_success_msg)




def delete_project(request, project_id_delete):
	project_to_delete = Project.objects.get(id = project_id_delete)

	#status 2 means project has been deleted
	if (project_to_delete.status == 2):
		project_to_delete.delete()

	else:
		project_to_delete.status = 2
		project_to_delete.save()

	return redirect ('/view_projects')


def view_profile(request):
	roles_n_permissions = request.session['roles_n_permissions']
	user_names = request.session['user_names']
	return render (request, "profile.html", {'user_names': user_names, 'roles_n_permissions': roles_n_permissions})


def view_messages(request):
	return render (request, "messages_chats.html")


def nm_user(request):
	return render (request, "user_projects.html")


def roles_permissions(request):
	roles_n_permissions = request.session['roles_n_permissions']

	all_roles = Role.objects.all()
	user_permissions = Permission.objects.all()


	logged_in_userid = request.session['user_id']
	user_names = request.session['user_names']

	roles_n_permissions = get_roles_permissions(request, logged_in_userid)


	#Get all roles of each user
	permissions_for_each_role = []

	for i in all_roles:
		permissions_of_this_role = Role_Permission.objects.filter(role = i)

		permission_for_role_i = []
		#Loop through each role found
		for j in permissions_of_this_role:
			permission_for_role_i.append(j.permission.permission_action)

		permissions_for_each_role.append(permission_for_role_i)

	# return HttpResponse (permissions_for_each_role)

	return render (request, "roles_permissions.html", {'all_roles': all_roles, 'permissions_for_each_role': permissions_for_each_role,
		'user_permissions': user_permissions, 'roles_n_permissions': roles_n_permissions, 'user_names': user_names})


def add_role(request):
	if request.method == "POST":

		role_name_input = request.POST["role_name_input"]
		role_description_input = request.POST["role_description_input"]

		#If Role does not exist
		if not (Role.objects.filter(role_name = role_name_input).exists()):
			new_role = Role()
			new_role.role_name = role_name_input
			new_role.role_description = role_description_input
			new_role.save()

		return redirect ('/roles_permissions')


def user_management(request):
	current_user = request.session['user_id']
	user_x = User.objects.get (id = current_user)
	get_all_projects = Project.objects.all().order_by('-project_DOR')
	user_names = request.session['user_names']


	get_all_project_collabs = User_Project_Collab.objects.filter(user = user_x)


	user_x_collab = []
	for collab in get_all_project_collabs:
		user_x_collab.append(collab.project.id)


	for obj in get_all_projects:
		column_value = obj.project_skills
		if column_value:
			list_value = literal_eval(column_value)
			obj.project_skills = list_value
			obj.save()


	roles_n_permissions = request.session['roles_n_permissions']

	session_val = check_session(request, 'url_to_redirect_to')

	get_all_users = User.objects.all().order_by('-date_of_registration')

	#Count all user accounts
	all_user_accounts_count = User.objects.all().count()

	#Count how many Users are active
	active_user_count = User.objects.filter(status = 1).count()

	#Count how many Users have been deleted
	deleted_user_count = User.objects.filter(status = 2).count()

	#Count how many Users have been Disabled
	disabled_user_count = User.objects.filter(status = 0).count()

	#Get permissions in database
	user_permissions = Permission.objects.all()

	#Get roles in database
	user_roles = Role.objects.all()


	#Get all roles of each user
	roles_for_each_user = []

	for i in get_all_users:
		roles_of_this_user = User_Role.objects.filter(user_x = i)

		roles_for_user_i = []
		#Loop through each role found
		for j in roles_of_this_user:
			roles_for_user_i.append(j.role_x.role_name)

		roles_for_each_user.append(roles_for_user_i)


	if (session_val == 'session_true'):
		return render (request, "user_management.html", {'all_users': get_all_users, 
			'user_summary': [all_user_accounts_count, active_user_count, disabled_user_count, deleted_user_count],
			'user_permissions': user_permissions, 'user_roles': user_roles, 'roles_for_each_user': roles_for_each_user,
			'roles_n_permissions': roles_n_permissions, 'get_all_projects': get_all_projects, 'user_names': user_names, 
			'current_user': current_user, 'get_all_project_collabs': user_x_collab})
		# return render (request, "dashboard.html")

	else:
		return redirect ('/')
	# return render (request, "user_management.html")



def update_user(request, user_id):
	if request.method == "POST":
		user_to_update = User.objects.get(id = user_id)

		first_name_input = request.POST["first_name"]
		last_name_input = request.POST["last_name"]
		email_input = request.POST["email"]
		password_input = request.POST["password"]
		# confirm_password_input = request.POST["confirm_password"]

		user_to_update.first_name = first_name_input
		user_to_update.last_name = last_name_input
		user_to_update.email = email_input
		user_to_update.password = password_input
		user_to_update.save()

		return redirect('/dashboard')


# from django.contrib import messages
# from django.shortcuts import render, redirect

# def my_view(request):
# 	messages.add_message(request, messages.INFO, "Hello world.")

# 	return render(request, 'my_template.html')

def delete_role(request, role_id):
	role_to_delete = Role.objects.get(id = role_id)
	
	# Delete the item
	role_to_delete.delete()
	return redirect ('/roles_permissions')



def edit_permissions_for_role(request, role_id):
	if request.method == 'POST':

		#We have the role id
		role_selected = Role.objects.get(id = role_id)

		all_permissions = Permission.objects.all()

		for i in all_permissions:
			checkbox_status = request.POST.get(i.permission_action, None)

			#Checkbox has been selected
			if (checkbox_status == 'on'):
				role_perm = Permission.objects.get (permission_action = i.permission_action)
				# role_perm_del = Role_Permission.objects.get(permission = role_perm, role = role_selected)


				#If already exists
				if not (Role_Permission.objects.filter(permission = role_perm, role = role_selected).exists()):
					role_perm = Role_Permission()
					role_perm.role = role_selected
					role_perm.permission = Permission.objects.get (permission_action = i.permission_action)
					role_perm.save()

			#Checkbox has not been selected
			else:
				role_perm = Permission.objects.get (permission_action = i.permission_action)

				#If exists
				if (Role_Permission.objects.filter(permission = role_perm, role = role_selected).exists()):
					role_perm_del = Role_Permission.objects.get(permission = role_perm, role = role_selected)
					role_perm_del.delete()


		return redirect ('/roles_permissions')
				# if not (Role_Permission.objects.get(role_name = role_name_input).exists()):



	# if request.method == 'POST':
	# 	data = request.POST

	# 	my_checkbox_status = request.POST.get('manage users', None)
	# 	my_checkbox_status2 = request.POST.get('manage projects', None)

	# 	return HttpResponse (f"manage users = {my_checkbox_status} and manage projects = {my_checkbox_status2}")

		# else:
		# 	return HttpResponse (my_checkbox_status)

		# return HttpResponse(data)

def admin_add_user(request):
	if request.method == "POST":

		first_name_input = request.POST["first_name"]
		last_name_input = request.POST["last_name"]
		email_input = request.POST["email"]
		password_input = request.POST["password"]
		# confirm_password_input = request.POST["confirm_password"]

		# checkbox_status = request.POST.get('manage users', None)


		#If email does not exist/ User is not registered yet
		if not (User.objects.filter(email=email_input).exists()):
			user = User()
			user.first_name = first_name_input
			user.last_name = last_name_input
			user.email = email_input
			user.password = password_input
			user.save()


			# user = authenticate(request, email=email_input, password = password_input)

			all_permissions = Permission.objects.all()

			all_roles = Role.objects.all()

			for i in all_permissions:
				checkbox_status = request.POST.get(i.permission_action, None)

				#Checkbox has been selected
				if (checkbox_status == 'on'):
					user_perm = Permission.objects.get (permission_action = i.permission_action)
					
					user_permission_add = User_Permission()
					user_permission_add.user_p = user
					user_permission_add.permission = user_perm
					user_permission_add.save()


			for i in all_roles:
				checkbox_status = request.POST.get(i.role_name, None)

				#Checkbox has been selected
				if (checkbox_status == 'on'):
					user_role_selected = Role.objects.get (role_name = i.role_name)

					user_role = User_Role()
					user_role.user_x = user
					user_role.role_x = user_role_selected
					user_role.save()
					# role_perm_del = Role_Permission.objects.get(permission = role_perm, role = role_selected)

			# return HttpResponse (user)
			# login_user(request, user)

			return HttpResponseRedirect('/dashboard')  

		else:
			return redirect('/user_management')




def get_roles_permissions(request, user_id):
	user_to_get_permissions = User.objects.get (id = user_id)
	user_to_get_roles = User_Role.objects.filter(user_x = user_to_get_permissions)

	user_permissions = User_Permission.objects.filter(user_p = user_to_get_permissions)

	roles_n_permissions = []

	permissions_of_user = []
	for i in user_permissions:
		permissions_of_user.append(i.permission.permission_action)

	roles_of_user = []
	for i in user_to_get_roles:
		roles_of_user.append(i.role_x.role_name)

	roles_n_permissions.append(roles_of_user)
	roles_n_permissions.append(permissions_of_user)

	return roles_n_permissions



# def get_permissions(request, user_id):
# 	user_to_get_permissions = User.objects.get (id = user_id)

def learning_content(request):
	all_modules = Learning_Module.objects.all().order_by('-module_DOR')
	all_modules_count = Learning_Module.objects.all().count()

	for obj in all_modules:
		column_value = obj.module_tags
		if column_value:
			list_value = literal_eval(column_value)
			obj.module_tags = list_value
			obj.save()


	logged_in_userid = request.session['user_id']
	user_names = request.session['user_names']

	roles_n_permissions = get_roles_permissions(request, logged_in_userid)
	return render (request, "learning_module_management.html", {'roles_n_permissions': roles_n_permissions, 'user_names': user_names,
		'all_modules': all_modules, 'all_modules_count': all_modules_count})



def add_module(request):
	if request.method == "POST":

		module_title = request.POST["module_title"]
		module_description = request.POST["module_description"]
		module_tags = request.POST['module_tags']

		check_modules = Learning_Module.objects.filter(module_title = module_title)
		if (check_modules.exists()):
			return redirect('/learning_content')

		else:
			logged_in_userid = request.session['user_id']
			get_user = User.objects.get(id = logged_in_userid)

			new_module = Learning_Module()
			new_module.module_title = module_title
			new_module.module_description = module_description
			new_module.module_creator = get_user

			tags_list = module_tags.split(", ")
			new_module.module_tags = str(tags_list)

			new_module.save()
			return redirect('/learning_content')


def delete_module (request, module_id):
	module_to_delete = Learning_Module.objects.get(id = module_id)
	module_to_delete.delete()

	return redirect ('/learning_content')



def edit_module (request, module_id):
	module_to_edit = Learning_Module.objects.get(id = module_id)

	if request.method == "POST":
		module_title = request.POST["module_title"]
		module_description = request.POST["module_description"]

		try:
			module_to_edit_title = Learning_Module.objects.get(module_title = module_title)

		except:
			module_to_edit.module_title = module_title
			module_to_edit.module_description = module_description
			module_to_edit.save()

	return redirect ('/learning_content')



def view_module (request, module_id):
	# module_to_edit = Learning_Module.objects.get(id = module_id)

	# if request.method == "POST":
	# 	module_title = request.POST["module_title"]
	# 	module_description = request.POST["module_description"]

	# 	try:
	# 		module_to_edit_title = Learning_Module.objects.get(module_title = module_title)

	# 	except:
	# 		module_to_edit.module_title = module_title
	# 		module_to_edit.module_description = module_description
	# 		module_to_edit.save()

	return render (request, 'learning_content_management.html')


from django.http import JsonResponse

def like_project(request):
	if request.method == 'POST':
		# Retrieve the data from the request
		project_id = request.POST.get('projectId')
		is_liked = request.POST.get('isLiked')

		project_liked = Notification()
		project_liked.notification_title = 'testing AJAX'
		project_liked.notification_content = 'testing AJAX'
		project_liked.notification_status = '1'
		project_liked.notification_link_to = 'testing AJAX'
		project_liked.notification_date = datetime.today()


		user_x = User.objects.all()

		project_liked.notification_recipient = user_x[0]
		project_liked.save()

		# Perform the necessary actions based on the data
		# Update the like status of the project with the given project_id

		# Return a JSON response indicating the success or failure of the request
		response_data = {'status': 'success'}
		return JsonResponse(response_data)

	else:
		# Handle invalid or non-AJAX requests
		response_data = {'status': 'failure'}
		return JsonResponse(response_data, status=400)


def project_details(request, project_id):
	get_project_details = Project.objects.get (id = project_id)

	# for obj in get_project_details:
	column_value = get_project_details.project_skills
	if column_value:
		list_value = literal_eval(column_value)
		get_project_details.project_skills = list_value
		get_project_details.save()


	return render(request, "project_details.html", {'get_project_details': get_project_details})


# def user_project_likes (request, user_id, project_id):
# 	User_Project_Like


def apply_to_project(request, project_id):
	if request.method == 'POST':
		current_user = request.session['user_id']

		#Get user
		user_apply = User.objects.get (id = current_user)

		#Get project
		project_apply = Project.objects.get (id = project_id)


		#Check for the user's id and project id exist
		check_project_collabs = User_Project_Collab.objects.filter(user = user_apply).filter (project = project_apply)

		#If exists, remove it
		if (check_project_collabs.exists()):
			check_project_collab = User_Project_Collab.objects.filter(user = user_apply).get(project = project_apply)
			check_project_collab.delete()


		else:
			user_project_collab = User_Project_Collab()
			user_project_collab.user = user_apply
			user_project_collab.project = project_apply

			#0 = pending approval, 1 = approved, collaborating
			user_project_collab.status = 0
			user_project_collab.save()

		return redirect('/dashboard')



def view_projects_collaborations(request):
	current_user = request.session['user_id']

	project_collab_status = [0, 0, 0]

	#Get user
	user_collabs = User.objects.get (id = current_user)

	user_project_collabs = User_Project_Collab.objects.filter(user = user_collabs)

	for obj in user_project_collabs:
		column_value = obj.project.project_skills
		if column_value:
			list_value = literal_eval(column_value)
			obj.project.project_skills = list_value
			obj.save()


	#Get Pending collabs
	get_pending_project_collabs = User_Project_Collab.objects.filter(user = user_collabs).filter (status = 0)
	get_pending_project_collab_count = get_pending_project_collabs.count()


	#Get Active collabs
	get_active_project_collabs = User_Project_Collab.objects.filter(user = user_collabs).filter (status = 1)
	get_active_project_collab_count = get_active_project_collabs.count()


	project_collab_status[0] = get_pending_project_collab_count
	project_collab_status[1] = get_active_project_collab_count


	return render (request, "project_collab_page.html", {'user_project_collabs': user_project_collabs, 'project_collab_status': project_collab_status})