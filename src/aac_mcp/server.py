
"""
FastMCP Server for Alteryx Analytics Cloud Schedule API.
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
from ..client.configuration import Configuration
from ..client.scheduling_models import ScheduleCreateRequest, ScheduleUpdateRequest
from . import tools

logger = logging.getLogger(__name__)


class AACMCPServer:
    """FastMCP Server for Alteryx Analytics Cloud Schedule API."""
    
    def __init__(self):
        self.config = Configuration()
        # Create API client and schedule API
        api_client = ApiClient(self.config)
        self.schedule_api = ScheduleApi(api_client)
        self.workspace_api = WorkspaceApi(api_client)
        self.person_api = PersonApi(api_client)
        self.plan_api = PlanApi(api_client)
        
        # Initialize FastMCP server
        self.app = FastMCP(
            name="aac-mcp",
            instructions="MCP server for Alteryx Analytics Cloud Schedule API operations"
        )
        
        # Register all tools
        self._register_tools()
    
    def _initialize_client(self) -> None:
        """Initialize the Schedule API client."""
        self.config = Configuration()
        # Create API client and all APIs
        api_client = ApiClient(self.config)
        self.schedule_api = ScheduleApi(api_client)
        self.workspace_api = WorkspaceApi(api_client)
        self.person_api = PersonApi(api_client)
        self.plan_api = PlanApi(api_client)
    
    def _ensure_client_initialized(self) -> None:
        """Ensure the client is initialized before making API calls."""
        if self.schedule_api is None:
            self._initialize_client()
    
    def _register_tools(self) -> None:
        """Register all MCP tools."""
        
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
        
        @self.app.tool(
            name="update_schedule",
            description="Update an existing schedule by ID"
        )
        def update_schedule(schedule_id: str, schedule_data: Dict[str, Any]) -> str:
            """Update an existing schedule.
            
            Args:
                schedule_id: The ID of the schedule to update
                schedule_data: Dictionary containing updated schedule data
            """
            self._ensure_client_initialized()
            return tools.update_schedule(self.schedule_api, schedule_id, schedule_data)
        
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
        
        @self.app.tool(
            name="count_schedules",
            description="Get the count of schedules in the workspace"
        )
        def count_schedules() -> str:
            """Get the count of schedules in the workspace."""
            self._ensure_client_initialized()
            return tools.count_schedules(self.schedule_api)
        
        @self.app.tool(
            name="get_current_workspace",
            description="Get the current workspace"
        )
        def get_current_workspace() -> str:
            """Get the current workspace."""
            self._ensure_client_initialized()
            return tools.get_current_workspace(self.workspace_api)
        
        @self.app.tool(
            name="get_workspace_configuration",
            description="Get workspace configuration by ID"
        )
        def get_workspace_configuration(workspace_id: str) -> str:
            """Get workspace configuration.
            
            Args:
                workspace_id: The ID of the workspace
            """
            self._ensure_client_initialized()
            return tools.get_workspace_configuration(self.workspace_api, workspace_id)
        
        @self.app.tool(
            name="list_workspace_users",
            description="List the users in a workspace"
        )
        def list_workspace_users(workspace_id: str) -> str:
            """List the users in a workspace.
            """
            self._ensure_client_initialized()
            return tools.list_workspace_users(self.workspace_api, workspace_id)
        
        @self.app.tool(
            name="list_workspace_admins",
            description="List the admins in a workspace"
        )
        def list_workspace_admins(workspace_id: str) -> str:
            """List the admins in a workspace.
            
            """
            self._ensure_client_initialized()
            return tools.list_workspace_admins(self.person_api, self.workspace_api, workspace_id)

        @self.app.tool(
            name="get_user",
            description="Get a user by ID"
        )
        def get_user(user_id: str) -> str:
            """Get a user by ID.
            
            Args:
                user_id: The ID of the user
            """
            self._ensure_client_initialized()
            return tools.get_user(self.person_api, user_id)
        
        @self.app.tool(
            name="count_plans",
            description="Get the count of plans in the current workspace"
        )
        def count_plans() -> str:
            """Get the count of plans in the current workspace."""
            self._ensure_client_initialized()
            return tools.count_plans(self.plan_api)
        
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
            description="Get a plan by ID"
        )
        def get_plan(plan_id: str) -> str:
            """Get a plan by ID.
            
            Args:
                plan_id: The ID of the plan
            """
            self._ensure_client_initialized()
            return tools.get_plan(self.plan_api, plan_id)
        
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

