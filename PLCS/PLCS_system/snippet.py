def add_project(request):
	# skills = request.POST['skills_required']
	# skills_list = skills.split(", ")

	if request.method == 'POST':
		task_deadlines = request.POST.getlist('task_deadline[]')
		task_details = request.POST.getlist('task_details[]')
		sub_tasks = []

		for i in range(len(task_details)):
			sub_task_key = f'sub_tasks[{i}][]'
			sub_task_values = request.POST.getlist(sub_task_key)
			task_data = [task_deadlines[i], task_details[i], sub_task_values]
			sub_tasks.append(task_data)

		# Save the tasks in your desired way (e.g., to a database)
		# ...
		print (sub_tasks)
		return HttpResponse(sub_tasks)