from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django import forms
from .models import Job, Employee

class JobForm(forms.ModelForm):
	class Meta:
		model = Job
		fields = ['v1', 'v2', 'v3', 'f1', 'f2', 'f3', 'h1', 'h2', 'h3', 'i1', 'i2', 'i3']

class EmployeeForm(forms.ModelForm):
	class Meta:
		model = Employee
		fields = ['number', 'department', 'employer', 'pto', 'foreman', 'reg', 'ot']

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")

			if not user.is_active:
				raise forms.ValidationError("This user is no longer active.")
		return super(UserLoginForm, self).clean(*args, **kwargs)