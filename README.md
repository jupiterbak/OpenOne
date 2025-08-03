

# aac-mcp

**Unofficial MCP Server & API Client for Alteryx Analytics Cloud (AAC)**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io/)

> **⚠️ DISCLAIMER**: This is NOT an official Alteryx implementation. This project is a personal initiative and is not affiliated with, endorsed by, or supported by Alteryx or any other company.


## Overview

aac-mcp is an unofficial Model Context Protocol (MCP) server and Python API client for Alteryx Analytics Cloud (AAC). It enables seamless integration between Claude and other MCP-compatible clients with your Alteryx Analytics Cloud instance, providing programmatic access to schedules, workflows, and user management.

## Features

- **MCP-Compatible Server** - Direct integration with Claude and other MCP clients
- **Python API Client** - Full-featured client for Alteryx Analytics Cloud
- **Schedule Management** - Create, update, delete, enable/disable schedules
- **Multi-Region Support** - Works with all AAC regions


## Installation

### Prerequisites

- Python 3.10 or higher
- Alteryx Analytics Cloud account
- OAuth2 credentials (Client ID & Secret)

### Install Options

**From GitHub (Recommended)**:
```bash
pip install git+https://github.com/your-username/aac-mcp.git
```

**From source**:
```bash
git clone https://github.com/your-username/aac-mcp.git
cd aac-mcp
pip install .
```

**For development**:
```bash
git clone https://github.com/your-username/aac-mcp.git
cd aac-mcp
pip install -e .[develop]
```

### Configuration

#### Environment Variables

Set up your Alteryx Analytics Cloud credentials using environment variables:

```bash
# Required
export ALTERYX_AACP_API_BASE_URL=https://api.eu1.alteryxcloud.com
export ALTERYX_AACP_TOKEN_ENDPOINT=https://pingauth-eu1.alteryxcloud.com/as
export ALTERYX_AACP_CLIENT_ID="your_client_id_here"
export ALTERYX_AACP_PROJECT_ID="your_project_id_here"
export ALTERYX_AACP_ACCESS_TOKEN="your_access_token_here"
export ALTERYX_AACP_REFRESH_TOKEN="your_refresh_token"
# Optional
export ALTERYX_AACP_PERSISTENT_FOLDER="~/.aacp"
export ALTERYX_VERIFY_SSL=1
```

#### Configuration File

Create a `.env` file in your project root:

```env
ALTERYX_AACP_API_BASE_URL=https://api.eu1.alteryxcloud.com
ALTERYX_AACP_TOKEN_ENDPOINT=https://pingauth-eu1.alteryxcloud.com/as
ALTERYX_AACP_CLIENT_ID=your_client_id_here
ALTERYX_AACP_PROJECT_ID=your_project_id_here
ALTERYX_AACP_ACCESS_TOKEN=your_access_token_here
ALTERYX_AACP_REFRESH_TOKEN=your_refresh_token
ALTERYX_AACP_PERSISTENT_FOLDER=~/.aacp
ALTERYX_VERIFY_SSL=1
```

#### MCP Server Setup - Claude Desktop Configuration

Add the following to your Claude configuration file:

```json
{
  "mcpServers": {
    "aac-mcp": {
      "command": "python",
      "args": ["-m", "aac_mcp"],
      "env": {
        "ALTERYX_AACP_API_BASE_URL": "https://api.eu1.alteryxcloud.com",
        "ALTERYX_AACP_TOKEN_ENDPOINT": "https://pingauth-eu1.alteryxcloud.com/as",
        "ALTERYX_AACP_CLIENT_ID": "your_client_id_here",
        "ALTERYX_AACP_PROJECT_ID": "your_project_id_here",
        "ALTERYX_AACP_ACCESS_TOKEN": "your_access_token_here",
        "ALTERYX_AACP_REFRESH_TOKEN": "your_refresh_token",
        "ALTERYX_AACP_PERSISTENT_FOLDER": "~/.aacp"
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
    "aac-mcp": {
      "command": "python",
      "args": ["-m", "aac_mcp"],
      "cwd": "/path/to/your/project",
      "env": {
        "ALTERYX_AACP_CONFIG_FILE": "/path/to/your/.env"
      }
    }
  }
}
```

#### Testing the MCP Server

After configuration, restart Claude Desktop and test with these example queries:

- "List all schedules in my Alteryx Analytics Cloud instance"
- "Create a new daily schedule for my workflow"
- "Show me the status of recent workflow executions"
- "Disable the schedule with ID 12345"

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

| Category | Functionality | Description |
|----------|---------------|-------------|
| **Schedules** | Create, Read, Update, Delete | Full CRUD operations for workflow schedules |
| **Workflows** | Execute, Monitor, Manage | Run and track workflow executions |
| **Users** | Manage, Permissions | User administration and access control |
| **Jobs** | Monitor, Status | Track job execution and status |
| **Credentials** | OAuth2, Security | Secure authentication and token management |

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/your-username/aac-mcp.git
cd aac-mcp
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

## 🔗 Related Projects

- [Model Context Protocol](https://modelcontextprotocol.io/) - The MCP specification
- [Alteryx Analytics Cloud](https://www.alteryx.com/products/alteryx-analytics-cloud) - Official AAC documentation
- [Alteryx Community](https://community.alteryx.com/) - Community support and discussions


<div align="center">

**Made with ❤️ for the Alteryx Community**

[![GitHub stars](https://img.shields.io/github/stars/your-username/aac-mcp?style=social)](https://github.com/your-username/aac-mcp)
[![GitHub forks](https://img.shields.io/github/forks/your-username/aac-mcp?style=social)](https://github.com/your-username/aac-mcp)

</div>


