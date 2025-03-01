from django.contrib import admin
from .models import Task
from django.urls import reverse
from django.utils.html import format_html


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("module_name", "branch_name", "collectstatic", "migrations", "script_name", "start_pipeline")

    def start_pipeline(self, obj):
        return format_html('<a class="button" href="www.google.com">Start Pipeline</a>')

    start_pipeline.short_description = "Pipeline"
