from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Job, Entry, Task, Estimate, Department, Employee, Category, Group, Proto, DepartmentNum, Customer, DeptCheck, ClockIn
from django.contrib.auth import authenticate, login, get_user_model, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import JobForm, EmployeeForm, UserLoginForm
import datetime
from django.db.models import Q
from django import forms
#from datetime import datetime, timedelta, time

today = datetime.datetime.now().date()
tomorrow = today + datetime.timedelta(1)

class EntryDelete(DeleteView):
    model = Entry
    success_url = reverse_lazy('entry')

class ClockInDelete(DeleteView):
    model = ClockIn
    success_url = reverse_lazy('entry')

def selection(request):
	all_jobs = Job.objects.all().order_by('-number')
	return render(request, 'timeentry/selection.html', {'all_jobs' : all_jobs})

def deptcheckselect(request):
    all_departments = Department.objects.all()
    return render(request, 'timeentry/deptcheckselection.html', {'all_departments' : all_departments})

def allptoselect(request):
    return render(request, 'timeentry/allptoselect.html')

def protoSelect(request):
    all_jobs = Job.objects.all().order_by('-number')
    return render(request, 'timeentry/protoselect.html', {'all_jobs' : all_jobs})

def summary(request, job):
    job = get_object_or_404(Job, pk=job)
    num = job.number
    needed_entries = Entry.objects.filter(job=num)
    all_categories = Category.objects.all()
    all_tasks = Task.objects.all()
    all_estimates = Estimate.objects.filter(job=num)
    all_departments = Department.objects.all()
    all_groups = Group.objects.all()
    return render(request, 'timeentry/hours_summary.html', {'all_groups': all_groups, 'all_categories': all_categories, 'all_departments': all_departments, 'needed_entries' : needed_entries, 'job': job, 'all_tasks': all_tasks, 'all_estimates': all_estimates})

def warranty(request, year, month, day, year2, month2, day2):
    last_date = datetime.date(int(year), int(month), int(day))
    first_date = datetime.date(int(year2), int(month2), int(day2))
    needed_entries = Entry.objects.filter(Q(date__range=(first_date,last_date)) & Q(job=100)).order_by('note')
    return render(request, 'timeentry/warranty.html', {'last_date': last_date, 'first_date':first_date, 'needed_entries': needed_entries})

def proto(request, job):
    job = get_object_or_404(Job, pk=job)
    num = job.number
    categories = Category.objects.all()
    departmentNum = DepartmentNum.objects.all()
    needed_proto = Proto.objects.filter(job=num).order_by('category','department')
    return render(request, 'timeentry/proto_summary.html', {'categories':categories, 'departmentNum':departmentNum, 'needed_proto' : needed_proto, 'job': job})

def tasksummary(request, job, task):
    job = get_object_or_404(Job, pk=job)
    num = job.number
    task = Task.objects.filter(name=task)
    all_departments = Department.objects.all()
    needed_entries = Entry.objects.filter(job=num, task=task).order_by('-date')
    return render(request, 'timeentry/tasksummary.html', {'needed_entries': needed_entries, 'task': task, 'job': job, 'all_departments': all_departments})

class EntryForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('number'))
    job = forms.ModelChoiceField(queryset=Job.objects.filter(isActive=True).order_by('number'))
    task = forms.ModelChoiceField(queryset=Task.objects.all().order_by('name'))
    class Meta:
        model = Entry
        fields = ['note', 'task', 'category', 'reg', 'ot', 'dt', 'date', 'job', 'employee']
		
class SelfEntryForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('number'))
    job = forms.ModelChoiceField(queryset=Job.objects.filter(isActive=True).order_by('-number'))
    task = forms.ModelChoiceField(queryset=Task.objects.all().order_by('name'))
    class Meta:
        model = Entry
        fields = ['job', 'note', 'category', 'task', 'reg', 'ot', 'dt', 'date', 'employee']

class EntryCreate(CreateView):
    form_class=EntryForm
    model = Entry
    def get_context_data(self, **kwargs):
        active_jobs = Job.objects.filter(isActive=True)
        all_jobs = Job.objects.all().order_by('-number')
        context = super(EntryCreate, self).get_context_data(**kwargs)
        context['all_jobs'] = all_jobs
        context['active_jobs'] = active_jobs
        return context

class EmployeeEntryCreate(CreateView):
    form_class=SelfEntryForm
    template_name='timeentry/employee_entry_form.html'
    model = Entry
    def get_context_data(self, **kwargs):
        active_jobs = Job.objects.filter(isActive=True)
        all_jobs = Job.objects.all().order_by('-number')
        context = super(EmployeeEntryCreate, self).get_context_data(**kwargs)
        context['all_jobs'] = all_jobs
        context['active_jobs'] = active_jobs
        return context

class ClockInCreate(CreateView):
    template_name = 'timeentry/clockin.html'
    model = ClockIn
    fields = ['time', 'employee']
    def get_context_data(self, **kwargs): 
        context = super(ClockInCreate, self).get_context_data(**kwargs)   
        needed_clockins = ClockIn.objects.filter(time__range=(today,tomorrow))
        context['needed_clockins'] = needed_clockins     
        return context

class DeptCheckCreate(CreateView):
    template_name = 'timeentry/deptcheck.html' #take this out to go back to using the form
    model = DeptCheck
    fields = ['department', 'date', 'checkedby']
    def get_context_data(self, **kwargs): 
        day = self.kwargs['day']
        month = self.kwargs['month']
        year = self.kwargs['year']
        last_date = datetime.date(int(year), int(month), int(day)) 
        first_date = last_date-datetime.timedelta(days=6) 
        check_date = last_date+datetime.timedelta(days=1)
        department = self.kwargs['department'] 
        departmentname = Department.objects.filter(pk=department)
        needed_clockins = ClockIn.objects.filter(Q(time__range=(first_date, check_date)) & Q(employee__department = department)).order_by('time')
        needed_entries = Entry.objects.filter(Q(date__range=(first_date, last_date)) & Q(employee__department = department)).order_by('date')
        needed_checks = DeptCheck.objects.filter(Q(date__range=(last_date, check_date)) & Q(department = department))
        context = super(DeptCheckCreate, self).get_context_data(**kwargs)
        context['needed_entries'] = needed_entries
        context['needed_clockins'] = needed_clockins
        context['last_date'] = last_date
        context['departmentname'] = departmentname
        context['department'] = department
        context['needed_checks'] = needed_checks
        return context

class ProtoForm(forms.ModelForm):
    class Meta:
        model = Proto
        fields = ['job', 'category', 'department', 'entry', 'entered_by']
 
class ProtoCreate(CreateView):
    form_class=ProtoForm
    model = Proto
    def get_context_data(self, **kwargs):
        all_jobs = Job.objects.all().order_by('-number')
        context = super(ProtoCreate, self).get_context_data(**kwargs)
        context['all_jobs'] = all_jobs
        return context
 
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = []
 
class JobCreate(CreateView):
    form_class=JobForm
    model = Job
    template_name = 'timeentry/generic_form.html'
    def get_context_data(self, **kwargs):
        context = super(JobCreate, self).get_context_data(**kwargs)
        return context
  
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = []
   
class ClockInForm(forms.ModelForm):
    class Meta:
        model = ClockIn
        exclude = []

class EmployeeCreate(CreateView):
    form_class=EmployeeForm
    model = Employee
    template_name = 'timeentry/generic_form.html'
    def get_context_data(self, **kwargs):
        context = super(EmployeeCreate, self).get_context_data(**kwargs)
        return context
 
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = []
 
class CustomerCreate(CreateView):
    form_class=CustomerForm
    model = Customer
    template_name = 'timeentry/generic_form.html'
    def get_context_data(self, **kwargs):
        context = super(CustomerCreate, self).get_context_data(**kwargs)
        return context

class ClockInCreateManual(CreateView):
    form_class=ClockInForm
    model = ClockIn
    template_name = 'timeentry/generic_form.html'
    def get_context_data(self, **kwargs):
        context = super(ClockInCreateManual, self).get_context_data(**kwargs)
        return context

def vms(request, year, month, day):
    week_ending = datetime.date(int(year), int(month), int(day))
    year = year
    month = month
    day = day
    last_date = week_ending
    check_date = week_ending+datetime.timedelta(days=1)
    first_date = week_ending-datetime.timedelta(days=6)
    needed_entries = Entry.objects.filter(date__range=(first_date, last_date))
    dept_checks = DeptCheck.objects.filter(Q(date=last_date) | Q(date=check_date))
    all_departments = Department.objects.all()
    all_employees = Employee.objects.filter(employer=2)
    return render(request, 'timeentry/vms.html', {'year':year, 'month':month, 'day':day, 'dept_checks':dept_checks, 'all_departments':all_departments,'last_date':last_date, 'needed_entries': needed_entries, 'all_employees': all_employees})

def gillman(request, year, month, day):
    week_ending = datetime.date(int(year), int(month), int(day))
    last_date = week_ending
    first_date = week_ending-datetime.timedelta(days=6)
    needed_entries = Entry.objects.filter(date__range=(first_date, last_date))
    needed_employees = Employee.objects.filter(employer=1)
    vendor = "Gillman"
    return render(request, 'timeentry/gillman.html', {'vendor':vendor,'last_date':last_date, 'needed_entries': needed_entries, 'needed_employees': needed_employees})

def aerotek(request, year, month, day):
    week_ending = datetime.date(int(year), int(month), int(day))
    last_date = week_ending
    first_date = week_ending-datetime.timedelta(days=6)
    needed_entries = Entry.objects.filter(date__range=(first_date, last_date))
    needed_employees = Employee.objects.filter(employer=3)
    vendor = "Aerotek"
    return render(request, 'timeentry/gillman.html', {'vendor':vendor,'last_date':last_date, 'needed_entries': needed_entries, 'needed_employees': needed_employees})

def timecardselection(request):    
    all_employees = Employee.objects.all().order_by('number')
    return render(request, 'timeentry/employees.html', {'all_employees' : all_employees})

def ptoselection(request):    
    all_employees = Employee.objects.all().order_by('number')
    return render(request, 'timeentry/ptoselect.html', {'all_employees' : all_employees})

def employeeselection(request):    
    all_employees = Employee.objects.all().order_by('number')
    return render(request, 'timeentry/employeeselect.html', {'all_employees' : all_employees})

def jobselection(request):    
    all_jobs = Job.objects.all().order_by('number')
    return render(request, 'timeentry/jobselection.html', {'all_jobs' : all_jobs})

def timecard(request, employee, year, month, day):
    week_ending = datetime.date(int(year), int(month), int(day))
    last_date = week_ending
    last_clock = week_ending+datetime.timedelta(days=1)
    first_date = week_ending-datetime.timedelta(days=6)
    person = Employee.objects.filter(number=employee)
    needed_clockins = ClockIn.objects.filter(employee = person, time__range=(first_date, last_clock)).order_by('time')
    needed_entries = Entry.objects.filter(employee = person, date__range=(first_date, last_date)).order_by('date')
    return render(request, 'timeentry/timecard.html', {'last_date': last_date, 'needed_entries': needed_entries, 'person': person, 'needed_clockins': needed_clockins})

def jobssold(request, year, month, day, year2, month2, day2):
    last_date = datetime.date(int(year), int(month), int(day))
    first_date = datetime.date(int(year2), int(month2), int(day2))
    needed_jobs = Job.objects.filter(podate__range=(first_date, last_date)).order_by('salesperson')
    return render(request, 'timeentry/jobssold.html', {'last_date': last_date, 'first_date':first_date, 'needed_jobs': needed_jobs})

class EntryUpdate(UpdateView):
    model = Entry
    fields = ['employee', 'job', 'note', 'category', 'task', 'reg', 'ot', 'dt', 'date']
    def get_context_data(self, **kwargs):
        active_jobs = Job.objects.all()
        all_jobs = Job.objects.all().order_by('-number')
        context = super(EntryUpdate, self).get_context_data(**kwargs)
        context['all_jobs'] = all_jobs
        context['active_jobs'] = active_jobs
        return context
    def get_success_url(self):
        return reverse('selection')

class EmployeeUpdate(UpdateView):
    model = Employee
    form = EmployeeForm
    fields = ['number', 'department', 'employer', 'pto', 'foreman', 'reg', 'ot']
    template_name = 'timeentry/generic_form.html'
    def get_success_url(self):
        return reverse('selection')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Employee "
        context['title2'] = self.object.name
        return context

class ClockInUpdate(UpdateView):
    model = ClockIn
    form = EmployeeForm
    fields = ['time']
    template_name = 'timeentry/generic_form.html'
    def get_success_url(self):
        return reverse('selection')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update ClockIn "
        context['title2'] = self.object.employee
        return context

class JobUpdate(UpdateView):
    model = Job
    form = JobForm
    fields = ['v1', 'v2', 'v3', 'f1', 'f2', 'f3', 'h1', 'h2', 'h3', 'i1', 'i2', 'i3', 'isActive']
    template_name = 'timeentry/generic_form.html'
    def get_success_url(self):
        return reverse('selection')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Job #"
        context['title2'] = self.object
        return context
     		
class ProtoUpdate(UpdateView):
    model = Proto
    fields = ['job', 'category', 'department', 'entry', 'entered_by']
    def get_success_url(self):
        return reverse('protoSelect')

def vmsselect(request):
    return render(request, 'timeentry/vmsselect.html', {})
def ltspselect(request):
    return render(request, 'timeentry/ltspselect.html', {})
def warrantyselect(request):
    return render(request, 'timeentry/warrantyselect.html', {})
def jobssoldselect(request):
    return render(request, 'timeentry/jobssoldselect.html', {})
def workedselect(request):
    return render(request, 'timeentry/workedselect.html', {})
def fworkedselect(request):
    return render(request, 'timeentry/fworkedselect.html', {})
def gillmanselect(request):
    return render(request, 'timeentry/gillmanselect.html', {})
def aerotekselect(request):
    return render(request, 'timeentry/aerotekselect.html', {})

def ltsp(request, year, month, day, year2, month2, day2):
    last_date = datetime.date(int(year), int(month), int(day))
    first_date = datetime.date(int(year2), int(month2), int(day2))
    needed_entries = Entry.objects.filter(Q(date__range=(first_date,last_date)) & Q(job=0)).order_by('-date')
    all_departments = Department.objects.all()
    all_employees = Employee.objects.all().order_by('number')
    return render(request, 'timeentry/ltsp.html', {'day':day, 'year':year, 'month':month, 'month2':month2,'day2':day2,'year2':year2, 'all_employees': all_employees, 'all_departments': all_departments, 'last_date': last_date, 'first_date':first_date, 'needed_entries': needed_entries})

def empltsp(request, employee, year, month, day, year2, month2, day2):
    person = Employee.objects.filter(number=employee)
    last_date = datetime.date(int(year), int(month), int(day))
    first_date = datetime.date(int(year2), int(month2), int(day2))
    needed_entries = Entry.objects.filter(Q(date__range=(first_date,last_date)) & Q(job=0) & Q(employee = person)).order_by('-date')
    return render(request, 'timeentry/empltsp.html', {'person': person, 'last_date': last_date, 'first_date':first_date, 'needed_entries': needed_entries})

def worked(request, year, month, day, year2, month2, day2):
    last_date = datetime.date(int(year), int(month), int(day))
    first_date = datetime.date(int(year2), int(month2), int(day2))
    days = (last_date-first_date).days
    needed_entries = Entry.objects.filter(Q(date__range=(first_date,last_date)) & Q(employee__department__lte=9)).order_by('-date')
    all_departments = Department.objects.all()
    all_employees = Employee.objects.all().order_by('number')
    return render(request, 'timeentry/worked.html', {'days':days,'day':day, 'year':year, 'month':month, 'month2':month2,'day2':day2,'year2':year2, 'all_employees': all_employees, 'all_departments': all_departments, 'last_date': last_date, 'first_date':first_date, 'needed_entries': needed_entries})

def foremenworked(request, year, month, day, year2, month2, day2):
    last_date = datetime.date(int(year), int(month), int(day))
    first_date = datetime.date(int(year2), int(month2), int(day2))
    days = (last_date-first_date).days
    needed_entries = Entry.objects.filter(Q(date__range=(first_date,last_date)) & Q(employee__foreman=True)).order_by('-date')
    all_departments = Department.objects.all()
    all_employees = Employee.objects.all().order_by('number')
    return render(request, 'timeentry/worked.html', {'days':days,'day':day, 'year':year, 'month':month, 'month2':month2,'day2':day2,'year2':year2, 'all_employees': all_employees, 'all_departments': all_departments, 'last_date': last_date, 'first_date':first_date, 'needed_entries': needed_entries})

def pto(request, year, employee):
    last_date = datetime.date(int(year), 12,31)
    first_date = datetime.date(int(year),1,1)
    needed_employee = Employee.objects.filter(number=employee)
    needed_entries = Entry.objects.filter(Q(date__range=(first_date,last_date)) & Q(employee__number=employee) & Q(job=1)).order_by('date')
    context = {'last_date':last_date,'first_date':first_date, 'needed_entries':needed_entries, 'needed_employee':needed_employee}
    return render(request, 'timeentry/pto.html', context)

def allpto(request, year):
    last_date = datetime.date(int(year), 12,31)
    first_date = datetime.date(int(year),1,1)
    needed_entries = Entry.objects.filter(Q(date__range=(first_date,last_date)) & Q(employee__employer=2) & Q(job=1)).order_by('date')
    context = {'last_date':last_date,'first_date':first_date, 'needed_entries':needed_entries}
    return render(request, 'timeentry/allpto.html', context)

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('selection')
    return render(request, "timeentry/login_form.html", {"form":form})

def logout_view(request):
    logout(request)
    return redirect('selection')
