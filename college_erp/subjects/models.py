from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    # Aap chaho toh aur fields add kar sakte ho (code, credit, etc.)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
# Create your models here.
