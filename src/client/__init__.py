# coding: utf-8

# flake8: noqa

"""
    Scheduling (Alpha)

    No description provided (generated API client)  # noqa: E501

    OpenAPI spec version: v2024.14.0
    
    Generated API client
"""

from __future__ import absolute_import

# import apis into sdk package
from src.client.schedule_api import ScheduleApi
from src.client.plan_api import PlanApi
from src.client.plan_edge_api import PlanEdgeApi
from src.client.plan_node_api import PlanNodeApi
from src.client.plan_override_api import PlanOverrideApi
from src.client.plan_snapshot_run_api import PlanSnapshotRunApi
from src.client.person_api import PersonApi
from src.client.workspace_api import WorkspaceApi
from src.client.api.api_client import ApiClient
from src.client.configuration import Configuration

# Legacy APIs - Account and Authentication
from src.client.legacy_account_api import AccountApi as LegacyAccountApi
from src.client.legacy_api_access_token_api import ApiAccessTokenApi as LegacyApiAccessTokenApi
from src.client.legacy_authorization_api import AuthorizationApi as LegacyAuthorizationApi
from src.client.legacy_o_auth2_api_token_api import OAuth2ApiTokenApi as LegacyOAuth2ApiTokenApi

# Legacy APIs - AWS and Cloud Configuration
from src.client.legacy_aws_config_api import AwsConfigApi as LegacyAwsConfigApi
from src.client.legacy_aws_role_api import AwsRoleApi as LegacyAwsRoleApi
from src.client.legacy_base_storage_config_api import BaseStorageConfigApi as LegacyBaseStorageConfigApi
from src.client.legacy_cloud_config_api import CloudConfigApi as LegacyCloudConfigApi

# Legacy APIs - Connections and Permissions
from src.client.legacy_connection_api import ConnectionApi as LegacyConnectionApi
from src.client.legacy_connection_permission_api import ConnectionPermissionApi as LegacyConnectionPermissionApi
from src.client.legacy_connector_metadata_api import ConnectorMetadataApi as LegacyConnectorMetadataApi

# Legacy APIs - Environment and Parameters
from src.client.legacy_environment_parameter_api import EnvironmentParameterApi as LegacyEnvironmentParameterApi

# Legacy APIs - Flows and Flow Management
from src.client.legacy_flow_api import FlowApi as LegacyFlowApi
from src.client.legacy_flow_node_api import FlowNodeApi as LegacyFlowNodeApi
from src.client.legacy_flow_notification_settings_api import FlowNotificationSettingsApi as LegacyFlowNotificationSettingsApi
from src.client.legacy_flow_permission_api import FlowPermissionApi as LegacyFlowPermissionApi
from src.client.legacy_flow_run_api import FlowRunApi as LegacyFlowRunApi
from src.client.legacy_flow_run_parameter_override_api import FlowRunParameterOverrideApi as LegacyFlowRunParameterOverrideApi

# Legacy APIs - Folders and Organization
from src.client.legacy_folder_api import FolderApi as LegacyFolderApi

# Legacy APIs - Datasets and Data Management
from src.client.legacy_imported_dataset_api import ImportedDatasetApi as LegacyImportedDatasetApi
from src.client.legacy_wrangled_dataset_api import WrangledDatasetApi as LegacyWrangledDatasetApi

# Legacy APIs - Jobs and Job Management
from src.client.legacy_job_api import JobApi as LegacyJobApi
from src.client.legacy_job_group_api import JobGroupApi as LegacyJobGroupApi

# Legacy APIs - Macros and Scripts
from src.client.legacy_macro_api import MacroApi as LegacyMacroApi
from src.client.legacy_sql_script_api import SqlScriptApi as LegacySqlScriptApi

# Legacy APIs - Miscellaneous
from src.client.legacy_misc_api import MiscApi as LegacyMiscApi

# Legacy APIs - Output and Publication
from src.client.legacy_output_object_api import OutputObjectApi as LegacyOutputObjectApi
from src.client.legacy_publication_api import PublicationApi as LegacyPublicationApi

# Legacy APIs - Plans and Planning
from src.client.legacy_plan_api import PlanApi as LegacyPlanApi
from src.client.legacy_plan_edge_api import PlanEdgeApi as LegacyPlanEdgeApi
from src.client.legacy_plan_node_api import PlanNodeApi as LegacyPlanNodeApi
from src.client.legacy_plan_override_api import PlanOverrideApi as LegacyPlanOverrideApi
from src.client.legacy_plan_snapshot_run_api import PlanSnapshotRunApi as LegacyPlanSnapshotRunApi

# Legacy APIs - Scheduling
from src.client.legacy_schedule_api import ScheduleApi as LegacyScheduleApi

# Legacy APIs - Webhooks and Tasks
from src.client.legacy_webhook_flow_task_api import WebhookFlowTaskApi as LegacyWebhookFlowTaskApi

# Legacy APIs - Workspace and Write Settings
from src.client.legacy_workspace_api import WorkspaceApi as LegacyWorkspaceApi
from src.client.legacy_write_setting_api import WriteSettingApi as LegacyWriteSettingApi

# Legacy APIs - Person and User Management
from src.client.legacy_person_api import PersonApi as LegacyPersonApi

# Import legacy models
from src.client.legacy_models import *

# Import IAM models
from src.client.iam_models import *

# Import plan models
from src.client.plan_models import *

# import scheduling models into sdk package
from src.client.scheduling_models import *
