import requests
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Task
from urllib.parse import urlencode


def trigger_jenkins_build(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    params = {
        'token': 'Task',  # From Jenkins job config
        'BRANCH_NAME': task.branch_name,
        'MIGRATIONS': 'true' if task.migrations else 'false',
        'COLLECT_STATIC': 'true' if task.collectstatic else 'false',  # Fixed name
        'MODULE_NAME': task.module_name,
        'SCRIPT_NAME': task.script_name or '',
    }
    
    session = requests.Session()
    session.auth = (settings.JENKINS_USER, settings.JENKINS_API_TOKEN)
    
    try:
        # Get CSRF crumb
        crumb_response = session.get(
            "http://54.174.41.239:8080/crumbIssuer/api/json"
        )
        crumb_response.raise_for_status()
        crumb = crumb_response.json()
        
        # Send build trigger
        response = session.post(
            "http://54.174.41.239:8080/job/TaskManagementPipeline/buildWithParameters",
            data=urlencode(params),
            headers={
                crumb['crumbRequestField']: crumb['crumb'],
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        
        if response.status_code in (200, 201):
            messages.success(request, "Build triggered successfully!")
        else:
            raise ValidationError(
                f"Jenkins API Error ({response.status_code}): {response.text}"
            )
            
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    
    return redirect('/admin/tasks/task/')