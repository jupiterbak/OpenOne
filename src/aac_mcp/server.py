
"""
FastMCP Server for Alteryx Analytics Cloud Schedule API.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from ..client.schedule_api import ScheduleApi
from ..client.api.api_client import ApiClient
from ..client.configuration import Configuration
from ..client.scheduling_models import ScheduleCreateRequest, ScheduleUpdateRequest

logger = logging.getLogger(__name__)


class AACMCPServer:
    """FastMCP Server for Alteryx Analytics Cloud Schedule API."""
    
    def __init__(self):
        self.config = Configuration()
        # Create API client and schedule API
        api_client = ApiClient(self.config)
        self.schedule_api = ScheduleApi(api_client)
        
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
        # Create API client and schedule API
        api_client = ApiClient(self.config)
        self.schedule_api = ScheduleApi(api_client)
    
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
            try:
                self._ensure_client_initialized()
                response = self.schedule_api.list_schedules()
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
            except Exception as e:
                logger.error(f"Error listing schedules: {e}")
                raise
        
        @self.app.tool(
            name="get_schedule",
            description="Get details of a specific schedule by ID"
        )
        def get_schedule(schedule_id: str) -> str:
            """Get details of a specific schedule by ID.
            
            Args:
                schedule_id: The ID of the schedule to retrieve
            """
            if not schedule_id:
                raise ValueError("schedule_id is required")
            
            try:
                self._ensure_client_initialized()
                response = self.schedule_api.get_schedule(schedule_id)
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
            except Exception as e:
                logger.error(f"Error getting schedule {schedule_id}: {e}")
                raise
        
        @self.app.tool(
            name="create_schedule",
            description="Create a new schedule"
        )
        def create_schedule(schedule_data: Dict[str, Any]) -> str:
            """Create a new schedule.
            
            Args:
                schedule_data: Dictionary containing schedule configuration data
            """
            if not schedule_data:
                raise ValueError("schedule_data is required")
            
            try:
                self._ensure_client_initialized()
                
                # Convert dict to ScheduleCreateRequest
                create_request = ScheduleCreateRequest()
                for key, value in schedule_data.items():
                    if hasattr(create_request, key):
                        setattr(create_request, key, value)
                
                response = self.schedule_api.create_schedule(create_request)
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
            except Exception as e:
                logger.error(f"Error creating schedule: {e}")
                raise
        
        @self.app.tool(
            name="update_schedule",
            description="Update an existing schedule"
        )
        def update_schedule(schedule_id: str, schedule_data: Dict[str, Any]) -> str:
            """Update an existing schedule.
            
            Args:
                schedule_id: The ID of the schedule to update
                schedule_data: Dictionary containing updated schedule data
            """
            if not schedule_id:
                raise ValueError("schedule_id is required")
            if not schedule_data:
                raise ValueError("schedule_data is required")
            
            try:
                self._ensure_client_initialized()
                
                # Convert dict to ScheduleUpdateRequest
                update_request = ScheduleUpdateRequest()
                for key, value in schedule_data.items():
                    if hasattr(update_request, key):
                        setattr(update_request, key, value)
                
                response = self.schedule_api.update_schedule(update_request, schedule_id)
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
            except Exception as e:
                logger.error(f"Error updating schedule {schedule_id}: {e}")
                raise
        
        @self.app.tool(
            name="delete_schedule",
            description="Delete a schedule by ID"
        )
        def delete_schedule(schedule_id: str) -> str:
            """Delete a schedule by ID.
            
            Args:
                schedule_id: The ID of the schedule to delete
            """
            if not schedule_id:
                raise ValueError("schedule_id is required")
            
            try:
                self._ensure_client_initialized()
                response = self.schedule_api.delete_schedule(schedule_id)
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
            except Exception as e:
                logger.error(f"Error deleting schedule {schedule_id}: {e}")
                raise
        
        @self.app.tool(
            name="enable_schedule",
            description="Enable a schedule by ID"
        )
        def enable_schedule(schedule_id: str) -> str:
            """Enable a schedule by ID.
            
            Args:
                schedule_id: The ID of the schedule to enable
            """
            if not schedule_id:
                raise ValueError("schedule_id is required")
            
            try:
                self._ensure_client_initialized()
                response = self.schedule_api.enable_schedule(schedule_id)
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
            except Exception as e:
                logger.error(f"Error enabling schedule {schedule_id}: {e}")
                raise
        
        @self.app.tool(
            name="disable_schedule",
            description="Disable a schedule by ID"
        )
        def disable_schedule(schedule_id: str) -> str:
            """Disable a schedule by ID.
            
            Args:
                schedule_id: The ID of the schedule to disable
            """
            if not schedule_id:
                raise ValueError("schedule_id is required")
            
            try:
                self._ensure_client_initialized()
                response = self.schedule_api.disable_schedule(schedule_id)
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
            except Exception as e:
                logger.error(f"Error disabling schedule {schedule_id}: {e}")
                raise
        
        @self.app.tool(
            name="count_schedules",
            description="Get the count of schedules in the workspace"
        )
        def count_schedules() -> str:
            """Get the count of schedules in the workspace."""
            try:
                self._ensure_client_initialized()
                response = self.schedule_api.count_schedules()
                result = response.to_dict() if hasattr(response, 'to_dict') else response
                return json.dumps(result, indent=2, default=str)
            except Exception as e:
                logger.error(f"Error counting schedules: {e}")
                raise
