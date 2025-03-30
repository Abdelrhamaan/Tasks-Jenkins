from django.db import models

# Create your models here.

from django.db import models


class Task(models.Model):
    MODULE_CHOICES = [
        ("employees", "Employees"),
        ("departments", "Departments"),
    ]

    module_name = models.CharField(max_length=50, choices=MODULE_CHOICES)
    collectstatic = models.BooleanField(default=False)
    script_name = models.CharField(max_length=100, blank=True, null=True)
    migrations = models.BooleanField(default=False)
    branch_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.module_name} - {self.branch_name}"
