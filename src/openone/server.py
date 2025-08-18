
"""
FastMCP Server for OpenOne Analytics Platform Schedule API.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from ..client.schedule_api import ScheduleApi
from ..client.workspace_api import WorkspaceApi
from ..client.person_api import PersonApi
from ..client.plan_api import PlanApi
from ..client.api.api_client import ApiClient
from ..client.legacy_person_api import PersonApi as LegacyPersonApi
from ..client.legacy_workspace_api import WorkspaceApi as LegacyWorkspaceApi
from ..client.legacy_imported_dataset_api import ImportedDatasetApi as LegacyImportedDatasetApi
from ..client.legacy_connection_api import ConnectionApi as LegacyConnectionApi
from ..client.legacy_publication_api import PublicationApi as LegacyPublicationApi
from ..client.legacy_wrangled_dataset_api import WrangledDatasetApi as LegacyWrangledDatasetApi
from ..client.workflows_api import WorkflowsApi
from ..client.legacy_job_group_api import JobGroupApi
from ..client.configuration import Configuration
from ..client.scheduling_models import ScheduleCreateRequest, ScheduleUpdateRequest
from . import tools

logger = logging.getLogger(__name__)


class OpenOneMCPServer:
    """FastMCP Server for OpenOne Analytics Platform Schedule API."""
    
    def __init__(self):
        self.config = Configuration()
        # Create API client and all APIs
        api_client = ApiClient(self.config)
        
        # Core APIs
        self.schedule_api = ScheduleApi(api_client)
        self.workspace_api = WorkspaceApi(api_client)
        self.person_api = PersonApi(api_client)
        self.plan_api = PlanApi(api_client)
        self.workflows_api = WorkflowsApi(api_client)
        
        # Legacy APIs
        self.legacy_person_api = LegacyPersonApi(api_client)
        self.legacy_workspace_api = LegacyWorkspaceApi(api_client)
        self.legacy_imported_dataset_api = LegacyImportedDatasetApi(api_client)
        self.legacy_connection_api = LegacyConnectionApi(api_client)
        self.legacy_publication_api = LegacyPublicationApi(api_client)
        self.legacy_wrangled_dataset_api = LegacyWrangledDatasetApi(api_client)
        self.legacy_job_group_api = JobGroupApi(api_client)
        
        # Initialize FastMCP server
        self.app = FastMCP(
            name="openone",
            instructions="MCP server for OpenOne Analytics Platform Schedule API operations"
        )
        
        # Register all tools
        self._register_tools()
    
    def _initialize_client(self) -> None:
        """Initialize all API clients."""
        self.config = Configuration()
        # Create API client and all APIs
        api_client = ApiClient(self.config)
        
        # Core APIs
        self.schedule_api = ScheduleApi(api_client)
        self.workspace_api = WorkspaceApi(api_client)
        self.person_api = PersonApi(api_client)
        self.plan_api = PlanApi(api_client)
        self.workflows_api = WorkflowsApi(api_client)
        
        # Legacy APIs
        self.legacy_person_api = LegacyPersonApi(api_client)
        self.legacy_workspace_api = LegacyWorkspaceApi(api_client)
        self.legacy_imported_dataset_api = LegacyImportedDatasetApi(api_client)
        self.legacy_connection_api = LegacyConnectionApi(api_client)
        self.legacy_publication_api = LegacyPublicationApi(api_client)
        self.legacy_wrangled_dataset_api = LegacyWrangledDatasetApi(api_client)
        self.legacy_job_group_api = JobGroupApi(api_client)
    
    def _ensure_client_initialized(self) -> None:
        """Ensure the client is initialized before making API calls."""
        if self.schedule_api is None:
            self._initialize_client()
    
    def _register_tools(self) -> None:
        """Register all MCP tools."""
        
        # Schedule Management Tools
        @self.app.tool(
            name="list_schedules",
            description="List all schedules in the workspace"
        )
        def list_schedules() -> str:
            """List all schedules in the workspace."""
            self._ensure_client_initialized()
            return tools.list_schedules(self.schedule_api)
        
        @self.app.tool(
            name="get_schedule",
            description="Get details of a specific schedule by ID"
        )
        def get_schedule(schedule_id: str) -> str:
            """Get details of a specific schedule by ID.
            
            Args:
                schedule_id: The ID of the schedule to retrieve
            """
            self._ensure_client_initialized()
            return tools.get_schedule(self.schedule_api, schedule_id)
        
        # @self.app.tool(
        #     name="update_schedule",
        #     description="Update an existing schedule by ID"
        # )
        # def update_schedule(schedule_id: str, schedule_data: Dict[str, Any]) -> str:
        #     """Update an existing schedule.
            
        #     Args:
        #         schedule_id: The ID of the schedule to update
        #         schedule_data: Dictionary containing updated schedule data
        #     """
        #     self._ensure_client_initialized()
        #     return tools.update_schedule(self.schedule_api, schedule_id, schedule_data)
        
        @self.app.tool(
            name="delete_schedule",
            description="Delete a schedule by ID"
        )
        def delete_schedule(schedule_id: str) -> str:
            """Delete a schedule by ID.
            
            Args:
                schedule_id: The ID of the schedule to delete
            """
            self._ensure_client_initialized()
            return tools.delete_schedule(self.schedule_api, schedule_id)
        
        @self.app.tool(
            name="enable_schedule",
            description="Enable a schedule by ID"
        )
        def enable_schedule(schedule_id: str) -> str:
            """Enable a schedule by ID.
            
            Args:
                schedule_id: The ID of the schedule to enable
            """
            self._ensure_client_initialized()
            return tools.enable_schedule(self.schedule_api, schedule_id)
        
        @self.app.tool(
            name="disable_schedule",
            description="Disable a schedule by ID"
        )
        def disable_schedule(schedule_id: str) -> str:
            """Disable a schedule by ID.
            
            Args:
                schedule_id: The ID of the schedule to disable
            """
            self._ensure_client_initialized()
            return tools.disable_schedule(self.schedule_api, schedule_id)
        
        # Plan Management Tools
        @self.app.tool(
            name="list_plans",
            description="List all plans in the current workspace"
        )
        def list_plans() -> str:
            """List all plans in the current workspace."""
            self._ensure_client_initialized()
            return tools.list_plans(self.plan_api)
        
        @self.app.tool(
            name="get_plan",
            description="Get a plan by plan ID"
        )
        def get_plan(plan_id: str) -> str:
            """Get a plan by ID.
            
            Args:
                plan_id: The ID of the plan to retrieve
            """
            self._ensure_client_initialized()
            return tools.get_plan(self.plan_api, plan_id)
        
        @self.app.tool(
            name="delete_plan",
            description="Delete a plan by plan ID"
        )
        def delete_plan(plan_id: str) -> str:
            """Delete a plan by ID.
            
            Args:
                plan_id: The ID of the plan to delete
            """
            self._ensure_client_initialized()
            return tools.delete_plan(self.plan_api, plan_id)
        
        @self.app.tool(
            name="get_plan_schedules",
            description="Get the schedules for a plan by ID"
        )
        def get_plan_schedules(plan_id: str) -> str:
            """Get the schedules for a plan by ID."""
            self._ensure_client_initialized()
            return tools.get_plan_schedules(self.plan_api, plan_id)
        
        @self.app.tool(
            name="run_plan",
            description="Run a plan by ID"
        )
        def run_plan(plan_id: str) -> str:
            """Run a plan by ID.
            
            Args:
                plan_id: The ID of the plan to run
            """
            self._ensure_client_initialized()
            return tools.run_plan(self.plan_api, plan_id)
        
        # Workspace Management Tools
        @self.app.tool(
            name="list_workspaces",
            description="List all workspaces available to the current user"
        )
        def list_workspaces() -> str:
            """List all workspaces available to the current user.
            
            """
            self._ensure_client_initialized()
            return tools.list_workspaces(self.legacy_workspace_api)
        
        @self.app.tool(
            name="get_current_workspace",
            description="Get the current workspace that the user is in"
        )
        def get_current_workspace() -> str:
            """Get the current workspace."""
            self._ensure_client_initialized()
            return tools.get_current_workspace(self.workspace_api)
        
        @self.app.tool(
            name="get_workspace_configuration",
            description="Get workspace configuration by workspace ID"
        )
        def get_workspace_configuration(workspace_id: str) -> str:
            """Get workspace configuration.
            
            Args:
                workspace_id: The ID of the workspace to retrieve
            """
            self._ensure_client_initialized()
            return tools.get_workspace_configuration(self.workspace_api, workspace_id)
        
        @self.app.tool(
            name="list_workspace_users",
            description="List the users in a workspace by workspace ID"
        )
        def list_workspace_users(workspace_id: str) -> str:
            """List the users in a workspace.
            
            Args:
                workspace_id: The ID of the workspace to list users for
            """
            self._ensure_client_initialized()
            return tools.list_workspace_users(self.workspace_api, workspace_id)
        
        @self.app.tool(
            name="list_workspace_admins",
            description="List the admins in a workspace by workspace ID"
        )
        def list_workspace_admins(workspace_id: str) -> str:
            """List the admins in a workspace.
            
            Args:
                workspace_id: The ID of the workspace to list admins for
            """
            self._ensure_client_initialized()
            return tools.list_workspace_admins(self.person_api, self.workspace_api, workspace_id)
        
        # User Management Tools
        @self.app.tool(
            name="get_current_user",
            description="Get the current user"
        )
        def get_current_user() -> str:
            """Get the current user."""
            self._ensure_client_initialized()
            return tools.get_current_user(self.legacy_person_api)
        
        @self.app.tool(
            name="get_user",
            description="Get a user by user ID"
        )
        def get_user(user_id: str) -> str:
            """Get a user by ID.
            
            Args:
                user_id: The ID of the user to retrieve
            """
            self._ensure_client_initialized()
            return tools.get_user(self.person_api, user_id)
        
        # Dataset Management Tools
        @self.app.tool(
            name="list_datasets",
            description="List all datasets accessible to the current user"
        )
        def list_datasets() -> str:
            """List all datasets."""
            self._ensure_client_initialized()
            return tools.list_datasets(self.legacy_imported_dataset_api)
        
        @self.app.tool(
            name="get_dataset",
            description="Get a dataset by dataset ID"
        )
        def get_dataset(dataset_id: str) -> str:
            """Get a dataset by ID.
            
            Args:
                dataset_id: The ID of the dataset to retrieve
            """
            self._ensure_client_initialized()
            return tools.get_dataset(self.legacy_imported_dataset_api, dataset_id)
        
        # # Connection Management Tools
        # @self.app.tool(
        #     name="list_connections",
        #     description="List all connections accessible to the current user"
        # )
        # def list_connections() -> str:
        #     """List all connections."""
        #     self._ensure_client_initialized()
        #     return tools.list_connections(self.legacy_connection_api)
        
        # @self.app.tool(
        #     name="get_connection",
        #     description="Get a connection by ID"
        # )
        # def get_connection(connection_id: str) -> str:
        #     """Get a connection by ID.
            
        #     Args:
        #         connection_id: The ID of the connection to retrieve
        #     """
        #     self._ensure_client_initialized()
        #     return tools.get_connection(self.legacy_connection_api, connection_id)
        
        # @self.app.tool(
        #     name="get_connection_status",
        #     description="Get the status of a connection by ID"
        # )
        # def get_connection_status(connection_id: str) -> str:
        #     """Get the status of a connection by ID.
            
        #     Args:
        #         connection_id: The ID of the connection to check status for
        #     """
        #     self._ensure_client_initialized()
        #     return tools.get_connection_status(self.legacy_connection_api, connection_id)
        
        # # Publication Management Tools
        # @self.app.tool(
        #     name="list_publications",
        #     description="List all publications for the current user"
        # )
        # def list_publications() -> str:
        #     """List all publications for the current user."""
        #     self._ensure_client_initialized()
        #     return tools.list_publications(self.legacy_publication_api)
        
        # @self.app.tool(
        #     name="get_publication",
        #     description="Get a publication by ID"
        # )
        # def get_publication(publication_id: str) -> str:
        #     """Get a publication by ID.
            
        #     Args:
        #         publication_id: The ID of the publication to retrieve
        #     """
        #     self._ensure_client_initialized()
        #     return tools.get_publication(self.legacy_publication_api, publication_id)
        
        # @self.app.tool(
        #     name="delete_publication",
        #     description="Delete a publication by ID"
        # )
        # def delete_publication(publication_id: str) -> str:
        #     """Delete a publication by ID.
            
        #     Args:
        #         publication_id: The ID of the publication to delete
        #     """
        #     self._ensure_client_initialized()
        #     return tools.delete_publication(self.legacy_publication_api, publication_id)
        
        # Wrangled Dataset Management Tools
        @self.app.tool(
            name="list_wrangled_datasets",
            description="List all wrangled datasets. A wrangled dataset is a dataset that has been produced by a workflow after execution."
        )
        def list_wrangled_datasets() -> str:
            """List all wrangled datasets."""
            self._ensure_client_initialized()
            return tools.list_wrangled_datasets(self.legacy_wrangled_dataset_api)
        
        @self.app.tool(
            name="get_wrangled_dataset",
            description="Get a wrangled dataset by wrangled dataset ID"
        )
        def get_wrangled_dataset(wrangled_dataset_id: str) -> str:
            """Get a wrangled dataset by ID.
            
            Args:
                wrangled_dataset_id: The ID of the wrangled dataset to retrieve
            """
            self._ensure_client_initialized()
            return tools.get_wrangled_dataset(self.legacy_wrangled_dataset_api, wrangled_dataset_id)
        
        @self.app.tool(
            name="get_inputs_for_wrangled_dataset",
            description="Get the inputs for a wrangled dataset by wrangled dataset ID. These are the datasets that were used to produce the wrangled dataset."
        )
        def get_inputs_for_wrangled_dataset(wrangled_dataset_id: str) -> str:
            """Get the inputs for a wrangled dataset by ID.
            
            Args:
                wrangled_dataset_id: The ID of the wrangled dataset to get inputs for
            """
            self._ensure_client_initialized()
            return tools.get_inputs_for_wrangled_dataset(self.legacy_wrangled_dataset_api, wrangled_dataset_id)
        
        # Workflow Management Tools
        @self.app.tool(
            name="list_workflows",
            description="List all workflows accessible to the current user"
        )
        def list_workflows() -> str:
            """List all workflows accessible to the current user."""
            self._ensure_client_initialized()
            return tools.list_workflows(self.workflows_api)
        
        @self.app.tool(
            name="get_workflow",
            description="Get a workflow by ID"
        )
        def get_workflow(workflow_id: str) -> str:
            """Get a workflow by ID.
            
            Args:
                workflow_id: The ID of the workflow to retrieve
            """
            self._ensure_client_initialized()
            return tools.get_workflow(self.workflows_api, workflow_id)
        
        @self.app.tool(
            name="run_workflow",
            description="Run a workflow by ID"
        )
        def run_workflow(workflow_id: str) -> str:
            """Run a workflow by ID.
            
            Args:
                workflow_id: The ID of the workflow to run
            """
            self._ensure_client_initialized()
            return tools.run_workflow(self.workflows_api, workflow_id)
        
        # Job Group Management Tools
        @self.app.tool(
            name="list_job_groups",
            description="List all job groups accessible to the current user"
        )
        def list_job_groups() -> str:
            """List all job groups accessible to the current user."""
            self._ensure_client_initialized()
            return tools.list_job_groups(self.legacy_job_group_api)
        
        @self.app.tool(
            name="get_job_group",
            description="Get a job group by ID"
        )
        def get_job_group(job_id: str) -> str:
            """Get a job group by ID.
            
            Args:
                job_id: The ID of the job to retrieve
            """
            self._ensure_client_initialized()
            return tools.get_job_group(self.legacy_job_group_api, job_id)
        
        @self.app.tool(
            name="get_job_status",
            description="Get the status of a job by ID"
        )
        def get_job_status(job_id: str) -> str:
            """Get the status of a job by ID.
            
            Args:
                job_id: The ID of the job to check status for
            """
            self._ensure_client_initialized()
            return tools.get_job_status(self.legacy_job_group_api, job_id)
        
        @self.app.tool(
            name="get_job_input",
            description="Get all the input datasets of a job by ID"
        )
        def get_job_input(job_id: str) -> str:
            """Get all the input datasets of a job by ID.
            
            Args:
                job_id: The ID of the job to get inputs for
            """
            self._ensure_client_initialized()
            return tools.get_job_input(self.legacy_job_group_api, job_id)
        
        @self.app.tool(
            name="get_job_output",
            description="Get all the output datasets of a job by ID"
        )
        def get_job_output(job_id: str) -> str:
            """Get all the output datasets of a job by ID.
            
            Args:
                job_id: The ID of the job to get outputs for
            """
            self._ensure_client_initialized()
            return tools.get_job_output(self.legacy_job_group_api, job_id)

