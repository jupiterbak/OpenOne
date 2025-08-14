# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from src.client.api.api_client import ApiClient


class WorkspaceApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
     
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_users_to_group(self, user_ids, id, group_id, **kwargs):  # noqa: E501
        """Add users to group in workspace  # noqa: E501

        Add users to group in workspace.  <small>ref: [addUsersToGroup](#operation/addUsersToGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_users_to_group(user_ids, id, group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[str] user_ids: IDs of users to add to group (required)
        :param int id: (required)
        :param str group_id: (required)
        :param object body:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.add_users_to_group_with_http_info(user_ids, id, group_id, **kwargs)  # noqa: E501
        else:
            (data) = self.add_users_to_group_with_http_info(user_ids, id, group_id, **kwargs)  # noqa: E501
            return data

    def add_users_to_group_with_http_info(self, user_ids, id, group_id, **kwargs):  # noqa: E501
        """Add users to group in workspace  # noqa: E501

        Add users to group in workspace.  <small>ref: [addUsersToGroup](#operation/addUsersToGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_users_to_group_with_http_info(user_ids, id, group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[str] user_ids: IDs of users to add to group (required)
        :param int id: (required)
        :param str group_id: (required)
        :param object body:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['user_ids', 'id', 'group_id', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_users_to_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'user_ids' is set
        if ('user_ids' not in params or
                params['user_ids'] is None):
            raise ValueError("Missing the required parameter `user_ids` when calling `add_users_to_group`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `add_users_to_group`")  # noqa: E501
        # verify the required parameter 'group_id' is set
        if ('group_id' not in params or
                params['group_id'] is None):
            raise ValueError("Missing the required parameter `group_id` when calling `add_users_to_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'group_id' in params:
            path_params['groupId'] = params['group_id']  # noqa: E501

        query_params = []
        if 'user_ids' in params:
            query_params.append(('userIds', params['user_ids']))  # noqa: E501
            collection_formats['userIds'] = 'multi'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/groups/:groupId/users', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_workspace(self, body, **kwargs):  # noqa: E501
        """Create workspace  # noqa: E501

        Create a new workspace  <small>ref: [createWorkspace](#operation/createWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_workspace(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param WorkspaceCreateRequest body: (required)
        :param str account_id: accountId associated with the workspace - required for account admin access
        :return: Workspace
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_workspace_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_workspace_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_workspace_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create workspace  # noqa: E501

        Create a new workspace  <small>ref: [createWorkspace](#operation/createWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_workspace_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param WorkspaceCreateRequest body: (required)
        :param str account_id: accountId associated with the workspace - required for account admin access
        :return: Workspace
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_workspace`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LWorkspace',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_workspace_group(self, body, id, **kwargs):  # noqa: E501
        """Create group in workspace  # noqa: E501

        Create group in workspace. Add group members. Assign roles.  <small>ref: [createWorkspaceGroup](#operation/createWorkspaceGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_workspace_group(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateGroupPayload body: (required)
        :param int id: (required)
        :return: CreateGroupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_workspace_group_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.create_workspace_group_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def create_workspace_group_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Create group in workspace  # noqa: E501

        Create group in workspace. Add group members. Assign roles.  <small>ref: [createWorkspaceGroup](#operation/createWorkspaceGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_workspace_group_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateGroupPayload body: (required)
        :param int id: (required)
        :return: CreateGroupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_workspace_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_workspace_group`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `create_workspace_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/groups', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LCreateGroupResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_current_workspace_configuration_settings(self, body, **kwargs):  # noqa: E501
        """Reset a configuration settings for the current workspace  # noqa: E501

        Delete Workspace configuration settings override (reset the settings to their initial values).  <small>ref: [deleteCurrentWorkspaceConfigurationSettings](#operation/deleteCurrentWorkspaceConfigurationSettings)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_current_workspace_configuration_settings(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteSettingsRequest body: (required)
        :return: DeleteSettingsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_current_workspace_configuration_settings_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_current_workspace_configuration_settings_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def delete_current_workspace_configuration_settings_with_http_info(self, body, **kwargs):  # noqa: E501
        """Reset a configuration settings for the current workspace  # noqa: E501

        Delete Workspace configuration settings override (reset the settings to their initial values).  <small>ref: [deleteCurrentWorkspaceConfigurationSettings](#operation/deleteCurrentWorkspaceConfigurationSettings)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_current_workspace_configuration_settings_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteSettingsRequest body: (required)
        :return: DeleteSettingsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_current_workspace_configuration_settings" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `delete_current_workspace_configuration_settings`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/current/delete-configuration', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LDeleteSettingsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_group(self, id, group_id, **kwargs):  # noqa: E501
        """Delete group from workspace  # noqa: E501

        Delete group from workspace.  <small>ref: [deleteGroup](#operation/deleteGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_group(id, group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str group_id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_group_with_http_info(id, group_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_group_with_http_info(id, group_id, **kwargs)  # noqa: E501
            return data

    def delete_group_with_http_info(self, id, group_id, **kwargs):  # noqa: E501
        """Delete group from workspace  # noqa: E501

        Delete group from workspace.  <small>ref: [deleteGroup](#operation/deleteGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_group_with_http_info(id, group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str group_id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'group_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_group`")  # noqa: E501
        # verify the required parameter 'group_id' is set
        if ('group_id' not in params or
                params['group_id'] is None):
            raise ValueError("Missing the required parameter `group_id` when calling `delete_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'group_id' in params:
            path_params['groupId'] = params['group_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/groups/:groupId', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_workspace_configuration_settings(self, body, id, **kwargs):  # noqa: E501
        """Reset a workspace configuration settings  # noqa: E501

        Delete Workspace configuration settings override (reset the settings to their initial values).  <small>ref: [deleteWorkspaceConfigurationSettings](#operation/deleteWorkspaceConfigurationSettings)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_workspace_configuration_settings(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteSettingsRequest body: (required)
        :param int id: (required)
        :return: DeleteSettingsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_workspace_configuration_settings_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_workspace_configuration_settings_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def delete_workspace_configuration_settings_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Reset a workspace configuration settings  # noqa: E501

        Delete Workspace configuration settings override (reset the settings to their initial values).  <small>ref: [deleteWorkspaceConfigurationSettings](#operation/deleteWorkspaceConfigurationSettings)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_workspace_configuration_settings_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteSettingsRequest body: (required)
        :param int id: (required)
        :return: DeleteSettingsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_workspace_configuration_settings" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `delete_workspace_configuration_settings`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_workspace_configuration_settings`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/delete-configuration', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LDeleteSettingsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_workspace_user(self, person_id, id, **kwargs):  # noqa: E501
        """Remove a user from a workspace  # noqa: E501

        Remove a user from a workspace. This endpoint removes the user's membership from the workspace but does not delete the user altogether. Before using this endpoint, use `transferUserAssetsInWorkspace` endpoint to transfer existing objects of that person to another person.  <small>ref: [deleteWorkspaceUser](#operation/deleteWorkspaceUser)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_workspace_user(person_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int person_id: (required)
        :param int id: (required)
        :return: DeleteWorkspaceUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_workspace_user_with_http_info(person_id, id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_workspace_user_with_http_info(person_id, id, **kwargs)  # noqa: E501
            return data

    def delete_workspace_user_with_http_info(self, person_id, id, **kwargs):  # noqa: E501
        """Remove a user from a workspace  # noqa: E501

        Remove a user from a workspace. This endpoint removes the user's membership from the workspace but does not delete the user altogether. Before using this endpoint, use `transferUserAssetsInWorkspace` endpoint to transfer existing objects of that person to another person.  <small>ref: [deleteWorkspaceUser](#operation/deleteWorkspaceUser)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_workspace_user_with_http_info(person_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int person_id: (required)
        :param int id: (required)
        :return: DeleteWorkspaceUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['person_id', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_workspace_user" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'person_id' is set
        if ('person_id' not in params or
                params['person_id'] is None):
            raise ValueError("Missing the required parameter `person_id` when calling `delete_workspace_user`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_workspace_user`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'person_id' in params:
            path_params['personId'] = params['person_id']  # noqa: E501
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/people/{personId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LDeleteWorkspaceUserResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_configuration_for_workspace(self, id, **kwargs):  # noqa: E501
        """Get workspace configuration  # noqa: E501

        Get workspace configuration. Settings set to null use the default configuration.  It is possible to filter the configuration to a specific key using the query parameter `key`: ``` /v4/workspaces/:id/configuration?key=outputFormats.JSON [{ \"key\": \"outputFormats.JSON\", \"value\": true }] ```  <small>ref: [getConfigurationForWorkspace](#operation/getConfigurationForWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_configuration_for_workspace(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str key:
        :return: GenericJsonResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_configuration_for_workspace_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_configuration_for_workspace_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_configuration_for_workspace_with_http_info(self, id, **kwargs):  # noqa: E501
        """Get workspace configuration  # noqa: E501

        Get workspace configuration. Settings set to null use the default configuration.  It is possible to filter the configuration to a specific key using the query parameter `key`: ``` /v4/workspaces/:id/configuration?key=outputFormats.JSON [{ \"key\": \"outputFormats.JSON\", \"value\": true }] ```  <small>ref: [getConfigurationForWorkspace](#operation/getConfigurationForWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_configuration_for_workspace_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str key:
        :return: GenericJsonResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_configuration_for_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_configuration_for_workspace`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'key' in params:
            query_params.append(('key', params['key']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/configuration', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LGenericJsonResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_configuration_schema(self, id, **kwargs):  # noqa: E501
        """Get configuration schema  # noqa: E501

        Get configuration schema for the specified workspace.  <small>ref: [getConfigurationSchema](#operation/getConfigurationSchema)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_configuration_schema(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: ConfigurationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_configuration_schema_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_configuration_schema_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_configuration_schema_with_http_info(self, id, **kwargs):  # noqa: E501
        """Get configuration schema  # noqa: E501

        Get configuration schema for the specified workspace.  <small>ref: [getConfigurationSchema](#operation/getConfigurationSchema)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_configuration_schema_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: ConfigurationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_configuration_schema" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_configuration_schema`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/configuration-schema', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LConfigurationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_current_configuration_for_workspace(self, **kwargs):  # noqa: E501
        """Get current workspace configuration  # noqa: E501

        Get workspace configuration. Settings set to null use the default configuration.  It is possible to filter the configuration to a specific key using the query parameter `key`: ``` /v4/workspaces/:id/configuration?key=outputFormats.JSON [{ \"key\": \"outputFormats.JSON\", \"value\": true }] ```  <small>ref: [getCurrentConfigurationForWorkspace](#operation/getCurrentConfigurationForWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_current_configuration_for_workspace(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str key:
        :return: GenericJsonResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_current_configuration_for_workspace_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_current_configuration_for_workspace_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_current_configuration_for_workspace_with_http_info(self, **kwargs):  # noqa: E501
        """Get current workspace configuration  # noqa: E501

        Get workspace configuration. Settings set to null use the default configuration.  It is possible to filter the configuration to a specific key using the query parameter `key`: ``` /v4/workspaces/:id/configuration?key=outputFormats.JSON [{ \"key\": \"outputFormats.JSON\", \"value\": true }] ```  <small>ref: [getCurrentConfigurationForWorkspace](#operation/getCurrentConfigurationForWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_current_configuration_for_workspace_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str key:
        :return: GenericJsonResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_current_configuration_for_workspace" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'key' in params:
            query_params.append(('key', params['key']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/current/configuration', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LGenericJsonResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_current_configuration_schema(self, **kwargs):  # noqa: E501
        """Get current configuration schema  # noqa: E501

        Get configuration schema for the current workspace.  <small>ref: [getCurrentConfigurationSchema](#operation/getCurrentConfigurationSchema)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_current_configuration_schema(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: ConfigurationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_current_configuration_schema_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_current_configuration_schema_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_current_configuration_schema_with_http_info(self, **kwargs):  # noqa: E501
        """Get current configuration schema  # noqa: E501

        Get configuration schema for the current workspace.  <small>ref: [getCurrentConfigurationSchema](#operation/getCurrentConfigurationSchema)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_current_configuration_schema_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: ConfigurationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_current_configuration_schema" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/current/configuration-schema', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LConfigurationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_groups(self, id, **kwargs):  # noqa: E501
        """Get groups in workspace  # noqa: E501

        Get groups in workspace  <small>ref: [getGroups](#operation/getGroups)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_groups(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str name: Value for filtering groups by name.
        :param bool include_full_users: Expand group member objects
        :return: GetGroupsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_groups_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_groups_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_groups_with_http_info(self, id, **kwargs):  # noqa: E501
        """Get groups in workspace  # noqa: E501

        Get groups in workspace  <small>ref: [getGroups](#operation/getGroups)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_groups_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str name: Value for filtering groups by name.
        :param bool include_full_users: Expand group member objects
        :return: GetGroupsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'limit', 'offset', 'name', 'include_full_users']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_groups" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_groups`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501
        if 'include_full_users' in params:
            query_params.append(('includeFullUsers', params['include_full_users']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/groups', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LGetGroupsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def invite_list_of_users(self, body, id, **kwargs):  # noqa: E501
        """Invite users  # noqa: E501

        Invite a list of users to a workspace. Send an email to the specified emails with invitation codes.  <small>ref: [inviteListOfUsers](#operation/inviteListOfUsers)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.invite_list_of_users(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param InviteListOfUsersPayload body: (required)
        :param int id: (required)
        :return: WorkspaceUserIdList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.invite_list_of_users_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.invite_list_of_users_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def invite_list_of_users_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Invite users  # noqa: E501

        Invite a list of users to a workspace. Send an email to the specified emails with invitation codes.  <small>ref: [inviteListOfUsers](#operation/inviteListOfUsers)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.invite_list_of_users_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param InviteListOfUsersPayload body: (required)
        :param int id: (required)
        :return: WorkspaceUserIdList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method invite_list_of_users" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `invite_list_of_users`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `invite_list_of_users`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/people/batch', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LWorkspaceUserIdList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def invite_user(self, body, id, **kwargs):  # noqa: E501
        """Invite user  # noqa: E501

        Invite user to a workspace. Send an email to the specified email with an invitation code.  <small>ref: [inviteUser](#operation/inviteUser)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.invite_user(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param InviteUserPayload body: (required)
        :param int id: (required)
        :return: InviteUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.invite_user_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.invite_user_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def invite_user_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Invite user  # noqa: E501

        Invite user to a workspace. Send an email to the specified email with an invitation code.  <small>ref: [inviteUser](#operation/inviteUser)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.invite_user_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param InviteUserPayload body: (required)
        :param int id: (required)
        :return: InviteUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method invite_user" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `invite_user`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `invite_user`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/people', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LInviteUserResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_workspace_users(self, id, **kwargs):  # noqa: E501
        """List workspace users  # noqa: E501

        List users for the specified workspace.  <small>ref: [listWorkspaceUsers](#operation/listWorkspaceUsers)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_workspace_users(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param Status status: Status values to filter the list
        :param bool include_privileges: Include the user's maximal privileges and authorization roles
        :param Roles roles: Roles values to filter the list
        :param ExcludingRoles excluding_roles: Excluded roles to filter the list
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :return: PersonReadResponseList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_workspace_users_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_workspace_users_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def list_workspace_users_with_http_info(self, id, **kwargs):  # noqa: E501
        """List workspace users  # noqa: E501

        List users for the specified workspace.  <small>ref: [listWorkspaceUsers](#operation/listWorkspaceUsers)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_workspace_users_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param Status status: Status values to filter the list
        :param bool include_privileges: Include the user's maximal privileges and authorization roles
        :param Roles roles: Roles values to filter the list
        :param ExcludingRoles excluding_roles: Excluded roles to filter the list
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :return: PersonReadResponseList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'status', 'include_privileges', 'roles', 'excluding_roles', 'limit', 'offset', 'filter_type', 'sort', 'filter_fields', 'filter', 'include_count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_workspace_users" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `list_workspace_users`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
        if 'include_privileges' in params:
            query_params.append(('includePrivileges', params['include_privileges']))  # noqa: E501
        if 'roles' in params:
            query_params.append(('roles', params['roles']))  # noqa: E501
        if 'excluding_roles' in params:
            query_params.append(('excludingRoles', params['excluding_roles']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'filter_type' in params:
            query_params.append(('filterType', params['filter_type']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'filter_fields' in params:
            query_params.append(('filterFields', params['filter_fields']))  # noqa: E501
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501
        if 'include_count' in params:
            query_params.append(('includeCount', params['include_count']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/people', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LPersonReadResponseList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_workspaces(self, **kwargs):  # noqa: E501
        """List Workspaces  # noqa: E501

        Lists all workspaces available to user  <small>ref: [listWorkspaces](#operation/listWorkspaces)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_workspaces(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: account ID associated with workspaces, required for access by account admins
        :param str fields: comma-separated list of fields.
        :return: WorkspacesList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_workspaces_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_workspaces_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_workspaces_with_http_info(self, **kwargs):  # noqa: E501
        """List Workspaces  # noqa: E501

        Lists all workspaces available to user  <small>ref: [listWorkspaces](#operation/listWorkspaces)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_workspaces_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: account ID associated with workspaces, required for access by account admins
        :param str fields: comma-separated list of fields.
        :return: WorkspacesList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'fields']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_workspaces" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'account_id' in params:
            query_params.append(('accountId', params['account_id']))  # noqa: E501
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LWorkspacesList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read_current_workspace(self, **kwargs):  # noqa: E501
        """Read current workspace  # noqa: E501

        Get information about the current workspace.  <small>ref: [readCurrentWorkspace](#operation/readCurrentWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_current_workspace(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: Workspace
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.read_current_workspace_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.read_current_workspace_with_http_info(**kwargs)  # noqa: E501
            return data

    def read_current_workspace_with_http_info(self, **kwargs):  # noqa: E501
        """Read current workspace  # noqa: E501

        Get information about the current workspace.  <small>ref: [readCurrentWorkspace](#operation/readCurrentWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_current_workspace_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: Workspace
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read_current_workspace" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/current', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LWorkspace',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def remove_users_from_group(self, id, group_id, user_ids, **kwargs):  # noqa: E501
        """Remove users from group in workspace  # noqa: E501

        Remove users from group in workspace.  <small>ref: [removeUsersFromGroup](#operation/removeUsersFromGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_users_from_group(id, group_id, user_ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str group_id: (required)
        :param list[str] user_ids: IDs of users to remove from group (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.remove_users_from_group_with_http_info(id, group_id, user_ids, **kwargs)  # noqa: E501
        else:
            (data) = self.remove_users_from_group_with_http_info(id, group_id, user_ids, **kwargs)  # noqa: E501
            return data

    def remove_users_from_group_with_http_info(self, id, group_id, user_ids, **kwargs):  # noqa: E501
        """Remove users from group in workspace  # noqa: E501

        Remove users from group in workspace.  <small>ref: [removeUsersFromGroup](#operation/removeUsersFromGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_users_from_group_with_http_info(id, group_id, user_ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str group_id: (required)
        :param list[str] user_ids: IDs of users to remove from group (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'group_id', 'user_ids']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method remove_users_from_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `remove_users_from_group`")  # noqa: E501
        # verify the required parameter 'group_id' is set
        if ('group_id' not in params or
                params['group_id'] is None):
            raise ValueError("Missing the required parameter `group_id` when calling `remove_users_from_group`")  # noqa: E501
        # verify the required parameter 'user_ids' is set
        if ('user_ids' not in params or
                params['user_ids'] is None):
            raise ValueError("Missing the required parameter `user_ids` when calling `remove_users_from_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'group_id' in params:
            path_params['groupId'] = params['group_id']  # noqa: E501

        query_params = []
        if 'user_ids' in params:
            query_params.append(('userIds', params['user_ids']))  # noqa: E501
            collection_formats['userIds'] = 'multi'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/groups/:groupId/users', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def save_current_workspace_configuration(self, body, **kwargs):  # noqa: E501
        """Save current workspace configuration  # noqa: E501

        Update the workspace configuration for the specified keys. To reset a configuration value to its default, use the [delete endpoint](#operation/deleteWorkspaceConfigurationSettings).  Use the [getConfigurationSchema](#operation/getConfigurationSchema) endpoint to get the list of editable configuration values.  <small>ref: [saveCurrentWorkspaceConfiguration](#operation/saveCurrentWorkspaceConfiguration)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save_current_workspace_configuration(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ConfigurationChangePayload body: (required)
        :return: ConfigurationSavedResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.save_current_workspace_configuration_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.save_current_workspace_configuration_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def save_current_workspace_configuration_with_http_info(self, body, **kwargs):  # noqa: E501
        """Save current workspace configuration  # noqa: E501

        Update the workspace configuration for the specified keys. To reset a configuration value to its default, use the [delete endpoint](#operation/deleteWorkspaceConfigurationSettings).  Use the [getConfigurationSchema](#operation/getConfigurationSchema) endpoint to get the list of editable configuration values.  <small>ref: [saveCurrentWorkspaceConfiguration](#operation/saveCurrentWorkspaceConfiguration)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save_current_workspace_configuration_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ConfigurationChangePayload body: (required)
        :return: ConfigurationSavedResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method save_current_workspace_configuration" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `save_current_workspace_configuration`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/current/configuration', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LConfigurationSavedResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def save_workspace_configuration(self, body, id, **kwargs):  # noqa: E501
        """Save workspace configuration  # noqa: E501

        Update the workspace configuration for the specified keys. To reset a configuration value to its default, use the [delete endpoint](#operation/deleteWorkspaceConfigurationSettings).  Use the [getConfigurationSchema](#operation/getConfigurationSchema) endpoint to get the list of editable configuration values.  <small>ref: [saveWorkspaceConfiguration](#operation/saveWorkspaceConfiguration)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save_workspace_configuration(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ConfigurationChangePayload body: (required)
        :param int id: (required)
        :return: ConfigurationSavedResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.save_workspace_configuration_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.save_workspace_configuration_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def save_workspace_configuration_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Save workspace configuration  # noqa: E501

        Update the workspace configuration for the specified keys. To reset a configuration value to its default, use the [delete endpoint](#operation/deleteWorkspaceConfigurationSettings).  Use the [getConfigurationSchema](#operation/getConfigurationSchema) endpoint to get the list of editable configuration values.  <small>ref: [saveWorkspaceConfiguration](#operation/saveWorkspaceConfiguration)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save_workspace_configuration_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ConfigurationChangePayload body: (required)
        :param int id: (required)
        :return: ConfigurationSavedResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method save_workspace_configuration" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `save_workspace_configuration`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `save_workspace_configuration`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/configuration', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LConfigurationSavedResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def set_roles_to_group(self, body, id, group_id, **kwargs):  # noqa: E501
        """Sets roles to group in the workspace  # noqa: E501

        Sets roles to group in the workspace  <small>ref: [setRolesToGroup](#operation/setRolesToGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.set_roles_to_group(body, id, group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SetRolesToGroupRequest body: (required)
        :param int id: (required)
        :param str group_id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.set_roles_to_group_with_http_info(body, id, group_id, **kwargs)  # noqa: E501
        else:
            (data) = self.set_roles_to_group_with_http_info(body, id, group_id, **kwargs)  # noqa: E501
            return data

    def set_roles_to_group_with_http_info(self, body, id, group_id, **kwargs):  # noqa: E501
        """Sets roles to group in the workspace  # noqa: E501

        Sets roles to group in the workspace  <small>ref: [setRolesToGroup](#operation/setRolesToGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.set_roles_to_group_with_http_info(body, id, group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SetRolesToGroupRequest body: (required)
        :param int id: (required)
        :param str group_id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id', 'group_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method set_roles_to_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `set_roles_to_group`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `set_roles_to_group`")  # noqa: E501
        # verify the required parameter 'group_id' is set
        if ('group_id' not in params or
                params['group_id'] is None):
            raise ValueError("Missing the required parameter `group_id` when calling `set_roles_to_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'group_id' in params:
            path_params['groupId'] = params['group_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/groups/:groupId/roles', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def suspend_user(self, person_id, id, **kwargs):  # noqa: E501
        """Suspend user  # noqa: E501

        Suspend a user from the specified workspace.  <small>ref: [suspendUser](#operation/suspendUser)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.suspend_user(person_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int person_id: (required)
        :param int id: (required)
        :param object body:
        :return: SuspendedUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.suspend_user_with_http_info(person_id, id, **kwargs)  # noqa: E501
        else:
            (data) = self.suspend_user_with_http_info(person_id, id, **kwargs)  # noqa: E501
            return data

    def suspend_user_with_http_info(self, person_id, id, **kwargs):  # noqa: E501
        """Suspend user  # noqa: E501

        Suspend a user from the specified workspace.  <small>ref: [suspendUser](#operation/suspendUser)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.suspend_user_with_http_info(person_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int person_id: (required)
        :param int id: (required)
        :param object body:
        :return: SuspendedUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['person_id', 'id', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method suspend_user" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'person_id' is set
        if ('person_id' not in params or
                params['person_id'] is None):
            raise ValueError("Missing the required parameter `person_id` when calling `suspend_user`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `suspend_user`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'person_id' in params:
            path_params['personId'] = params['person_id']  # noqa: E501
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/people/{personId}/suspended', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LSuspendedUserResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def suspend_users(self, body, id, **kwargs):  # noqa: E501
        """Bulk suspend users  # noqa: E501

        Suspend users from the specified workspace.  <small>ref: [suspendUsers](#operation/suspendUsers)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.suspend_users(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SuspendListUsersPayload body: (required)
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.suspend_users_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.suspend_users_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def suspend_users_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Bulk suspend users  # noqa: E501

        Suspend users from the specified workspace.  <small>ref: [suspendUsers](#operation/suspendUsers)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.suspend_users_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SuspendListUsersPayload body: (required)
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method suspend_users" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `suspend_users`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `suspend_users`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/people/suspend', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def transfer_user_assets_in_current_workspace(self, body, **kwargs):  # noqa: E501
        """Transfer User Assets  # noqa: E501

        Transfer Alteryx Analytics Cloud assets to another user in the current workspace. For the given workspace, assigns ownership of all the user's contents to another user. This includes flows, datasets, recipes, and connections–basically any object that can be created and managed through the Alteryx Analytics Cloud UI.  > ℹ️ **NOTE**: This API endpoint does not delete the original user account. To delete the user account, another API call is needed.  > ℹ️ **NOTE**: The asset transfer endpoint cannot be applied to deleted users. You must transfer the assets first before deleting the user.  <small>ref: [transferUserAssetsInCurrentWorkspace](#operation/transferUserAssetsInCurrentWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.transfer_user_assets_in_current_workspace(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransferUserAssetsPayload body: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.transfer_user_assets_in_current_workspace_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.transfer_user_assets_in_current_workspace_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def transfer_user_assets_in_current_workspace_with_http_info(self, body, **kwargs):  # noqa: E501
        """Transfer User Assets  # noqa: E501

        Transfer Alteryx Analytics Cloud assets to another user in the current workspace. For the given workspace, assigns ownership of all the user's contents to another user. This includes flows, datasets, recipes, and connections–basically any object that can be created and managed through the Alteryx Analytics Cloud UI.  > ℹ️ **NOTE**: This API endpoint does not delete the original user account. To delete the user account, another API call is needed.  > ℹ️ **NOTE**: The asset transfer endpoint cannot be applied to deleted users. You must transfer the assets first before deleting the user.  <small>ref: [transferUserAssetsInCurrentWorkspace](#operation/transferUserAssetsInCurrentWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.transfer_user_assets_in_current_workspace_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransferUserAssetsPayload body: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method transfer_user_assets_in_current_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `transfer_user_assets_in_current_workspace`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/current/transfer', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def transfer_user_assets_in_workspace(self, body, id, **kwargs):  # noqa: E501
        """Transfer User Assets  # noqa: E501

        Transfer Alteryx Analytics Cloud assets to another user in the workspace. For the given workspace, assigns ownership of all the user's contents to another user. This includes flows, datasets, recipes, and connections–basically any object that can be created and managed through the Alteryx Analytics Cloud UI.  > ℹ️ **NOTE**: This API endpoint does not delete the original user account. To delete the user account, another API call is needed.  > ℹ️ **NOTE**: The asset transfer endpoint cannot be applied to deleted users. You must transfer the assets first before deleting the user.  <small>ref: [transferUserAssetsInWorkspace](#operation/transferUserAssetsInWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.transfer_user_assets_in_workspace(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransferUserAssetsPayload body: (required)
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.transfer_user_assets_in_workspace_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.transfer_user_assets_in_workspace_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def transfer_user_assets_in_workspace_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Transfer User Assets  # noqa: E501

        Transfer Alteryx Analytics Cloud assets to another user in the workspace. For the given workspace, assigns ownership of all the user's contents to another user. This includes flows, datasets, recipes, and connections–basically any object that can be created and managed through the Alteryx Analytics Cloud UI.  > ℹ️ **NOTE**: This API endpoint does not delete the original user account. To delete the user account, another API call is needed.  > ℹ️ **NOTE**: The asset transfer endpoint cannot be applied to deleted users. You must transfer the assets first before deleting the user.  <small>ref: [transferUserAssetsInWorkspace](#operation/transferUserAssetsInWorkspace)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.transfer_user_assets_in_workspace_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransferUserAssetsPayload body: (required)
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method transfer_user_assets_in_workspace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `transfer_user_assets_in_workspace`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `transfer_user_assets_in_workspace`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/transfer', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def unsuspend_users(self, body, id, **kwargs):  # noqa: E501
        """Bulk unsuspend users  # noqa: E501

        Unsuspend users from the specified workspace.  <small>ref: [unsuspendUsers](#operation/unsuspendUsers)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.unsuspend_users(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UnsuspendListUsersPayload body: (required)
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.unsuspend_users_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.unsuspend_users_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def unsuspend_users_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Bulk unsuspend users  # noqa: E501

        Unsuspend users from the specified workspace.  <small>ref: [unsuspendUsers](#operation/unsuspendUsers)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.unsuspend_users_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UnsuspendListUsersPayload body: (required)
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method unsuspend_users" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `unsuspend_users`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `unsuspend_users`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/people/unsuspend', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_group(self, body, id, group_id, **kwargs):  # noqa: E501
        """Update group details in workspace  # noqa: E501

        Update group details in workspace.  <small>ref: [updateGroup](#operation/updateGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_group(body, id, group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateGroupPayload body: (required)
        :param int id: (required)
        :param str group_id: (required)
        :return: UpdateGroupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_group_with_http_info(body, id, group_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_group_with_http_info(body, id, group_id, **kwargs)  # noqa: E501
            return data

    def update_group_with_http_info(self, body, id, group_id, **kwargs):  # noqa: E501
        """Update group details in workspace  # noqa: E501

        Update group details in workspace.  <small>ref: [updateGroup](#operation/updateGroup)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_group_with_http_info(body, id, group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateGroupPayload body: (required)
        :param int id: (required)
        :param str group_id: (required)
        :return: UpdateGroupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id', 'group_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_group`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_group`")  # noqa: E501
        # verify the required parameter 'group_id' is set
        if ('group_id' not in params or
                params['group_id'] is None):
            raise ValueError("Missing the required parameter `group_id` when calling `update_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'group_id' in params:
            path_params['groupId'] = params['group_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/workspaces/{id}/groups/:groupId', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LUpdateGroupResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
