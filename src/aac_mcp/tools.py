"""
MCP Tools for Alteryx Analytics Cloud Schedule API.
"""

import json
import logging
from typing import Any, Dict

from ..client.schedule_api import ScheduleApi
from ..client.workspace_api import WorkspaceApi
from ..client.person_api import PersonApi
from ..client.plan_api import PlanApi
from ..client.scheduling_models import ScheduleCreateRequest, ScheduleUpdateRequest

logger = logging.getLogger(__name__)

## Schedule API Functions

def list_schedules(schedule_api: ScheduleApi) -> str:
    """List all schedules in the workspace."""
    try:
        response = schedule_api.list_schedules()
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error listing schedules: {e}")
        return json.dumps({"error": f"Error listing schedules: {e}"}, indent=2, default=str)


def get_schedule(schedule_api: ScheduleApi, schedule_id: str) -> str:
    """Get details of a specific schedule by ID.
    
    Args:
        schedule_api: The Schedule API instance
        schedule_id: The ID of the schedule to retrieve
    """
    if not schedule_id:
        return json.dumps({"error": "schedule_id is required"}, indent=2, default=str)
    
    try:
        response = schedule_api.get_schedule(schedule_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting schedule {schedule_id}: {e}")
        return json.dumps({"error": f"Error getting schedule {schedule_id}: {e}"}, indent=2, default=str)

def delete_schedule(schedule_api: ScheduleApi, schedule_id: str) -> str:
    """Delete a schedule by ID.
    
    Args:
        schedule_api: The Schedule API instance
        schedule_id: The ID of the schedule to delete
    """
    if not schedule_id:
        return json.dumps({"error": "schedule_id is required"}, indent=2, default=str)

    try:
        # check if the schedule exists
        response = schedule_api.get_schedule(schedule_id)
        if response is None:
            logger.error(f"Schedule {schedule_id} not found")
            return json.dumps({"error": f"Schedule {schedule_id} not found"}, indent=2, default=str)
        
        # check if the schedule is currently enabled and cannot be deleted
        if response.get("enabled", False):
            logger.error(f"Schedule {schedule_id} is currently enabled and cannot be deleted")
            return json.dumps({"error": f"Schedule {schedule_id} is currently enabled and cannot be deleted"}, indent=2, default=str)
        
        # delete the schedule
        response = schedule_api.delete_schedule(schedule_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error deleting schedule {schedule_id}: {e}")
        return json.dumps({"error": f"Error deleting schedule {schedule_id}: {e}"}, indent=2, default=str)


def enable_schedule(schedule_api: ScheduleApi, schedule_id: str) -> str:
    """Enable a schedule by ID.
    
    Args:
        schedule_api: The Schedule API instance
        schedule_id: The ID of the schedule to enable
    """
    if not schedule_id:
        return json.dumps({"error": "schedule_id is required"}, indent=2, default=str)
    
    try:
        # check if the schedule exists
        response = schedule_api.get_schedule(schedule_id)
        if response is None:
            logger.error(f"Schedule {schedule_id} not found")
            return json.dumps({"error": f"Schedule {schedule_id} not found"}, indent=2, default=str)
        
        response = schedule_api.enable_schedule(schedule_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error enabling schedule {schedule_id}: {e}")
        return json.dumps({"error": f"Error enabling schedule {schedule_id}: {e}"}, indent=2, default=str)


def disable_schedule(schedule_api: ScheduleApi, schedule_id: str) -> str:
    """Disable a schedule by ID.
    
    Args:
        schedule_api: The Schedule API instance
        schedule_id: The ID of the schedule to disable
    """
    if not schedule_id:
        return json.dumps({"error": "schedule_id is required"}, indent=2, default=str)
    
    try:
        # check if the schedule exists
        response = schedule_api.get_schedule(schedule_id)
        if response is None:
            logger.error(f"Schedule {schedule_id} not found")
            return json.dumps({"error": f"Schedule {schedule_id} not found"}, indent=2, default=str)
        
        response = schedule_api.disable_schedule(schedule_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error disabling schedule {schedule_id}: {e}")
        return json.dumps({"error": f"Error disabling schedule {schedule_id}: {e}"}, indent=2, default=str)


def count_schedules(schedule_api: ScheduleApi) -> str:
    """Get the count of schedules in the workspace.
    
    Args:
        schedule_api: The Schedule API instance
    """
    try:
        response = schedule_api.count_schedules()
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error counting schedules: {e}")
        return json.dumps({"error": f"Error counting schedules: {e}"}, indent=2, default=str)


## Workspace API Functions

def get_current_workspace(workspace_api: WorkspaceApi) -> str:
    """Get information about the current workspace.
    
    Args:
        workspace_api: The Workspace API instance
    """
    try:
        response = workspace_api.read_current_workspace()
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting current workspace: {e}")
        return json.dumps({"error": f"Error getting current workspace: {e}"}, indent=2, default=str)
    
def get_workspace_configuration(workspace_api: WorkspaceApi, workspace_id: str) -> str:
    """Get workspace configuration.
    
    Args:
        workspace_api: The Workspace API instance
        workspace_id: The ID of the workspace
    """    
    try:
        # get the workspace configuration
        response = workspace_api.get_configuration_for_workspace(workspace_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting workspace configuration for {workspace_id}: {e}")
        return json.dumps({"error": f"Error getting workspace configuration for {workspace_id}: {e}"}, indent=2, default=str)


def list_workspace_users(workspace_api: WorkspaceApi, workspace_id: str) -> str:
    """List workspace users.
    
    Args:
        workspace_api: The Workspace API instance
        workspace_id: The ID of the workspace
    """
    try:
        # check if the workspace exists
        response = workspace_api.get_workspace(workspace_id)
        if response is None:
            logger.error(f"Workspace {workspace_id} not found")
            return json.dumps({"error": f"Workspace {workspace_id} not found"}, indent=2, default=str)
        
        # list the workspace users
        response = workspace_api.list_workspace_users(workspace_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error listing workspace users: {e}")
        return json.dumps({"error": f"Error listing workspace users: {e}"}, indent=2, default=str)


def list_workspace_admins(person_api: PersonApi, workspace_api: WorkspaceApi, workspace_id: str) -> str:
    """List workspace admins.
    
    Args:
        person_api: The Person API instance
        workspace_id: The ID of the workspace
    """
    try:
        # check if the workspace exists
        response = workspace_api.get_configuration_for_workspace(workspace_id)
        if response is None:
            logger.error(f"Workspace {workspace_id} not found")
            return json.dumps({"error": f"Workspace {workspace_id} not found"}, indent=2, default=str)
        
        response = person_api.list_workspace_admins(workspace_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error listing workspace admins: {e}")
        return json.dumps({"error": f"Error listing workspace admins: {e}"}, indent=2, default=str)


## Person API Functions
def get_user(person_api: PersonApi, user_id: str) -> str:
    """Get person details by ID.
    
    Args:
        person_api: The Person API instance
        user_id: The ID of the user to retrieve
    """
    if not user_id:
        return json.dumps({"error": "user_id is required"}, indent=2, default=str)
    
    try:
        response = person_api.get_person(user_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return json.dumps({"error": f"Error getting user {user_id}: {e}"}, indent=2, default=str)


##  Plan API Functions
def count_plans(plan_api: PlanApi) -> str:
    """Get the count of plans.
    
    Args:
        plan_api: The Plan API instance
        """
    try:
        response = plan_api.count_plans()
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error counting plans: {e}")
        return json.dumps({"error": f"Error counting plans: {e}"}, indent=2, default=str)

def list_plans(plan_api: PlanApi) -> str:
    """List plans. Retrieve all existing plans along with their details, using query parameters to filter the results.
    
    Args:
        plan_api: The Plan API instance
    """
    try:
        response = plan_api.list_plans()
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error listing plans: {e}")
        return json.dumps({"error": f"Error listing plans: {e}"}, indent=2, default=str)

def get_plan(plan_api: PlanApi, plan_id: str) -> str:
    """Get a plan by ID.
    
    Args:
        plan_api: The Plan API instance
        plan_id: The ID of the plan to retrieve
    """
    if not plan_id:
        return json.dumps({"error": "plan_id is required"}, indent=2, default=str)
    
    try:        
        response = plan_api.read_full(plan_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting plan {plan_id}: {e}")
        return json.dumps({"error": f"Error getting plan {plan_id}: {e}"}, indent=2, default=str)

def get_plan_schedules(plan_api: PlanApi, plan_id: str) -> str:
    """Get the schedules for a plan by ID.
    
    Args:
        plan_api: The Plan API instance
        plan_id: The ID of the plan to get the schedules for
    """
    if not plan_id:
        return json.dumps({"error": "plan_id is required"}, indent=2, default=str)
    
    try:
        # check if the plan exists
        response = plan_api.read_full(plan_id)
        if response is None:
            logger.error(f"Plan {plan_id} not found")
            return json.dumps({"error": f"Plan {plan_id} not found"}, indent=2, default=str)
        
        # get the schedules for the plan
        response = plan_api.get_schedules_for_plan(plan_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting schedules for plan {plan_id}: {e}")
        return json.dumps({"error": f"Error getting schedules for plan {plan_id}: {e}"}, indent=2, default=str)

def delete_plan(plan_api: PlanApi, plan_id: str) -> str:
    """Delete a plan by ID.
    
    Args:
        plan_api: The Plan API instance
        plan_id: The ID of the plan to delete
    """
    if not plan_id:
        return json.dumps({"error": "plan_id is required"}, indent=2, default=str)
    
    try:
        # check if the plan exists
        response = plan_api.read_full(plan_id)
        if response is None:
            logger.error(f"Plan {plan_id} not found")
            return json.dumps({"error": f"Plan {plan_id} not found"}, indent=2, default=str)
        
        # delete the plan
        response = plan_api.delete_plan(plan_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error deleting plan {plan_id}: {e}")
        return json.dumps({"error": f"Error deleting plan {plan_id}: {e}"}, indent=2, default=str)

def run_plan(plan_api: PlanApi, plan_id: str) -> str:
    """Run a plan by ID.
    
    Args:
        plan_api: The Plan API instance
        plan_id: The ID of the plan to run
    """
    if not plan_id:
        return json.dumps({"error": "plan_id is required"}, indent=2, default=str)
    
    try:
        # check if the plan exists
        response = plan_api.read_full(plan_id)
        if response is None:
            logger.error(f"Plan {plan_id} not found")
            return json.dumps({"error": f"Plan {plan_id} not found"}, indent=2, default=str)
        
        response = plan_api.run_plan(plan_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error running plan {plan_id}: {e}")
        return json.dumps({"error": f"Error running plan {plan_id}: {e}"}, indent=2, default=str)
    