# coding: utf-8

"""
    Workflows API

    OpenAPI spec version: v1
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from src.client.api.api_client import ApiClient


class WorkflowsApi(object):
    """Workflows API client for Alteryx Cloud
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_workflows(self, **kwargs):  # noqa: E501
        """List workflows  # noqa: E501

        Retrieve a list of workflows with optional filtering and pagination.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_workflows(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool include_associated_subjects: Include associated subjects in the response
        :param int limit: Maximum number of workflows to return (default 10)
        :param str name_like: Filter workflows by name (partial match)
        :param int offset: Number of workflows to skip for pagination (default 0)
        :param str sort: Sort order (e.g., '-updatedAt' for descending by update date)
        :param str type_eq: Filter workflows by type (e.g., 'cloud')
        :return: WorkflowList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_workflows_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_workflows_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_workflows_with_http_info(self, **kwargs):  # noqa: E501
        """List workflows  # noqa: E501

        Retrieve a list of workflows with optional filtering and pagination.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_workflows_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool include_associated_subjects: Include associated subjects in the response
        :param int limit: Maximum number of workflows to return (default 10)
        :param str name_like: Filter workflows by name (partial match)
        :param int offset: Number of workflows to skip for pagination (default 0)
        :param str sort: Sort order (e.g., '-updatedAt' for descending by update date)
        :param str type_eq: Filter workflows by type (e.g., 'cloud')
        :return: WorkflowList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['include_associated_subjects', 'limit', 'name_like', 'offset', 'sort', 'type_eq']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_workflows" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'include_associated_subjects' in params:
            query_params.append(('includeAssociatedSubjects', params['include_associated_subjects']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'name_like' in params:
            query_params.append(('name[like]', params['name_like']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'type_eq' in params:
            query_params.append(('type[eq]', params['type_eq']))  # noqa: E501

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
            '/svc-workflow/api/v1/workflows', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WorkflowList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_workflow(self, workflow_id, **kwargs):  # noqa: E501
        """Get workflow  # noqa: E501

        Retrieve a specific workflow by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_workflow(workflow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str workflow_id: Workflow ID (required)
        :return: Workflow
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_workflow_with_http_info(workflow_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_workflow_with_http_info(workflow_id, **kwargs)  # noqa: E501
            return data

    def get_workflow_with_http_info(self, workflow_id, **kwargs):  # noqa: E501
        """Get workflow  # noqa: E501

        Retrieve a specific workflow by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_workflow_with_http_info(workflow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str workflow_id: Workflow ID (required)
        :return: Workflow
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['workflow_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_workflow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'workflow_id' is set
        if ('workflow_id' not in params or
                params['workflow_id'] is None):
            raise ValueError("Missing the required parameter `workflow_id` when calling `get_workflow`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'workflow_id' in params:
            path_params['workflow_id'] = params['workflow_id']  # noqa: E501

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
            '/svc-workflow/api/v1/workflows/{workflow_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Workflow',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def run_workflow(self, workflow_id, **kwargs):  # noqa: E501
        """Run workflow  # noqa: E501

        Execute a specific workflow by ID with optional compiler version and execution engine.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.run_workflow(workflow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str workflow_id: Workflow ID (required)
        :param str compiler_version: Compiler version (e.g., '6.21.6')
        :param str execution_engine: Execution engine (e.g., 'amp')
        :return: WorkflowRunResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.run_workflow_with_http_info(workflow_id, **kwargs)  # noqa: E501
        else:
            (data) = self.run_workflow_with_http_info(workflow_id, **kwargs)  # noqa: E501
            return data

    def run_workflow_with_http_info(self, workflow_id, **kwargs):  # noqa: E501
        """Run workflow  # noqa: E501

        Execute a specific workflow by ID with optional compiler version and execution engine.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.run_workflow_with_http_info(workflow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str workflow_id: Workflow ID (required)
        :param str compiler_version: Compiler version (e.g., '6.21.6')
        :param str execution_engine: Execution engine (e.g., 'amp')
        :return: WorkflowRunResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['workflow_id', 'compiler_version', 'execution_engine']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method run_workflow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'workflow_id' is set
        if ('workflow_id' not in params or
                params['workflow_id'] is None):
            raise ValueError("Missing the required parameter `workflow_id` when calling `run_workflow`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'workflow_id' in params:
            path_params['workflow_id'] = params['workflow_id']  # noqa: E501

        query_params = []
        if 'compiler_version' in params:
            query_params.append(('compilerVersion', params['compiler_version']))  # noqa: E501
        if 'execution_engine' in params:
            query_params.append(('executionEngine', params['execution_engine']))  # noqa: E501

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
            '/svc-workflow/api/v1/workflows/{workflow_id}/run', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WorkflowRunResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
