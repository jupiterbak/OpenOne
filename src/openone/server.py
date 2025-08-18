
"""
FastMCP Server for OpenOne Analytics Platform Schedule API.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP, Context
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
        
        # Register all resources
        self._register_resources()
    
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
        def list_schedules(ctx: Context) -> str:
            """List all schedules in the workspace."""
            self._ensure_client_initialized()
            
            # Report progress context for potentially long-running operation
            ctx.report_progress("📅 Retrieving schedules from Alteryx Analytics Platform...")

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
        def list_plans(ctx: Context) -> str:
            """List all plans in the current workspace."""
            self._ensure_client_initialized()
            
            # Report progress context for potentially long-running operation
            ctx.report_progress("🗂️ Fetching all plans from current workspace...")
            
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
            
            # Report progress context for potentially long-running operation
            self.app.request_context.report_progress(f"🚀 Executing plan {plan_id} on Alteryx Analytics Platform...")
            
            return tools.run_plan(self.plan_api, plan_id)
        
        # Workspace Management Tools
        @self.app.tool(
            name="list_workspaces",
            description="List all workspaces available to the current user"
        )
        def list_workspaces(ctx: Context) -> str:
            """List all workspaces available to the current user.
            
            """
            self._ensure_client_initialized()
            
            # Report progress context for potentially long-running operation
            ctx.report_progress("🏢 Fetching all accessible workspaces across regions...")
            
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
        def list_datasets(ctx: Context) -> str:
            """List all datasets."""
            self._ensure_client_initialized()
            
            # Report progress context for potentially long-running operation
            ctx.report_progress("📊 Loading all datasets from workspace (up to 1000 records)...")
            
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
        
        # # Wrangled Dataset Management Tools
        # @self.app.tool(
        #     name="list_wrangled_datasets",
        #     description="List all wrangled datasets. A wrangled dataset is a dataset that has been produced by a workflow after execution."
        # )
        # def list_wrangled_datasets() -> str:
        #     """List all wrangled datasets."""
        #     self._ensure_client_initialized()
            
        #     # Report progress context for potentially long-running operation
        #     self.app.request_context.report_progress("🧹 Retrieving all wrangled datasets produced by workflows...")
            
        #     return tools.list_wrangled_datasets(self.legacy_wrangled_dataset_api)
        
        # @self.app.tool(
        #     name="get_wrangled_dataset",
        #     description="Get a wrangled dataset by wrangled dataset ID"
        # )
        # def get_wrangled_dataset(wrangled_dataset_id: str) -> str:
        #     """Get a wrangled dataset by ID.
            
        #     Args:
        #         wrangled_dataset_id: The ID of the wrangled dataset to retrieve
        #     """
        #     self._ensure_client_initialized()
        #     return tools.get_wrangled_dataset(self.legacy_wrangled_dataset_api, wrangled_dataset_id)
        
        # @self.app.tool(
        #     name="get_inputs_for_wrangled_dataset",
        #     description="Get the inputs for a wrangled dataset by wrangled dataset ID. These are the datasets that were used to produce the wrangled dataset."
        # )
        # def get_inputs_for_wrangled_dataset(wrangled_dataset_id: str) -> str:
        #     """Get the inputs for a wrangled dataset by ID.
            
        #     Args:
        #         wrangled_dataset_id: The ID of the wrangled dataset to get inputs for
        #     """
        #     self._ensure_client_initialized()
        #     return tools.get_inputs_for_wrangled_dataset(self.legacy_wrangled_dataset_api, wrangled_dataset_id)
        
        # Workflow Management Tools
        @self.app.tool(
            name="list_workflows",
            description="List all workflows accessible to the current user"
        )
        def list_workflows(ctx: Context) -> str:
            """List all workflows accessible to the current user."""
            self._ensure_client_initialized()
            
            # Report progress context for potentially long-running operation
            ctx.report_progress("⚙️ Fetching all workflows from Alteryx Analytics Platform (up to 1000 records)...")
            
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
            
            # Report progress context for potentially long-running operation
            self.app.request_context.report_progress(f"⚙️ Starting workflow execution for {workflow_id} (compiler v6.21.6, engine: amp)...")
            
            return tools.run_workflow(self.workflows_api, workflow_id)
        
        # Job Group Management Tools
        @self.app.tool(
            name="list_job_groups",
            description="List all job groups accessible to the current user"
        )
        def list_job_groups(ctx: Context) -> str:
            """List all job groups accessible to the current user."""
            self._ensure_client_initialized()
            
            # Report progress context for potentially long-running operation
            ctx.report_progress("🔄 Loading all job groups and execution history (up to 1000 records)...")
            
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
            
            # Report progress context for potentially long-running operation
            self.app.request_context.report_progress(f"🔄 Retrieving input datasets for job {job_id}...")
            
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
            
            # Report progress context for potentially long-running operation
            self.app.request_context.report_progress(f"🔄 Retrieving output datasets for job {job_id}...")
            
            return tools.get_job_output(self.legacy_job_group_api, job_id)
        
        # Resource Management Tools
        @self.app.tool(
            name="list_available_resources",
            description="List all available MCP resources (datasets and workflows)"
        )
        def list_available_resources(ctx: Context) -> str:
            """List all available MCP resources."""
            self._ensure_client_initialized()
            
            # Report progress context for potentially long-running operation
            ctx.report_progress("📋 Gathering all available MCP resources...")
            
            try:
                all_resources = []
                
                # Get dataset resources
                ctx.report_progress("📊 Loading all datasets from workspace (up to 1000 records)...")
                try:
                    dataset_resources = self._list_dataset_resources()
                    all_resources.extend(dataset_resources)
                except Exception as e:
                    logger.error(f"Error getting dataset resources: {e}")
                
                # Get workflow resources
                ctx.report_progress("⚙️ Fetching all workflows from Alteryx Analytics Platform (up to 1000 records)...")
                try:
                    workflow_resources = self._list_workflow_resources()
                    all_resources.extend(workflow_resources)
                except Exception as e:
                    logger.error(f"Error getting workflow resources: {e}")
                
                # Add configuration resource
                config_resource = {
                    "uri": "config://settings",
                    "name": "Server Configuration", 
                    "description": "Current OpenOne MCP server configuration and settings",
                    "mimeType": "application/json"
                }
                all_resources.append(config_resource)
                
                resource_summary = {
                    "total_resources": len(all_resources),
                    "resource_types": {
                        "datasets": len([r for r in all_resources if r["uri"].startswith("dataset://")]),
                        "workflows": len([r for r in all_resources if r["uri"].startswith("workflow://")]),
                        "configuration": len([r for r in all_resources if r["uri"].startswith("config://")]),
                    },
                    "resources": all_resources
                }
                
                return json.dumps(resource_summary, indent=2, default=str)
                
            except Exception as e:
                logger.error(f"Error listing available resources: {e}")
                return json.dumps({"error": f"Error listing available resources: {e}"}, indent=2)

    def _register_resources(self) -> None:
        """Register all MCP resources."""
        
        # Dataset Resources
        @self.app.resource("dataset://{dataset_id}")
        def read_dataset(dataset_id: str) -> str:
            """Read a specific dataset resource."""
            self._ensure_client_initialized()
            
            try:
                # Get dataset details
                response = self.legacy_imported_dataset_api.get_imported_dataset(dataset_id)
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
                
            except Exception as e:
                logger.error(f"Error reading dataset {dataset_id}: {e}")
                return json.dumps({"error": f"Error reading dataset {dataset_id}: {e}"}, indent=2)
        
        # Register resource listing handler
        def _list_datasets_resources() -> List[Dict[str, Any]]:
            """List all available dataset resources."""
            self._ensure_client_initialized()
            
            try:
                # Get datasets from API
                response = self.legacy_imported_dataset_api.list_dataset_library(
                    datasets_filter="all", 
                    ownership_filter="all", 
                    schematized=False, 
                    limit=1000
                )
                
                # Convert to resource format
                datasets_data = response.to_dict() if hasattr(response, 'to_dict') else response
                resources = []
                
                # Extract datasets from response
                if isinstance(datasets_data, dict) and 'data' in datasets_data:
                    datasets = datasets_data['data']
                elif isinstance(datasets_data, list):
                    datasets = datasets_data
                else:
                    datasets = []
                
                for dataset in datasets:
                    if isinstance(dataset, dict):
                        dataset_id = dataset.get('id', 'unknown')
                        name = dataset.get('name', f'Dataset {dataset_id}')
                        description = dataset.get('description', 'No description available')
                        
                        resources.append({
                            "uri": f"dataset://{dataset_id}",
                            "name": name,
                            "description": description,
                            "mimeType": "application/json"
                        })
                
                return resources
                
            except Exception as e:
                logger.error(f"Error listing datasets as resources: {e}")
                return []
        
        # Store the resource lister for potential MCP use
        self._list_dataset_resources = _list_datasets_resources
        
        # Add workflow resources
        @self.app.resource("workflow://{workflow_id}")
        def read_workflow(workflow_id: str) -> str:
            """Read a specific workflow resource."""
            self._ensure_client_initialized()
            
            try:
                # Get workflow details
                response = self.workflows_api.get_workflow(workflow_id)
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
                
            except Exception as e:
                logger.error(f"Error reading workflow {workflow_id}: {e}")
                return json.dumps({"error": f"Error reading workflow {workflow_id}: {e}"}, indent=2)
        
        # Register workflow resource listing handler
        def _list_workflows_resources() -> List[Dict[str, Any]]:
            """List all available workflow resources."""
            self._ensure_client_initialized()
            
            try:
                # Get workflows from API
                response = self.workflows_api.get_workflows(limit=1000)
                
                # Convert to resource format
                workflows_data = response.to_dict() if hasattr(response, 'to_dict') else response
                resources = []
                
                # Extract workflows from response
                if isinstance(workflows_data, dict) and 'data' in workflows_data:
                    workflows = workflows_data['data']
                elif isinstance(workflows_data, list):
                    workflows = workflows_data
                else:
                    workflows = []
                
                for workflow in workflows:
                    if isinstance(workflow, dict):
                        workflow_id = workflow.get('id', 'unknown')
                        name = workflow.get('name', f'Workflow {workflow_id}')
                        description = workflow.get('description', 'No description available')
                        
                        resources.append({
                            "uri": f"workflow://{workflow_id}",
                            "name": name,
                            "description": description,
                            "mimeType": "application/json"
                        })
                
                return resources
                
            except Exception as e:
                logger.error(f"Error listing workflows as resources: {e}")
                return []
        
        # Store the workflow resource lister
        self._list_workflow_resources = _list_workflows_resources
        
        # Add configuration resource
        @self.app.resource("config://settings")
        def read_config() -> str:
            """Read the current server configuration."""
            try:
                # Get configuration details
                config_data = {
                    "server_info": {
                        "name": "openone",
                        "description": "MCP server for OpenOne Analytics Platform",
                        "version": "1.0.0"
                    },
                    "api_configuration": {
                        "api_base_url": getattr(self.config, 'host', 'Not configured'),
                        "token_endpoint": getattr(self.config, 'token_endpoint', 'Not configured'),
                        "project_id": getattr(self.config, 'project_id', 'Not configured'),
                        "verify_ssl": getattr(self.config, 'verify_ssl', True),
                        "persistent_folder": getattr(self.config, 'persitent_folder', 'Not configured'),
                    },
                    "authentication": {
                        "client_id_configured": bool(getattr(self.config, 'client_id', None)),
                        "access_token_configured": bool(getattr(self.config, 'access_token', None)),
                        "refresh_token_configured": bool(getattr(self.config, 'refresh_token', None)),
                        "token_expires_at": getattr(self.config.oauth2_handler, 'token_expires_at', None)
                    },
                    "available_apis": {
                        "schedule_api": "Available",
                        "workspace_api": "Available", 
                        "person_api": "Available",
                        "plan_api": "Available",
                        "workflows_api": "Available",
                        "legacy_person_api": "Available",
                        "legacy_workspace_api": "Available",
                        "legacy_imported_dataset_api": "Available",
                        "legacy_connection_api": "Available",
                        "legacy_publication_api": "Available",
                        "legacy_wrangled_dataset_api": "Available",
                        "legacy_job_group_api": "Available"
                    },
                    "resource_types": {
                        "datasets": "dataset://{dataset_id}",
                        "workflows": "workflow://{workflow_id}",
                        "configuration": "config://settings"
                    },
                    "tool_summary": {
                        "total_tools": 26,
                        "categories": {
                            "schedule_management": 6,
                            "plan_management": 6, 
                            "workspace_management": 5,
                            "user_management": 2,
                            "dataset_management": 2,
                            "workflow_management": 3,
                            "job_management": 5,
                            "resource_management": 1
                        }
                    }
                }
                
                return json.dumps(config_data, indent=2, default=str)
                
            except Exception as e:
                logger.error(f"Error reading configuration: {e}")
                return json.dumps({"error": f"Error reading configuration: {e}"}, indent=2)

