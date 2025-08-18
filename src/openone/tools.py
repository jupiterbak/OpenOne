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
from ..client.legacy_person_api import PersonApi as LegacyPersonApi
from ..client.legacy_workspace_api import WorkspaceApi as LegacyWorkspaceApi
from ..client.legacy_imported_dataset_api import ImportedDatasetApi as LegacyImportedDatasetApi
from ..client.legacy_connection_api import ConnectionApi as LegacyConnectionApi
from ..client.legacy_publication_api import PublicationApi as LegacyPublicationApi
from ..client.legacy_wrangled_dataset_api import WrangledDatasetApi as LegacyWrangledDatasetApi

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
def list_workspaces(workspace_api: LegacyWorkspaceApi) -> str:
    """List all workspaces available to the current user.
    
    Args:
        workspace_api: The Workspace API instance
        account_id: The ID of the account to list workspaces for. If not provided, the current user's account ID will be used.
        """
    try:
        response = workspace_api.list_workspaces()
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error listing workspaces: {e}")
        return json.dumps({"error": f"Error listing workspaces: {e}"}, indent=2, default=str)
    

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
        response = workspace_api.get_configuration_for_workspace(workspace_id)
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
    
def get_current_user(person_api: LegacyPersonApi) -> str:
    """Get the current user.
    
    Args:
        person_api: The Legacy Person API instance
    """
    try:
        response = person_api.get_current_person()
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        return json.dumps({"error": f"Error getting current user: {e}"}, indent=2, default=str)

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
    
# Legacy dataset API Functions
def list_datasets(dataset_api: LegacyImportedDatasetApi) -> str:
    """List all datasets.
    
    Args:
        dataset_api: The Dataset API instance
    """
    try:
        response = dataset_api.list_dataset_library(datasets_filter="all", ownership_filter="all", schematized=False, limit=100)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error listing datasets: {e}")
        return json.dumps({"error": f"Error listing datasets: {e}"}, indent=2, default=str)
    
    
def get_dataset(dataset_api: LegacyImportedDatasetApi, dataset_id: str) -> str:
    """Get a dataset by ID.
    
    Args:
        dataset_api: The Dataset API instance
        dataset_id: The ID of the dataset to retrieve
    """
    if not dataset_id:
        return json.dumps({"error": "dataset_id is required"}, indent=2, default=str)
    
    try:
        response = dataset_api.get_imported_dataset(dataset_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting dataset {dataset_id}: {e}")
        return json.dumps({"error": f"Error getting dataset {dataset_id}: {e}"}, indent=2, default=str)
    
# Connection API Functions
def list_connections(connection_api: LegacyConnectionApi) -> str:
    """List all connections.
    
    Args:
        connection_api: The Connection API instance
    """
    try:
        response = connection_api.list_connections()
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error listing connections: {e}")
        return json.dumps({"error": f"Error listing connections: {e}"}, indent=2, default=str)
    
def get_connection(connection_api: LegacyConnectionApi, connection_id: str) -> str:
    """Get a connection by ID.
    
    Args:
        connection_api: The Connection API instance
        connection_id: The ID of the connection to retrieve
    """
    if not connection_id:
        return json.dumps({"error": "connection_id is required"}, indent=2, default=str)
    
    try:
        response = connection_api.get_connection(connection_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting connection {connection_id}: {e}")
        return json.dumps({"error": f"Error getting connection {connection_id}: {e}"}, indent=2, default=str)
    
def get_connection_status(connection_api: LegacyConnectionApi, connection_id: str) -> str:
    """Get the status of a connection by ID.
    
    Args:
        connection_api: The Connection API instance
        connection_id: The ID of the connection to retrieve
    """
    if not connection_id:
        return json.dumps({"error": "connection_id is required"}, indent=2, default=str)
    
    try:
        # check if the connection exists
        response = connection_api.get_connection(connection_id)
        if response is None:
            logger.error(f"Connection {connection_id} not found")
            return json.dumps({"error": f"Connection {connection_id} not found"}, indent=2, default=str)
        
        # get the status of the connection
        response = connection_api.get_connection_status(connection_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting connection status {connection_id}: {e}")
        return json.dumps({"error": f"Error getting connection status {connection_id}: {e}"}, indent=2, default=str)

# Publication API Functions
def list_publications(publication_api: LegacyPublicationApi) -> str:
    """List all publications for the current user.
    
    Args:
        publication_api: The Publication API instance
    """
    try:
        response = publication_api.list_publications(limit=100)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error listing publications: {e}")
        return json.dumps({"error": f"Error listing publications: {e}"}, indent=2, default=str)
    
def get_publication(publication_api: LegacyPublicationApi, publication_id: str) -> str:
    """Get a publication by ID.
    
    Args:
        publication_api: The Publication API instance
        publication_id: The ID of the publication to retrieve
    """
    if not publication_id:
        return json.dumps({"error": "publication_id is required"}, indent=2, default=str)
    
    try:
        response = publication_api.get_publication(publication_id, embed="")
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting publication {publication_id}: {e}")
        return json.dumps({"error": f"Error getting publication {publication_id}: {e}"}, indent=2, default=str)
    
def delete_publication(publication_api: LegacyPublicationApi, publication_id: str) -> str:
    """Delete a publication by ID.
    
    Args:
        publication_api: The Publication API instance
        publication_id: The ID of the publication to delete
    """
    if not publication_id:
        return json.dumps({"error": "publication_id is required"}, indent=2, default=str)
    
    try:
        # check if the publication exists
        response = publication_api.get_publication(publication_id)
        if response is None:
            logger.error(f"Publication {publication_id} not found")
            return json.dumps({"error": f"Publication {publication_id} not found"}, indent=2, default=str)
        
        response = publication_api.delete_publication(publication_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error deleting publication {publication_id}: {e}")
        return json.dumps({"error": f"Error deleting publication {publication_id}: {e}"}, indent=2, default=str)
 
 # Wrangled Dataset API Functions
def list_wrangled_datasets(wrangled_dataset_api: LegacyWrangledDatasetApi) -> str:
    """List all wrangled datasets.
    
    Args:
        wrangled_dataset_api: The Wrangled Dataset API instance
    """
    try:
        response = wrangled_dataset_api.list_wrangled_datasets()
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error listing wrangled datasets: {e}")
        return json.dumps({"error": f"Error listing wrangled datasets: {e}"}, indent=2, default=str)

def get_wrangled_dataset(wrangled_dataset_api: LegacyWrangledDatasetApi, wrangled_dataset_id: str) -> str:  
    """Get a wrangled dataset by ID.
    
    Args:
        wrangled_dataset_api: The Wrangled Dataset API instance
        wrangled_dataset_id: The ID of the wrangled dataset to retrieve
    """
    if not wrangled_dataset_id:
        return json.dumps({"error": "wrangled_dataset_id is required"}, indent=2, default=str)
    
    try:
        response = wrangled_dataset_api.get_wrangled_dataset(wrangled_dataset_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting wrangled dataset {wrangled_dataset_id}: {e}")
        return json.dumps({"error": f"Error getting wrangled dataset {wrangled_dataset_id}: {e}"}, indent=2, default=str)


def get_inputs_for_wrangled_dataset(wrangled_dataset_api: LegacyWrangledDatasetApi, wrangled_dataset_id: str) -> str:
    """Get the inputs for a wrangled dataset by ID.
    
    Args:
        wrangled_dataset_api: The Wrangled Dataset API instance
        wrangled_dataset_id: The ID of the wrangled dataset to get the inputs for
    """
    if not wrangled_dataset_id:
        return json.dumps({"error": "wrangled_dataset_id is required"}, indent=2, default=str)
    
    try:
        # check if the wrangled dataset exists
        response = wrangled_dataset_api.get_wrangled_dataset(wrangled_dataset_id)
        if response is None:
            logger.error(f"Wrangled dataset {wrangled_dataset_id} not found")
            return json.dumps({"error": f"Wrangled dataset {wrangled_dataset_id} not found"}, indent=2, default=str)
        
        # get the inputs for the wrangled dataset
        response = wrangled_dataset_api.get_inputs_for_wrangled_dataset(wrangled_dataset_id)
        result = response.to_dict() if hasattr(response, 'to_dict') else response
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting inputs for wrangled dataset {wrangled_dataset_id}: {e}")
        return json.dumps({"error": f"Error getting inputs for wrangled dataset {wrangled_dataset_id}: {e}"}, indent=2, default=str)
    