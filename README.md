

# OpenOne

**Unofficial MCP Server & API Client for Alteryx Analytics Platform**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io/)

> **⚠️ DISCLAIMER**: This is NOT an official implementation. This project is a personal initiative and is not affiliated with, endorsed by, or supported by any company.


## Overview

OpenOne is an unofficial Model Context Protocol (MCP) server and Python API client for Alteryx Analytics Platform. It enables seamless integration between Claude and other MCP-compatible clients with your Alteryx Analytics Platform instance, providing programmatic access to schedules, datasets, plans and user management.

### 🚀 Quick Stats
- **25 MCP Tools** across 8 functional categories
- **Complete API Coverage** for all core Alteryx APIs including legacy APIs  
- **Production Ready** with comprehensive error handling
- **Real-time Integration** with Claude Desktop

## Features

- **🔗 MCP-Compatible Server** - Direct integration with Claude and other MCP clients
- **🐍 Python API Client** - Full-featured client for Alteryx Analytics Platform
  - **📅 Schedule Management** - Complete CRUD operations for workflow schedules
  - **🗂️ Plan Management** - Create, run, and manage execution plans
  - **🏢 Workspace Management** - Multi-workspace support and user administration
  - **📊 Dataset Management** - Access imported and wrangled datasets
  - **⚙️ Workflow Management** - List, get, and run workflows
  - **🔄 Job Management** - Monitor job execution and retrieve inputs/outputs
  - **👥 User Management** - User profiles and permission management
  - **🌍 Multi-Region Support** - Works with all regions worldwide
- **🔄 Real-time Operations** - Live status monitoring and execution tracking

## Installation

### Prerequisites

- Python 3.10 or higher
- Alteryx Analytics Cloud Platform account
- OAuth2 credentials (Client ID, initial Access Token & Refresh Token)

### Install Options

**From GitHub (Recommended)**:
```bash
git clone https://github.com/jupiterbak/OpenOne.git
cd OpenOne
pip install .
```

### Configuration

#### Environment Variables

Set up your OpenOne Analytics Platform credentials using environment variables:

```bash
# Required
export OPENONE_API_BASE_URL="https://api.eu1.alteryxcloud.com"
export OPENONE_TOKEN_ENDPOINT="https://pingauth-eu1.alteryxcloud.com/as"
export OPENONE_CLIENT_ID="your_client_id_here"
export OPENONE_PROJECT_ID="your_project_id_here"
export OPENONE_ACCESS_TOKEN="your_access_token_here"
export OPENONE_REFRESH_TOKEN="your_refresh_token"
# Optional
export OPENONE_PERSISTENT_FOLDER="~/.openone"
export OPENONE_VERIFY_SSL=1
```

#### Configuration File

Create a `.env` file in your project root:

```env
OPENONE_API_BASE_URL=https://api.eu1.alteryxcloud.com
OPENONE_TOKEN_ENDPOINT=https://pingauth-eu1.alteryxcloud.com/as
OPENONE_CLIENT_ID=your_client_id_here
OPENONE_PROJECT_ID=your_project_id_here
OPENONE_ACCESS_TOKEN=your_access_token_here
OPENONE_REFRESH_TOKEN=your_refresh_token
OPENONE_PERSISTENT_FOLDER=~/.openone
OPENONE_VERIFY_SSL=1
```

#### MCP Server Setup - Claude Desktop Configuration

Add the following to your Claude configuration file:

```json
{
  "mcpServers": {
    "openone": {
      "command": "python",
      "args": ["-m", "openone"],
      "env": {
        "OPENONE_API_BASE_URL": "https://api.eu1.alteryxcloud.com",
        "OPENONE_TOKEN_ENDPOINT": "https://pingauth-eu1.alteryxcloud.com/as",
        "OPENONE_CLIENT_ID": "your_client_id_here",
        "OPENONE_PROJECT_ID": "your_project_id_here",
        "OPENONE_ACCESS_TOKEN": "your_access_token_here",
        "OPENONE_REFRESH_TOKEN": "your_refresh_token",
        "OPENONE_PERSISTENT_FOLDER": "~/.openone"
      }
    }
  }
}
```

Alternative: Using a Configuration File

Instead of setting environment variables in the Claude config, you can create a `.env` file and reference it:

```json
{
  "mcpServers": {
    "openone": {
      "command": "python",
      "args": ["-m", "openone"],
      "cwd": "/path/to/your/project",
      "env": {
        "OPENONE_CONFIG_FILE": "/path/to/your/.env"
      }
    }
  }
}
```

#### Testing the MCP Server

After configuration, restart Claude Desktop and test with these example queries:

**Basic Operations:**
- "List all schedules in my OpenOne Analytics Platform instance"
- "Show me my current workspace details and user count"
- "Get a count of all my plans and datasets"

**Schedule Management:**
- "Disable the schedule with ID 12345 and tell me why"
- "Show me all enabled schedules and their next run times"
- "Delete all schedules that haven't run in the last 30 days"

**Data Operations:**
- "List all my datasets and show their connection status"
- "Check if my database connections are working properly"
- "Show me all wrangled datasets and their input sources"

**Advanced Queries:**
- "Run plan abc123 and monitor its execution status"
- "Show me all workspace admins and their permissions"
- "List my publications and delete any older than 6 months"

### API Client Usage

### Basic Usage

```python
import client
from client.rest import ApiException
from pprint import pprint

# Configure the client
configuration = client.Configuration()
api_instance = client.ScheduleApi(client.ApiClient(configuration))

try:
    # List all schedules
    schedules = api_instance.list_schedules()
    print(f"Found {len(schedules)} schedules")
    
    # Get a specific schedule
    schedule = api_instance.get_schedule(schedule_id="12345")
    pprint(schedule)
    
except ApiException as e:
    print(f"API Error: {e}")
```

## MCP Available Tools

The MCP server provides comprehensive access to Alteryx Analytics Cloud through organized tool categories:

### 📅 Schedule Management Tools
| Tool | Description | Parameters |
|------|-------------|-------------|
| `list_schedules` | List all schedules in the workspace | None |
| `get_schedule` | Get details of a specific schedule | `schedule_id` |
| `delete_schedule` | Delete a schedule by ID | `schedule_id` |
| `enable_schedule` | Enable a schedule by ID | `schedule_id` |
| `disable_schedule` | Disable a schedule by ID | `schedule_id` |
| `count_schedules` | Get the count of schedules in workspace | None |

### 🗂️ Plan Management Tools
| Tool | Description | Parameters |
|------|-------------|-------------|
| `list_plans` | List all plans in current workspace | None |
| `get_plan` | Get a plan by plan ID | `plan_id` |
| `delete_plan` | Delete a plan by plan ID | `plan_id` |
| `get_plan_schedules` | Get schedules for a plan by plan ID | `plan_id` |
| `run_plan` | Run a plan by plan ID | `plan_id` |
| `count_plans` | Get the count of plans in workspace | None |

### 🏢 Workspace Management Tools
| Tool | Description | Parameters |
|------|-------------|-------------|
| `list_workspaces` | List all available workspaces | None |
| `get_current_workspace` | Get current workspace that user is in | None |
| `get_workspace_configuration` | Get workspace configuration by workspace ID | `workspace_id` |
| `list_workspace_users` | List users in a workspace by workspace ID | `workspace_id` |
| `list_workspace_admins` | List admins in a workspace by workspace ID | `workspace_id` |

### 👥 User Management Tools
| Tool | Description | Parameters |
|------|-------------|-------------|
| `get_current_user` | Get current user information | None |
| `get_user` | Get user details by user ID | `user_id` |

### 📊 Dataset Management Tools
| Tool | Description | Parameters |
|------|-------------|-------------|
| `list_datasets` | List all datasets accessible to current user | None |
| `get_dataset` | Get dataset details by dataset ID | `dataset_id` |

### 🧹 Wrangled Dataset Management Tools
| Tool | Description | Parameters |
|------|-------------|-------------|
| `list_wrangled_datasets` | List all wrangled datasets (produced by workflows) | None |
| `get_wrangled_dataset` | Get wrangled dataset by wrangled dataset ID | `wrangled_dataset_id` |
| `get_inputs_for_wrangled_dataset` | Get input datasets for wrangled dataset by wrangled dataset ID | `wrangled_dataset_id` |

### ⚙️ Workflow Management Tools
| Tool | Description | Parameters |
|------|-------------|-------------|
| `list_workflows` | List all workflows accessible to current user | None |
| `get_workflow` | Get workflow details by workflow ID | `workflow_id` |
| `run_workflow` | Run a workflow by workflow ID | `workflow_id` |

### 🔄 Job Management Tools
| Tool | Description | Parameters |
|------|-------------|-------------|
| `list_job_groups` | List all job groups accessible to current user | None |
| `get_job_group` | Get job group details by job ID | `job_id` |
| `get_job_status` | Get status of a job by job ID | `job_id` |
| `get_job_input` | Get all input datasets of a job by job ID | `job_id` |
| `get_job_output` | Get all output datasets of a job by job ID | `job_id` |

### Example Usage with Claude

Here are some example queries you can use with Claude once the MCP server is configured:

**Schedule Management:**
- "List all my schedules and show me which ones are currently enabled"
- "Get details for schedule ID 12345 and tell me when it last ran"
- "Disable the schedule with ID 67890 temporarily"
- "Delete the schedule named 'old-workflow-schedule'"

**Plan Management:**
- "Show me all my plans and their current status"
- "Run the plan with ID abc123 and monitor its progress"
- "Get the schedules associated with my data processing plan"

**Workspace & User Management:**
- "List all workspaces I have access to"
- "Show me all users in workspace ws-456 and their roles"
- "Get my current user profile and permissions"

**Data Management:**
- "List all my datasets and show their sizes"
- "Show me all my wrangled datasets and their input sources"
- "Get details about dataset ds-456 and its metadata"

**Workflows & Jobs:**
- "List all my workflows and show which ones are active"
- "Run workflow wf-789 and monitor its execution"
- "Show me all job groups and their current status"
- "Get the input and output datasets for job job-123"

### 🔢 Tool Summary

| Category | Tool Count | Key Operations |
|----------|------------|----------------|
| **Schedule Management** | 6 tools | List, Get, Delete, Enable, Disable, Count |
| **Plan Management** | 6 tools | List, Get, Delete, Run, Get Schedules, Count |
| **Workspace Management** | 5 tools | List, Get Current, Get Config, List Users/Admins |
| **User Management** | 2 tools | Get Current User, Get User by ID |
| **Dataset Management** | 2 tools | List, Get by ID |
| **Wrangled Dataset Management** | 3 tools | List, Get, Get Inputs |
| **Workflow Management** | 3 tools | List, Get, Run |
| **Job Management** | 5 tools | List, Get, Status, Get Inputs/Outputs |
| **Total** | **25 tools** | Complete Alteryx Platform integration |

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/jupiterbak/OpenOne.git
cd OpenOne
pip install -e .[develop]
pytest  # Run tests
```

### Code Style

- Follow PEP 8 guidelines
- Add type hints where appropriate
- Include docstrings for all functions
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">

**Made with ❤️ for the Alteryx Community**

[![GitHub stars](https://img.shields.io/github/stars/jupiterbak/OpenOne?style=social)](https://github.com/jupiterbak/OpenOne)
[![GitHub forks](https://img.shields.io/github/forks/jupiterbak/OpenOne?style=social)](https://github.com/jupiterbak/OpenOne)

</div>


