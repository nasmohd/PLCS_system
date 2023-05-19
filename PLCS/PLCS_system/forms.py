from django import forms
from myapp.models import Employee


class EmployeeForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email', )