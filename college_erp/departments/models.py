from django.db import models

# dashboard/models.py

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=20)

    # YE WALA PART ADD KARO ✅
    def __str__(self):
        return self.department_name
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name

class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_staff_members')
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.name