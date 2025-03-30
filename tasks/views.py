import requests
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Task

def trigger_jenkins_build(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    jenkins_url = "http://54.174.41.239:8080/job/TaskManagementPipeline/buildWithParameters"
    params = {
        'BRANCH_NAME': task.branch_name,
        'MIGRATIONS': 'true' if task.migrations else 'false',
        'COLLECTSTATIC': 'true' if task.collectstatic else 'false',
        'MODULE_NAME': task.module_name,
        'SCRIPT_NAME': task.script_name or '',
    }
    
    # Jenkins credentials from settings
    auth = (settings.JENKINS_USER, settings.JENKINS_API_TOKEN)
    
    # Get the Jenkins crumb
    crumb_url = "http://54.174.41.239:8080/crumbIssuer/api/json"
    try:
        crumb_response = requests.get(crumb_url, auth=auth)
        crumb_response.raise_for_status()
        crumb_data = crumb_response.json()
        headers = {crumb_data['crumbRequestField']: crumb_data['crumb']}
    except Exception as e:
        messages.error(request, f"Failed to get Jenkins crumb: {e}")
        return redirect('/admin/tasks/task/')
    
    # Trigger the build with POST and include the crumb in headers
    response = requests.post(jenkins_url, params=params, auth=auth, headers=headers)
    
    if response.status_code in (200, 201):
        messages.success(request, "Jenkins build triggered successfully!")
    else:
        messages.error(request, f"Failed to trigger Jenkins build: {response.content}")
    
    # Redirect back to the admin page (adjust the URL as needed)
    return redirect('/admin/tasks/task/')
