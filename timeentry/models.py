from django.db import models 
import datetime 
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now

def one_day_hence():
    result = timezone.now() - timezone.timedelta(days=1)
    result = result.date()
    return result

def today():
    result = timezone.now()
    result = result.date()
    return result


# Create your models here.
class Department(models.Model):
	name = models.CharField(max_length = 100)
	def __str__(self):
		return self.name	

class Employer(models.Model):
	name = models.CharField(max_length = 100)
	def __str__(self):
		return self.name

class Employee(models.Model):
	employer = models.ForeignKey(Employer, default=2, null=True, blank=True)
	name = models.CharField(max_length = 100)
	number = models.IntegerField()
	department = models.ForeignKey(Department, null=True, blank=True)
	reg = models.DecimalField(default=0, max_digits=4,decimal_places=2)	
	ot = models.DecimalField(default=0, max_digits=4,decimal_places=2)	
	foreman = models.BooleanField(default=False)
	pto = models.IntegerField(default=15)
	def __str__(self):
		return str(self.number)+" " + self.name+" - " + self.department.name

class Salesperson(models.Model):
	name = models.CharField(max_length = 100)
	def __str__(self):
		return self.name

class Customer(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Job(models.Model):
	number = models.IntegerField(primary_key=True)
	customer = models.ForeignKey(Customer, null=True, blank=True)
	name = models.CharField(max_length = 100)
	salesperson = models.ForeignKey(Salesperson, null=True, blank=True)
	value = models.DecimalField(max_digits=11,decimal_places=2)
	v1 = models.BooleanField(default=False)
	v2 = models.BooleanField(default=False)
	v3 = models.BooleanField(default=False)
	f1 = models.BooleanField(default=False)
	f2 = models.BooleanField(default=False)
	f3 = models.BooleanField(default=False)
	h1 = models.BooleanField(default=False)
	h2 = models.BooleanField(default=False)
	h3 = models.BooleanField(default=False)
	i1 = models.BooleanField(default=False)
	i2 = models.BooleanField(default=False)
	i3 = models.BooleanField(default=False)
	s1 = models.BooleanField(default=False)
	s2 = models.BooleanField(default=False)
	s3 = models.BooleanField(default=False)
	podate = models.DateField(null=True, blank=True, default=today)
	isActive = models.BooleanField(default=True)
	def __str__(self):
		return str(self.number) + " " + self.customer.name + " " + self.name

class Category(models.Model):
	name = models.CharField(max_length = 100)
	def __str__(self):
		return self.name

class DepartmentNum(models.Model):
	number = models.IntegerField()
	description = models.CharField(max_length = 50)
	def __str__(self):
		return str(self.number) + " - " + self.description

class Proto(models.Model):
	job = models.ForeignKey(Job)
	category = models.ForeignKey(Category)
	department = models.ForeignKey(DepartmentNum)
	entered_by = models.CharField(max_length = 50)
	entry = models.TextField(max_length = 1000)

class Group(models.Model):
	number = models.IntegerField()
	name = models.CharField(max_length = 100)
	def __str__(self):
		return str(self.number)+" - " + self.name

class TaskType(models.Model):
	name = models.CharField(max_length = 20)	
	def __str__(self):
		return self.name

class Task(models.Model):
	name = models.CharField(max_length = 10)
	description = models.CharField(max_length = 50, null=True, blank=True)
	group = models.ForeignKey(Group)
	task_type = models.ForeignKey(TaskType, null=True, blank=True)
	def __str__(self):
		return self.name + " " + self.description

class Estimate(models.Model):
	job = models.ForeignKey(Job)
	category = models.ForeignKey(Category)
	task = models.ForeignKey(Task)
	hours = models.DecimalField(max_digits=6, decimal_places=2)
	def __str__(self):
		return str(self.job.number) + " " + str(self.category) + " " + str(self.task)

class Entry(models.Model):
	employee = models.ForeignKey(Employee)
	job = models.ForeignKey(Job, null=True, blank=True)
	note = models.CharField(max_length = 50, null=True, blank=True)
	task = models.ForeignKey(Task, null=True, blank=True)
	category = models.ForeignKey(Category)
	reg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	ot = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	dt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	date = models.DateField(null=True, blank=True, default=today)
	def __str__(self):
		return self.employee.name + ": " + str(self.date)

class DeptCheck(models.Model):
	department = models.ForeignKey(Department)
	date = models.DateField(default=today)
	checkedby = models.CharField(max_length = 50, null=True, blank=True)
	def __str__(self):
		return str(self.date) + ": " + str(self.department)

class ClockIn(models.Model):
	time = models.DateTimeField(default=now)
	employee = models.ForeignKey(Employee)