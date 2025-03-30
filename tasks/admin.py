from django.contrib import admin
from .models import Task
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("module_name", "branch_name", "collectstatic", "migrations", "script_name", "start_pipeline")

    def start_pipeline(self, obj):
        jenkins_url = "http://54.174.41.239:8080/job/TaskManagementPipeline/buildWithParameters"
        params = (
            f"BRANCH_NAME={obj.branch_name}&"
            f"MIGRATIONS={'true' if obj.migrations else 'false'}&"
            f"COLLECTSTATIC={'true' if obj.collectstatic else 'false'}&"
            f"MODULE_NAME={obj.module_name}&"
            f"SCRIPT_NAME={obj.script_name or ''}"
        )
        trigger_url = f"{jenkins_url}?{params}"
        return format_html('<a class="button" href="{}">Start Pipeline</a>', trigger_url)

    start_pipeline.short_description = "Pipeline"

