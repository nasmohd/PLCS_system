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
from django.db.models import Q
from django.db.models import F
from django.db.models import Count

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
				if (check_DB_user_details[0].status != 0):
					if (check_DB_user_details[0].password == password_input):

						#Create Session for User
						request.session['email'] = check_DB_user_details[0].email
						request.session['roles_n_permissions'] = get_roles_permissions(request, check_DB_user_details[0].id)
						request.session['user_id'] = check_DB_user_details[0].id
						request.session['user_names'] = [check_DB_user_details[0].first_name, check_DB_user_details[0].last_name]

						return redirect('/dashboard') 
						# return HttpResponse (check_DB_user_details[0].password)

					else:
						messages.success(request, 'Wrong credentials', extra_tags='alert-danger')
						return redirect('/')

				else:
					messages.success(request, 'Account disabled, contact Admin', extra_tags='alert-danger')
					return redirect('/')

			else:
				messages.success(request, 'This user does not exist', extra_tags='alert-danger')
				return redirect('/') 

		messages.success(request, 'You need to log in', extra_tags='alert-danger')
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

		project_interests = request.POST['project_interests']
		learning_interests = request.POST['learning_interests']

		# skills = request.POST['skills_required']
		project_interests_list = project_interests.split(", ")
		learning_interests_list = learning_interests.split(", ")

		# project.project_skills = str(project_interests_list)


		#If email does not exist/ User is not registered yet
		if not (User.objects.filter(email=email_input).exists()):
			if (password_input == confirm_password_input):
				user = User()
				user.first_name = first_name_input
				user.last_name = last_name_input
				user.email = email_input
				user.password = password_input
				user.learning_interests = str(learning_interests_list)
				user.project_interests = str(project_interests_list)

				user.save()

				user_role = User_Role()
				user_role.user_x = user

				#When user registers, directly given role 'User'
				role_of_user = Role.objects.get(role_name = 'User')
				user_role.role_x = role_of_user
				user_role.save()

				user = authenticate(request, email=email_input, password = password_input)
				# return HttpResponse (user)
				# login_user(request, user)

				# return HttpResponse (user.id)
				# request.session['user_id'] = user.id

				#return HttpResponseRedirect('/dashboard')
				return redirect('/login_user')

			else:
				messages.success(request, 'Confirm password does not match with password entereed', extra_tags='alert-danger')
				return redirect('/register')

		else:
			messages.success(request, 'User already registered', extra_tags='alert-danger')
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

	notifs = get_notifications_of_user (request, current_user)
	# projects = Project.objects.annotate(request_counts=Count('user_project_collab', filter=models.Q(user_project_collab__status=0)))

	# return HttpResponse (projects)

	if ('Administrator' in roles_permissions[0]):
		# return HttpResponse ('admin')

		# get_all_projects = Project.objects.all().order_by('-project_DOR')
		get_all_projects = Project.objects.annotate(request_counts=Count('user_project_collab', filter=models.Q(user_project_collab__status=0))).order_by('-project_DOR')

		    # Paginate the data
		# paginator = Paginator(get_all_projects, 5)  # Change 10 to the desired number of items per page
		# page_number = request.GET.get('page')
		# page_obj = paginator.get_page(page_number)

		# get_all_projects = page_obj


		for obj in get_all_projects:
			column_value = obj.project_skills
			column_value2 = obj.project_images

			if column_value:
				list_value = literal_eval(column_value)
				obj.project_skills = list_value
				obj.save()

			if column_value2:
				list_value2 = literal_eval(column_value2)
				obj.project_images = list_value2
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
			'user_names': user_names, 'notifs': notifs})


	if ('User' in roles_permissions[0]):
		user_x = User.objects.get (id = current_user)

		get_all_projects = Project.objects.filter(user_project = user_x).annotate(request_counts=Count('user_project_collab', filter=models.Q(user_project_collab__status=0))).order_by('-project_DOR')

		# get_all_projects = Project.objects.filter(user_project = user_x).order_by('-project_DOR')

		active_all_projects = Project.objects.filter(status = 1, user_project = user_x).order_by('-project_DOR')


		for obj in get_all_projects:
			column_value = obj.project_skills
			column_value2 = obj.project_images

			if column_value:
				list_value = literal_eval(column_value)
				obj.project_skills = list_value
				obj.save()

			if column_value2:
				list_value2 = literal_eval(column_value2)
				obj.project_images = list_value2
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
			'user_names':user_names, 'current_user': current_user, 'notifs': notifs})



import re
import os
from shutil import copyfileobj
from django.conf import settings
import json

def add_project(request):
	# skills = request.POST['skills_required']
	# skills_list = skills.split(", ")

	# return HttpResponse (skills_list[2])
	uploaded_image1 = None
	uploaded_image2 = None
	uploaded_image3 = None

	# if request.method == 'POST':
	# 	todo_items = request.POST.get('todo_items')
	# 	if todo_items:
	# 		# Deserialize the JSON string into a Python list
	# 		todo_items = json.loads(todo_items)

	# 		# Process the todo_items as needed
	# 		for item in todo_items:
	# 			print (item)
	# 			# Perform your desired operations on each item
	# 			# For example, you can save each item to the database
	# 	return HttpResponse('ym')


	if request.method == "POST":
		current_user = request.session['user_id']


		# if 'image1' in request.FILES or 'image2' in request.FILES or 'image3' in request.FILES:
		project_images = ['x.pdf', 'x.pdf', 'x.pdf']
		# project_images = []
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

		#If image has been selected by the user, it is placed in the list "project_images" based on index


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


		#Take the submitted data about projec title, description, collaborators, budget etc.
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

		img_present = ['n', 'n', 'n']


		#COPY THE IMAGE TO THE PROJECT DIRECTORY 'static/project_imgs'
		for index, i in enumerate(project_images):
			destination_path = settings.STATIC_ROOT

			# Construct the full destination path
			destination_fullpath = os.path.join(destination_path, i)

			# pj = ['x', 'x', 'x']

			# Copy the uploaded image to the destination directory
			with open(destination_fullpath, 'wb') as destination_file:
				#For the first index, check at first index of project_images list if submitted
				if ((index == 0) and project_images[0] != 'x.pdf'):
					source_file = uploaded_image1.file
					# img_present[0] = ['y']
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
					# pj[0] = 'y'


				if ((index == 1) and (project_images[1] != 'x.pdf')):
					source_file = uploaded_image2.file
					# img_present[1] = ['y']
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
					# pj[1] = 'y'

				if ((index == 2) and (project_images[2] != 'x.pdf')):
					source_file = uploaded_image3.file
					# img_present[2] = ['y']
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
					# pj[2] = 'y'

		# return HttpResponse ('success')				




		#COPY THE FILE TO THE PROJECT DIRECTORY 'static/project_files'
		for index, i in enumerate(project_files): #index 0, 1, 2, i iterates each element in the list
			destination_path = settings.STATIC_ROOT2

			# Construct the full destination path
			destination_fullpath = os.path.join(destination_path, i)

			# Copy the uploaded image to the destination directory
			with open(destination_fullpath, 'wb') as destination_file:
				
				if ((index == 0) and (project_files[0] != 'x.jpg')):
					source_file = uploaded_file1.file

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

				if ((index == 1) and (project_files[1] != 'x.jpg')):
					source_file = uploaded_file2.file

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

		# project_images = ['x','y','z']
		# project_files = ['x','y','z']

		project.project_images = project_images
		project.project_files = project_files

		project.status = 1

		project.project_budget = project_budget
		project.project_collaborators = num_collaborators

		skills = request.POST['skills_required']
		skills_list = skills.split(", ")

		project.project_skills = str(skills_list)

		input_format = '%d-%m-%Y'
		output_format = '%Y-%m-%d'

		# Parse the input date string to a datetime object
		input_date = datetime.strptime(project_deadline, input_format)

		# Convert the datetime object to a string in the desired format
		project_deadline = input_date.strftime(output_format)

		project.project_deadline = project_deadline
		project.user_project = User.objects.get(id = current_user)

		task_deadlines = request.POST.getlist('task_deadline[]')
		task_details = request.POST.getlist('task_details[]')
		sub_tasks = []

		new_tasks = Collab_Task()

		for i in range(len(task_details)):
			sub_task_key = f'sub_tasks[{i}][]'
			sub_task_values = request.POST.getlist(sub_task_key)

			# Convert the date string to a datetime object
			task_deadline_str = datetime.strptime(task_deadlines[i], '%Y-%m-%d')

			# Format the date as 'DD-MM-YYYY'
			formatted_deadline_date = task_deadline_str.strftime('%d-%m-%Y')


			task_data = [formatted_deadline_date, task_details[i], sub_task_values]

			#Code to add each task based on user input
			# new_tasks = Collab_Task()
			new_tasks.task_x = task_details[i]
			
			new_tasks.task_deadline = task_deadline_str
			new_tasks.task_deliverables = sub_task_values
			


			sub_tasks.append(task_data)

			#For each task, add it into Collab_tasks table

		project.project_tasks = sub_tasks
		project.save()
		new_tasks.project = project
		new_tasks.save()

		# todo_items = request.POST.get('todo_items')
		# if todo_items:
		# 	# Deserialize the JSON string into a Python list
		# 	todo_items = json.loads(todo_items)

		# 	# Process the todo_items as needed
		# 	for item in todo_items:
		# 		new_task = Collab_Task()
		# 		new_task.project = project
		# 		new_task.task_x = item
		# 		new_task.task_status = 0
		# 		new_task.op_status = 0
		# 		new_task.save()


		messages.success(request, 'Project added successfully.', extra_tags='alert-success')

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
	current_user = request.session['user_id']

	user_x_details = User.objects.get(id = current_user)
	user_x_details_list = literal_eval(user_x_details.project_interests)
	user_x_details.project_interests = user_x_details_list

	user_x_details_list = literal_eval(user_x_details.learning_interests)
	user_x_details.learning_interests = user_x_details_list

	user_x_details.save()

	count_completed_projects = Project.objects.filter(user_project = user_x_details).filter(status = 3).count()
	count_active_projects = Project.objects.filter(user_project = user_x_details).filter(status = 1).count()
	all_projects_of_user = Project.objects.filter(user_project = user_x_details)

	user_project_details = [count_completed_projects, count_active_projects]



	roles_n_permissions = request.session['roles_n_permissions']
	user_names = request.session['user_names']
	return render (request, "profile.html", {'user_names': user_names, 'roles_n_permissions': roles_n_permissions, 'user_x_details': user_x_details,
		'user_project_details': user_project_details})


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
		# if not (Role.objects.filter(role_name = role_name_input).exists()):
		if not (Role.objects.filter(Q(role_name__icontains=role_name_input)).exists()):
			new_role = Role()
			new_role.role_name = role_name_input
			new_role.role_description = role_description_input
			new_role.save()
			messages.success(request, 'Role has been added', extra_tags='alert-success')

		else:
			messages.success(request, 'Role already exists', extra_tags='alert-danger')

		return redirect ('/roles_permissions')


def user_management(request):
	current_user = request.session['user_id']
	user_x = User.objects.get (id = current_user)
	get_all_projects = Project.objects.all().order_by('-project_DOR')
	user_names = request.session['user_names']


	#Recommnend Projects
	rec_proj = recommend_projects(current_user)
	rec_proj = rec_proj[0]
	# print (rec_proj[0])

	# Get recommended projects from the database based on the project IDs
	rec_projects_details = Project.objects.filter(project_id__in = rec_proj)


	get_all_project_collabs = User_Project_Collab.objects.filter(user = user_x)


	user_x_collab = []
	for collab in get_all_project_collabs:
		user_x_collab.append(collab.project.id)


	for obj in get_all_projects:
		column_value = obj.project_skills
		column_value2 = obj.project_images

		if column_value:
			list_value = literal_eval(column_value)
			obj.project_skills = list_value
			obj.save()

		if column_value2:
			list_value2 = literal_eval(column_value2)
			obj.project_images = list_value2
			obj.save()


	roles_n_permissions = request.session['roles_n_permissions']

	session_val = check_session(request, 'url_to_redirect_to')

	get_all_users = User.objects.all().order_by('-date_of_registration').exclude(id = current_user)

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

	all_roles = []


	notifs = get_notifications_of_user (request, current_user)


	#Get permissions for Roles
	#user_roles = "id = 1, role = Userid = 2, role = Administrator"
	permissions_for_role = []
	permissions_each_role = []
	for r in user_roles:
		all_roles.append(r.role_name)
		permissions_for_role_queryset = Role_Permission.objects.filter(role = r)

		for role_perm in permissions_for_role_queryset:
			permissions_each_role.append (role_perm.permission.permission_action)

		#Role index 0, has permissions in list at index 0
		permissions_for_role.append(permissions_each_role)
		permissions_each_role = []

	#roles = ['User', 'Administrator'], 
	#permissions = [['track progress', 'comment on users'], 
	#['manage users', 'manage projects', 'manage learning content', 'manage comments', 'comment on projects', 'track progress', 'comment on users']]


	#Get all roles of each user
	roles_for_each_user = []
	permissions_for_each_user = []

	for i in get_all_users:
		roles_of_this_user = User_Role.objects.filter(user_x = i)

		permissions_for_this_user = User_Permission.objects.filter(user_p = i)

		permissions_for_user_i = []
		for k in permissions_for_this_user:
			permissions_for_user_i.append (k.permission.permission_action)
		permissions_for_each_user.append (permissions_for_user_i)

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
			'current_user': current_user, 'get_all_project_collabs': user_x_collab, 'all_roles': all_roles, 
			'permissions_for_role': permissions_for_role, 'notifs': notifs, 'rec_projects_details': rec_projects_details, 
			'permissions_for_each_user': permissions_for_each_user})
		# return render (request, "dashboard.html")

	else:
		return redirect ('/')
	# return render (request, "user_management.html")



def get_notifications_of_user (request, user_id):
	user_x = User.objects.get(id = user_id)

	#Get notifications for this user
	user_notifications = Notification.objects.filter(notification_recipient = user_x).order_by('-id')

	#Get new notification
	new_user_notifications = Notification.objects.filter(notification_recipient = user_x).filter (notification_status = 0).order_by('-id')
	new_user_notifications_count = new_user_notifications.count()

	notifs = [user_notifications, new_user_notifications, new_user_notifications_count]

	return notifs


def get_user_details (request, user_id):
	user_names = request.session['user_names']
	return user_names



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

		messages.success(request, 'User has been updated', extra_tags='alert-success')
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

	messages.success(request, 'Role has been deleted', extra_tags='alert-danger')
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

		"""
		csrfmiddlewaretoken	
			'Xq4J3wRMTTovpyBh5tNJLR0d18UBwMcWKGEzTT2LuwZA9s0X3dNwegMSd4oOj4Bv'
			first_name	
			'Jamesx232'
			last_name	
			'Bond'
			email	
			'Jamesx232@gmail.com'
			password	
			'Jamesx232'
			User	
			'User'
			manage users	
			'manage users'
			manage projects	
			'manage projects'
		"""


		#If email does not exist/ User is not registered yet
		if not (User.objects.filter(email=email_input).exists()):
			user = User()
			user.first_name = first_name_input
			user.last_name = last_name_input
			user.email = email_input
			user.password = password_input
			user.profile_img = 'Beginner'
			user.learning_interests = 'Beginner'
			user.project_interests = 'Beginner'
			user.user_activity_tags = 'Beginner'
			user.user_description = 'Beginner'

			user.save()


			# user = authenticate(request, email=email_input, password = password_input)

			all_permissions = Permission.objects.all()

			all_roles = Role.objects.all()

			for i in all_permissions:
				# checkbox_status = request.POST.get(i.permission_action, None)

				if i.permission_action in request.POST:

				#Checkbox has been selected
				# if (checkbox_status == 'on'):
					user_perm = Permission.objects.get (permission_action = i.permission_action)
					
					user_permission_add = User_Permission()
					user_permission_add.user_p = user
					user_permission_add.permission = user_perm
					user_permission_add.save()


			for i in all_roles:
				# checkbox_status = request.POST.get(i.role_name, None)

				#Checkbox has been selected
				if i.role_name in request.POST:
				# if (checkbox_status == 'on'):
					user_role_selected = Role.objects.get (role_name = i.role_name)

					user_role = User_Role()
					user_role.user_x = user
					user_role.role_x = user_role_selected
					user_role.save()
					# role_perm_del = Role_Permission.objects.get(permission = role_perm, role = role_selected)

			# return HttpResponse (user)
			# login_user(request, user)
			messages.success(request, 'User has been registered', extra_tags='alert-success')
			return HttpResponseRedirect('/dashboard')

		else:
			messages.success(request, 'User email already registered', extra_tags='alert-danger')
			return redirect('/user_management')




def get_roles_permissions(request, user_id):
	user_to_get_permissions = User.objects.get (id = user_id)
	user_to_get_roles = User_Role.objects.filter(user_x = user_to_get_permissions)

	user_permissions = User_Permission.objects.filter(user_p = user_to_get_permissions)

	roles_n_permissions = []

	#Getting specific permissions of user
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

def learning_content(request, topic_id):
	all_modules = Learning_Module.objects.all().order_by('-module_DOR')
	all_modules_count = Learning_Module.objects.all().count()

	get_all_summaries = Summary.objects.all()

	for obj in all_modules:
		column_value = obj.module_tags
		if column_value:
			list_value = literal_eval(column_value)
			obj.module_tags = list_value
			obj.save()


	logged_in_userid = request.session['user_id']
	user_names = request.session['user_names']

	roles_n_permissions = get_roles_permissions(request, logged_in_userid)
	return render (request, "learning_content_management.html", {'roles_n_permissions': roles_n_permissions, 'user_names': user_names,
		'all_modules': all_modules, 'all_modules_count': all_modules_count, 'topic_id': topic_id, 'get_all_summaries': get_all_summaries})



def learning_content_modules(request):
	current_user = request.session['user_id']
	me_user = User.objects.get(id = current_user)

	all_modules = Learning_Module.objects.filter(module_creator = me_user).order_by('-module_DOR')
	all_modules_count = all_modules.count()
	# current_user = request.session['user_id']




	#Recommnend Learning Materials
	# rec_proj = recommend_learning_material(current_user)
	# rec_proj = rec_proj[0]

	# rec_projects_details = []
	# for id in rec_proj:
	# 	project_detail = Learning_Module.objects.get(id=id)
	# 	rec_projects_details.append(project_detail)
	# print (rec_proj[0])





	# return HttpResponse (rec_proj)


	# Get recommended projects from the database based on the project IDs
	# rec_projects_details = Learning_Module.objects.filter(id__in = rec_proj)
	

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
# 'rec_projects_details': rec_projects_details


def learning_topic(request):
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
		current_user = request.session['user_id']
		me_user = User.objects.get(id = current_user)

		module_title = request.POST["module_title"]
		module_description = request.POST["module_description"]
		module_tags = request.POST['module_tags']

		check_modules = Learning_Module.objects.filter(module_title = module_title).filter(module_creator = me_user)
		if (check_modules.exists()):
			return redirect('/learning_content_modules')

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
			return redirect('/learning_content_modules')


def delete_module (request, module_id):
	module_to_delete = Learning_Module.objects.get(id = module_id)
	module_to_delete.delete()

	return redirect ('/learning_content_modules')



def edit_module (request, module_id):
	module_to_edit = Learning_Module.objects.get(id = module_id)


	if request.method == "POST":
		module_title = request.POST["module_title"]
		module_description = request.POST["module_description"]

		module_to_edit.module_title = module_title
		module_to_edit.module_description = module_description
		module_to_edit.save()



		# try:
		# 	module_to_edit_title = Learning_Module.objects.get(module_title = module_title)

		# except:
		# 	module_to_edit.module_title = module_title
		# 	module_to_edit.module_description = module_description
		# 	module_to_edit.save()

	return redirect ('/learning_content_modules')



def view_module (request, module_id):
	current_user = request.session['user_id']
	notifs = get_notifications_of_user (request, current_user)
	user_names = request.session['user_names']

	get_all_summaries = Summary.objects.all()

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

	return render (request, 'learning_topic_management.html', {'notifs': notifs, 'user_names': user_names, 'module_id': module_id,
		'get_all_summaries': get_all_summaries})


def view_topics (request, module_id):
	current_user = request.session['user_id']
	notifs = get_notifications_of_user (request, current_user)
	user_names = request.session['user_names']

	topics_for_modulex = Module_Topic.objects.filter(module_belongs_to__id = module_id)

	get_all_summaries = Summary.objects.all()

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

	return render (request, 'learning_topic_management.html', {'notifs': notifs, 'user_names': user_names, 'module_id': module_id,
		'topics_for_modulex': topics_for_modulex})



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

	#Get permissions in database
	user_permissions = Permission.objects.all()

	#Get roles in database
	user_roles = Role.objects.all()
	current_user = request.session['user_id']
	user_x = User.objects.get (id = current_user)

	#Recommnend Projects
	rec_proj = recommend_projects(current_user)
	rec_proj = rec_proj[0]
	# print (rec_proj[0])

	# Get recommended projects from the database based on the project IDs
	rec_projects_details = Project.objects.filter(project_id__in = rec_proj)


	# get_all_project_collabs = User_Project_Collab.objects.filter(user = user_x)


	roles_n_permissions = request.session['roles_n_permissions']
	user_names = request.session['user_names']


	# for obj in get_project_details:
	column_value = get_project_details.project_skills
	if column_value:
		list_value = literal_eval(column_value)
		get_project_details.project_skills = list_value
		get_project_details.save()


	column_value2 = get_project_details.project_images
	if column_value2:
		list_value2 = literal_eval(column_value2)

		get_project_details.project_images = list_value2
		get_project_details.save()


	column_value3 = get_project_details.project_files
	if column_value3:
		list_value3 = literal_eval(column_value3)
		get_project_details.project_files = list_value3
		get_project_details.save()

	# for index, im in enumerate(list_value2):
	# 	list_value2[index] = "/static/project_imgs/" + im
	# 	get_project_details.project_images = list_value2

	# return HttpResponse (get_project_details.project_images)
	# {% static '/project_imgs/PLCS44#img1.png' %}{% static '/project_imgs/x.pdf' %}{% static '/project_imgs/x.pdf' %}
	return render(request, "project_details.html", {'get_project_details': get_project_details, 
		'roles_n_permissions': roles_n_permissions, 'user_names': user_names, 'rec_projects_details': rec_projects_details,
		'current_user': current_user})


# def user_project_likes (request, user_id, project_id):
# 	User_Project_Like

def apply_to_project(request, project_id, project_poster_id):
	if request.method == 'POST':
		current_user = request.session['user_id']
		msg_project_application = request.POST['msg_project_application']

		#Get user
		user_apply = User.objects.get (id = current_user)

		#Get project
		project_apply = Project.objects.get (id = project_id)

		#Get Project Poster
		project_poster = User.objects.get (id = project_poster_id)


		#Check for the user's id and project id exist
		check_project_collabs = User_Project_Collab.objects.filter(user = user_apply).filter (project = project_apply)

		#If exists, remove it
		if (check_project_collabs.exists()):
			check_project_collab = User_Project_Collab.objects.filter(user = user_apply).get(project = project_apply)
			check_project_collab.delete()


		#If collab entry does not exist, add it
		else:
			user_project_collab = User_Project_Collab()
			user_project_collab.user = user_apply
			user_project_collab.project = project_apply

			#0 = pending approval, 1 = approved, collaborating
			user_project_collab.status = 0
			user_project_collab.collab_request_msg = msg_project_application
			user_project_collab.save()


			#Save notification for the collaboration to the project poster
			collab_notif = Notification()
			collab_notif.notification_title = "Project collaboration request"
			collab_notif.notification_content = "{} {} has applied to collaborate in a project you posted".format(user_apply.first_name, user_apply.last_name)
			collab_notif.notification_type = "Collab Application"

			collab_notif.notification_status = 0
			collab_notif.notification_link_to = "/profile_history/{}/".format(current_user)
			collab_notif.notification_date = datetime.today()
			collab_notif.notification_recipient = project_poster
			collab_notif.save()
			messages.success(request, 'Your request to collaborate in a project has been sent', extra_tags='alert-success')

		return redirect('/dashboard')


#Project Collaborations, Track project progresses
def view_projects_collaborations(request):
	current_user = request.session['user_id']
	user_names = request.session['user_names']	

	project_collab_status = [0, 0, 0, 0, 0]
	roles_n_permissions = request.session['roles_n_permissions']

	#Get user
	user_collabs = User.objects.get (id = current_user)

	user_project_collabs = User_Project_Collab.objects.filter(project__user_project = user_collabs).exclude(status = 0)

	unique_projects = set()
	filtered_collabs = []

	for collab in user_project_collabs:
		if collab.project not in unique_projects:
			unique_projects.add(collab.project)
			filtered_collabs.append(collab)

	user_project_collabs = filtered_collabs

	for obj in user_project_collabs:
		column_value = obj.project.project_skills
		if column_value:
			list_value = literal_eval(column_value)
			obj.project.project_skills = list_value
			obj.save()


	#Get All collabs
	get_project_collabs = User_Project_Collab.objects.filter(project__user_project = user_collabs).exclude(status = 0)
	get_project_collab_count = get_project_collabs.count()


	#Get Pending collabs
	get_pending_project_collabs = User_Project_Collab.objects.filter(project__user_project = user_collabs).filter (status = 0)
	get_pending_project_collab_count = get_pending_project_collabs.count()


	#Get Active collabs
	get_active_project_collabs = User_Project_Collab.objects.filter(project__user_project = user_collabs).filter (status = 1)
	get_active_project_collab_count = get_active_project_collabs.count()


	#Get Completed collabs
	get_completed_project_collabs = User_Project_Collab.objects.filter(project__user_project = user_collabs).filter (status = 2)
	get_completed_project_collab_count = get_completed_project_collabs.count()


	#Get Deleted collabs
	get_deleted_project_collabs = User_Project_Collab.objects.filter(project__user_project = user_collabs).filter (status = 3)
	get_deleted_project_collab_count = get_deleted_project_collabs.count()


	project_collab_status[0] = get_project_collab_count
	project_collab_status[1] = get_pending_project_collab_count
	project_collab_status[2] = get_active_project_collab_count
	project_collab_status[3] = get_completed_project_collab_count
	project_collab_status[4] = get_deleted_project_collab_count


	return render (request, "project_collab_page.html", {'user_project_collabs': user_project_collabs, 
		'project_collab_status': project_collab_status, 'user_names': user_names, 'roles_n_permissions': roles_n_permissions})



def profile_history(request, user_id):
	profile_user_id = user_id
	user_x_details = User.objects.get(id = profile_user_id)

	current_user = request.session['user_id']
	me_user = User.objects.get (id = current_user)

	count_completed_projects = Project.objects.filter(user_project = user_x_details).filter(status = 3).count()
	count_active_projects = Project.objects.filter(user_project = user_x_details).filter(status = 1).count()
	all_projects_of_user = Project.objects.filter(user_project = user_x_details)

	user_project_details = [count_completed_projects, count_active_projects]

	for obj in all_projects_of_user:
		column_value = obj.project_skills
		if column_value:
			list_value = literal_eval(column_value)
			obj.project_skills = list_value
			obj.save()

	# return HttpResponse (user_x_details.project_interests)

	#Project Interests
	user_x_details_list = literal_eval(user_x_details.project_interests)
	user_x_details.project_interests = user_x_details_list

	user_x_details_list = literal_eval(user_x_details.learning_interests)
	user_x_details.learning_interests = user_x_details_list

	user_x_details.save()


	#Get collab application
	# collab_applications= User_Project_Collab.objects.filter (user = user_x_details).filter (status = 0).filter(project.user_project = user_x_details)

	collab_applications = User_Project_Collab.objects.filter(user=user_x_details, status = 0, project__user_project = me_user)

	# collab_applications = collab_applications.values('project')

	for obj in collab_applications:
		column_value = obj.project.project_skills
		if column_value:
			list_value = literal_eval(column_value)
			obj.project.project_skills = list_value
			obj.save()


	notifs = get_notifications_of_user (request, current_user)
	user_names = get_user_details(request, current_user)

	"""
	In this query, we use the double underscore (__) notation to perform a related model lookup. The project__user_project represents the user_project field on the related Project model.
	"""
	# id = 7, user = id = 12, f_name = test123, email = test123@gmail.com, status = 1, project = id = 11, title = PLC Programming, status = 1

	# return HttpResponse(collab_applications)


	# User_Project_Collab (models.Model):
	# user = models.ForeignKey(User, on_delete=models.CASCADE)
	# project = models.ForeignKey(Project, on_delete=models.CASCADE)
	# status = models.IntegerField(default=1)


	# Query to merge data based on shared_column
	# merged_collab_data = User_Project_Collab.objects.annotate(other_column2=F('table2__other_column2')).filter(
	# 	shared_column__isnull=False).values('shared_column', 'other_column1', 'other_column2')


	return render (request, "profile_history.html", {'user_project_collabs': all_projects_of_user, 
		'user_project_details': user_project_details, 'user_x_details': user_x_details, 'collab_applications': collab_applications, 
		'notifs': notifs, 'user_names': user_names})



def view_collab_requests(request, project_id):
	current_user = request.session['user_id']
	notifs = get_notifications_of_user (request, current_user)
	user_names = get_user_details(request, current_user)

	me_user = User.objects.get (id = current_user)
	
	project_details = Project.objects.get (id = project_id)

	project_details_list = literal_eval(project_details.project_skills)
	project_details.project_skills = project_details_list
	project_details.save()


	#Get collabs of project from this user
	collab_applications = User_Project_Collab.objects.filter(project=project_details, status = 0, project__user_project = me_user)

	for obj in collab_applications:
		column_value = obj.user.project_interests
		if column_value:
			list_value = literal_eval(column_value)
			obj.user.project_interests = list_value
			obj.save()

	# return HttpResponse (collab_applications)

	return render (request, "collab_requests.html", {'project_details': project_details, 'notifs': notifs, 
		'user_names': user_names, 'collab_applications': collab_applications})


def accept_collab (request, collab_id):
	get_exact_collab_details = User_Project_Collab.objects.get(id = collab_id)

	project_id_of_this_collab = get_exact_collab_details.project.id

	get_exact_collab_details.status = 1
	get_exact_collab_details.save()

	redirect_link = "/view_collab_requests/{}/".format(project_id_of_this_collab)

	messages.success(request, 'Collaboration request approved', extra_tags='alert-success')
	return redirect(redirect_link)

	# return HttpResponse ("accept")


def reject_collab (request, collab_id):
	return HttpResponse ("reject")


def project_collab_tasks(request, project_id):
	current_user = request.session['user_id']
	user_collabs = User.objects.get(id = current_user)

	notifs = get_notifications_of_user (request, current_user)
	user_names = get_user_details(request, current_user)
	project_details = Project.objects.get (id = project_id)

	project_details_list = literal_eval(project_details.project_skills)
	project_details.project_skills = project_details_list
	project_details.save()

	# collaborators_for_project = User_Project_Collab.objects.filter (user__id = current_user).filter(project__id = project_id).exclude(status=0)
	# collaborators_for_project = User_Project_Collab.objects.filter (user__id = current_user).filter(project__id = project_id).exclude(status=0)
	collaborators_for_project = User_Project_Collab.objects.filter(project__user_project = user_collabs).filter(project__id = project_id).exclude(status = 0)

	get_tasks_for_project = Collab_Task.objects.filter(project__id = project_id)


	return render (request, "project_tasks.html", {'project_details': project_details, 'notifs': notifs, 
		'user_names': user_names, 'collaborators_for_project': collaborators_for_project, 'get_tasks_for_project': get_tasks_for_project})


def add_topic(request, module_id):
	current_user = request.session['user_id']

	current_user = request.session['user_id']
	user_details = User.objects.get(id = current_user)
	module_details = Learning_Module.objects.get(id = module_id)
	# file1 = request.POST['file1']


	file1 = request.POST.get ('file1', None)

	if request.method == 'POST':
		topic_name = request.POST['topic_name'] 
		topic_description = request.POST['topic_description'] 
		topic_description = request.POST['topic_description'] 


		module_topic = Module_Topic()
		module_topic.module_belongs_to = module_details
		module_topic.topic_name = topic_name
		module_topic.topic_description = topic_description
		module_topic.topic_tags = ''
		module_topic.save()

		messages.success(request, 'Topic succcessfully added', extra_tags='alert-success')
		red = "/view_topics/" + str(module_id)
		return redirect (red)



def add_summary_content(request, topic_id):
	# current_user = request.session['user_id']
	# rec_proj = recommend_projects(current_user)
	# return HttpResponse (rec_proj)

	# rec_proj = recommend_projects(current_user)
	# return HttpResponse (rec_proj)

	current_user = request.session['user_id']
	user_details = User.objects.get(id = current_user)
	module_topic = Module_Topic.objects.get(id = topic_id)
	# file1 = request.POST['file1']
	file1 = request.POST.get ('file1', None)

	summary_cont = Summary()

	if request.method == 'POST':
		name_summary = request.POST['name_summary'] 
		summary_description = request.POST['summary_description'] 
		# file1 = request.POST['file1']

		destination_path = settings.STATIC_ROOT3

		# Construct the full destination path
		if (file1 != ''):
			i = request.FILES['file1'].name
			destination_fullpath = os.path.join(destination_path, i)

			# pj = ['x', 'x', 'x']

			# Copy the uploaded image to the destination directory
			with open(destination_fullpath, 'wb') as destination_file:
				#For the first index, check at first index of project_images list if submitted
				uploaded_file1 = request.FILES.get('file1')
				# source_file = uploaded_image1.file
				# img_present[0] = ['y']
				copyfileobj(uploaded_file1, destination_file)
				destination_file.close()

				img_extension = os.path.splitext(i)[1]

				# Rename the file
				# img_count = index+1

		else:
			messages.success(request, 'Please add a file', extra_tags='alert-danger')
			redir = "/learning_content/" + str(topic_id)
			return redirect (redir)
			# return redirect ('/view_module/')


		# summary_cont = Summary()
		summary_cont.user = user_details
		summary_cont.module_topic = module_topic
		summary_cont.file_name = name_summary
		summary_cont.file_description = summary_description
		summary_cont.file_link = summary_description
		summary_cont.save()


		if (file1 != ''):
			new_name = 'PLCS' + str(summary_cont.id) + img_extension

			# project_images[index] = new_name
			
			# Construct the full path to the file
			full_path = os.path.join(destination_path, i)

			# Rename the file
			os.rename(full_path, os.path.join(destination_path, new_name))

		else:
			new_name = ''

		summary_cont.file_link = new_name
		summary_cont.save()


		messages.success(request, 'Summary file added', extra_tags='alert-success')

		redir = "/learning_content/" + str(topic_id)
		return redirect (redir)


def view_messages(request):
	current_user = request.session['user_id']
	rec_proj = recommend_projects(current_user)
	return HttpResponse (rec_proj)
	
	# return render (request, "messages_chats.html")


#Recommend Projects
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast



def recommend_projects(user_id):
	# Step 1: Load data from the database

	## Load user data
	user = User.objects.get(id=user_id)
	users = [(user.email, user.project_interests)]

	# Load project data
	projects = [(project.project_id, project.project_skills) for project in Project.objects.all()]

	# Step 2: Preprocess data and compute cosine similarity matrix

	# Preprocess skills for CountVectorizer
	all_skills = [user[1] for user in users] + [project[1] for project in projects]

	# Create CountVectorizer and fit-transform the skills
	vectorizer = CountVectorizer()
	skills_matrix = vectorizer.fit_transform(all_skills)

	# Compute cosine similarity matrix
	user_skills = skills_matrix[:len(users)]
	project_skills = skills_matrix[len(users):]
	cosine_sim_matrix = cosine_similarity(user_skills, project_skills)
	print (cosine_sim_matrix)

	# Step 3: Generate recommendations

	recommendations = []

	for user_index, user in enumerate(users):
		email = user[0]

		# Get cosine similarity scores for the user
		user_sim_scores = cosine_sim_matrix[user_index]

		# Sort projects based on similarity scores
		sorted_indices = user_sim_scores.argsort()[::-1]

		# Get top 15 recommended projects
		num_projects = min(5, len(projects))
		recommended_projects = [projects[i][0] for i in sorted_indices[:num_projects]]

		recommendations.append(recommended_projects)

    # Render the recommendations in a template
	return recommendations



def recommend_learning_material (user_id):
	# Step 1: Load data from the database

	## Load user data
	user = User.objects.get(id=user_id)
	users = [(user.email, user.learning_interests)]

	# Load project data
	projects = [(project.id, project.module_tags) for project in Learning_Module.objects.all()]

	# Step 2: Preprocess data and compute cosine similarity matrix

	# Preprocess skills for CountVectorizer
	all_skills = [user[1] for user in users] + [project[1] for project in projects]

	# Create CountVectorizer and fit-transform the skills
	vectorizer = CountVectorizer()
	skills_matrix = vectorizer.fit_transform(all_skills)

	# Compute cosine similarity matrix
	user_skills = skills_matrix[:len(users)]
	project_skills = skills_matrix[len(users):]
	cosine_sim_matrix = cosine_similarity(user_skills, project_skills)

	# Step 3: Generate recommendations

	learning_recommendations = []

	for user_index, user in enumerate(users):
		email = user[0]

		# Get cosine similarity scores for the user
		user_sim_scores = cosine_sim_matrix[user_index]

		# Sort projects based on similarity scores
		sorted_indices = user_sim_scores.argsort()[::-1]

		# Get top 15 recommended projects
		num_projects = min(5, len(projects))
		recommended_learning_modules = [projects[i][0] for i in sorted_indices[:num_projects]]

		learning_recommendations.append(recommended_learning_modules)

    # Render the recommendations in a template
	return learning_recommendations





def delete_summary(request, summary_id, module_id):
	get_summary = Summary.objects.get (id = summary_id)
	get_summary.delete()

	red = "/view_module/" + str(module_id)
	return redirect (red)