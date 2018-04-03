from django.contrib import admin
from .models import Job
from .models import Category
from .models import Entry
from .models import Employee
from .models import Group
from .models import Task
from .models import Salesperson
from .models import Estimate
from .models import TaskType
from .models import Department
from .models import Customer
from .models import Employer
from .models import DepartmentNum
from .models import Proto
from .models import DeptCheck
from .models import ClockIn
admin.site.register(ClockIn)
admin.site.register(Proto)
admin.site.register(DepartmentNum)
admin.site.register(Department)
admin.site.register(TaskType)
admin.site.register(Estimate)
admin.site.register(Salesperson)
admin.site.register(Group)
admin.site.register(Task)
admin.site.register(Job)
admin.site.register(Category)
admin.site.register(Entry)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Employer)
admin.site.register(DeptCheck)