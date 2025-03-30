# admin.py
from django.urls import reverse
from django.utils.html import format_html
from django.conf import settings
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("module_name", "branch_name", "collectstatic", "migrations", "script_name", "start_pipeline")

    def start_pipeline(self, obj):
        # Assuming you have configured a URL pattern named 'trigger_jenkins_build'
        url = reverse("tasks/trigger_jenkins_build", args=[obj.id])
        return format_html('<a class="button" href="{}">Start Pipeline</a>', url)

    start_pipeline.short_description = "Pipeline"
