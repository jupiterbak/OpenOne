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


class FlowApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
     
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def copy_flow(self, body, id, **kwargs):  # noqa: E501
        """Copy Flow  # noqa: E501

        Create a copy of this flow, as well as all contained recipes.  <small>ref: [copyFlow](#operation/copyFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.copy_flow(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CopyFlowRequest body: (required)
        :param int id: (required)
        :return: Flow
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.copy_flow_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.copy_flow_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def copy_flow_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Copy Flow  # noqa: E501

        Create a copy of this flow, as well as all contained recipes.  <small>ref: [copyFlow](#operation/copyFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.copy_flow_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CopyFlowRequest body: (required)
        :param int id: (required)
        :return: Flow
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
                    " to method copy_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `copy_flow`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `copy_flow`")  # noqa: E501

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
            '/v4/flows/{id}/copy', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LFlow',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def count_flows(self, **kwargs):  # noqa: E501
        """Count flows  # noqa: E501

        Count existing flows  <small>ref: [countFlows](#operation/countFlows)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_flows(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted18 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param int folder_id: Only show flow from this folder
        :param str flows_filter: Which types of flows to count. One of ['all', 'shared', 'owned']
        :return: Count
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.count_flows_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.count_flows_with_http_info(**kwargs)  # noqa: E501
            return data

    def count_flows_with_http_info(self, **kwargs):  # noqa: E501
        """Count flows  # noqa: E501

        Count existing flows  <small>ref: [countFlows](#operation/countFlows)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_flows_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted18 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param int folder_id: Only show flow from this folder
        :param str flows_filter: Which types of flows to count. One of ['all', 'shared', 'owned']
        :return: Count
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['fields', 'embed', 'include_deleted', 'limit', 'offset', 'filter_type', 'sort', 'filter_fields', 'filter', 'include_count', 'folder_id', 'flows_filter']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method count_flows" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501
        if 'embed' in params:
            query_params.append(('embed', params['embed']))  # noqa: E501
        if 'include_deleted' in params:
            query_params.append(('includeDeleted', params['include_deleted']))  # noqa: E501
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
        if 'folder_id' in params:
            query_params.append(('folderId', params['folder_id']))  # noqa: E501
        if 'flows_filter' in params:
            query_params.append(('flowsFilter', params['flows_filter']))  # noqa: E501

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
            '/v4/flows/count', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LCount',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def count_flows_library(self, **kwargs):  # noqa: E501
        """Flow Library (count)  # noqa: E501

        Count flows, with special filtering behaviour  <small>ref: [countFlowsLibrary](#operation/countFlowsLibrary)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_flows_library(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted21 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param str flows_filter: Which types of flows to count. One of ['all', 'shared', 'owned', 'forTransfer']
        :return: FlowCountInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.count_flows_library_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.count_flows_library_with_http_info(**kwargs)  # noqa: E501
            return data

    def count_flows_library_with_http_info(self, **kwargs):  # noqa: E501
        """Flow Library (count)  # noqa: E501

        Count flows, with special filtering behaviour  <small>ref: [countFlowsLibrary](#operation/countFlowsLibrary)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_flows_library_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted21 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param str flows_filter: Which types of flows to count. One of ['all', 'shared', 'owned', 'forTransfer']
        :return: FlowCountInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['fields', 'embed', 'include_deleted', 'limit', 'offset', 'filter_type', 'sort', 'filter_fields', 'filter', 'include_count', 'flows_filter']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method count_flows_library" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501
        if 'embed' in params:
            query_params.append(('embed', params['embed']))  # noqa: E501
        if 'include_deleted' in params:
            query_params.append(('includeDeleted', params['include_deleted']))  # noqa: E501
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
        if 'flows_filter' in params:
            query_params.append(('flowsFilter', params['flows_filter']))  # noqa: E501

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
            '/v4/flowsLibrary/count', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LFlowCountInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_flow(self, body, **kwargs):  # noqa: E501
        """Create flow  # noqa: E501

        Create a new flow with specified name and optional description and target folder. > ℹ️ **NOTE**: You cannot add datasets to the flow through this endpoint. Moving pre-existing datasets into a flow is not supported in this release. Create the flow first and then when you create the datasets, associate them with the flow at the time of creation. - See [Create imported dataset](#operation/createImportedDataset) - See [Create wrangled dataset](#operation/createWrangledDataset)  <small>ref: [createFlow](#operation/createFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_flow(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param FlowCreateRequest body: (required)
        :return: Flow
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_flow_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_flow_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_flow_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create flow  # noqa: E501

        Create a new flow with specified name and optional description and target folder. > ℹ️ **NOTE**: You cannot add datasets to the flow through this endpoint. Moving pre-existing datasets into a flow is not supported in this release. Create the flow first and then when you create the datasets, associate them with the flow at the time of creation. - See [Create imported dataset](#operation/createImportedDataset) - See [Create wrangled dataset](#operation/createWrangledDataset)  <small>ref: [createFlow](#operation/createFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_flow_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param FlowCreateRequest body: (required)
        :return: Flow
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
                    " to method create_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_flow`")  # noqa: E501

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
            '/v4/flows', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LFlow',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_flow(self, id, **kwargs):  # noqa: E501
        """Delete flow  # noqa: E501

        Delete an existing flow  <small>ref: [deleteFlow](#operation/deleteFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_flow(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_flow_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_flow_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def delete_flow_with_http_info(self, id, **kwargs):  # noqa: E501
        """Delete flow  # noqa: E501

        Delete an existing flow  <small>ref: [deleteFlow](#operation/deleteFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_flow_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: None
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
                    " to method delete_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_flow`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/flows/{id}', 'DELETE',
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

    def get_flow(self, id, **kwargs):  # noqa: E501
        """Get flow  # noqa: E501

        Get an existing flow  <small>ref: [getFlow](#operation/getFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted19 include_deleted: Whether to include all or some of the nested deleted objects.
        :return: Flow
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_flow_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_flow_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_flow_with_http_info(self, id, **kwargs):  # noqa: E501
        """Get flow  # noqa: E501

        Get an existing flow  <small>ref: [getFlow](#operation/getFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted19 include_deleted: Whether to include all or some of the nested deleted objects.
        :return: Flow
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'fields', 'embed', 'include_deleted']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_flow`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501
        if 'embed' in params:
            query_params.append(('embed', params['embed']))  # noqa: E501
        if 'include_deleted' in params:
            query_params.append(('includeDeleted', params['include_deleted']))  # noqa: E501

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
            '/v4/flows/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LFlow',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_flow_count_for_folder(self, id, **kwargs):  # noqa: E501
        """Count flows in folder  # noqa: E501

        Get the count of flows contained in this folder.  <small>ref: [getFlowCountForFolder](#operation/getFlowCountForFolder)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_count_for_folder(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted25 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param str flows_filter: Which types of flows to count. One of ['all', 'shared', 'owned']
        :return: Count
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_flow_count_for_folder_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_flow_count_for_folder_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_flow_count_for_folder_with_http_info(self, id, **kwargs):  # noqa: E501
        """Count flows in folder  # noqa: E501

        Get the count of flows contained in this folder.  <small>ref: [getFlowCountForFolder](#operation/getFlowCountForFolder)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_count_for_folder_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted25 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param str flows_filter: Which types of flows to count. One of ['all', 'shared', 'owned']
        :return: Count
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'fields', 'embed', 'include_deleted', 'limit', 'offset', 'filter_type', 'sort', 'filter_fields', 'filter', 'include_count', 'flows_filter']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_flow_count_for_folder" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_flow_count_for_folder`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501
        if 'embed' in params:
            query_params.append(('embed', params['embed']))  # noqa: E501
        if 'include_deleted' in params:
            query_params.append(('includeDeleted', params['include_deleted']))  # noqa: E501
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
        if 'flows_filter' in params:
            query_params.append(('flowsFilter', params['flows_filter']))  # noqa: E501

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
            '/v4/folders/{id}/flows/count', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LCount',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_flow_inputs(self, id, **kwargs):  # noqa: E501
        """List Flow inputs  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  List all the inputs of a Flow. Also include data sources that are present in referenced flows.  <small>ref: [getFlowInputs](#operation/getFlowInputs)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_inputs(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: ImportedDatasetList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_flow_inputs_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_flow_inputs_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_flow_inputs_with_http_info(self, id, **kwargs):  # noqa: E501
        """List Flow inputs  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  List all the inputs of a Flow. Also include data sources that are present in referenced flows.  <small>ref: [getFlowInputs](#operation/getFlowInputs)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_inputs_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: ImportedDatasetList
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
                    " to method get_flow_inputs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_flow_inputs`")  # noqa: E501

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
            '/v4/flows/{id}/inputs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LImportedDatasetList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_flow_outputs(self, id, **kwargs):  # noqa: E501
        """List Flow outputs  # noqa: E501

        List all the outputs of a Flow.  <small>ref: [getFlowOutputs](#operation/getFlowOutputs)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_outputs(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: OutputObjectList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_flow_outputs_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_flow_outputs_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_flow_outputs_with_http_info(self, id, **kwargs):  # noqa: E501
        """List Flow outputs  # noqa: E501

        List all the outputs of a Flow.  <small>ref: [getFlowOutputs](#operation/getFlowOutputs)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_outputs_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: OutputObjectList
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
                    " to method get_flow_outputs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_flow_outputs`")  # noqa: E501

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
            '/v4/flows/{id}/outputs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LOutputObjectList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_flow_package(self, id, **kwargs):  # noqa: E501
        """Export flow  # noqa: E501

        Retrieve a package containing the definition of the specified flow.  Response body is the contents of the package. Package contents are a ZIPped version of the flow definition.  The flow package can be used to import the flow in another environment. See the [Import Flow Package](#operation/importPackage) for more information.  **Quotas**:<br/>40 req./user/min, 50 req./workspace/min  <small>ref: [getFlowPackage](#operation/getFlowPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_package(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str comment: comment to be displayed when flow is imported in a deployment package
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_flow_package_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_flow_package_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_flow_package_with_http_info(self, id, **kwargs):  # noqa: E501
        """Export flow  # noqa: E501

        Retrieve a package containing the definition of the specified flow.  Response body is the contents of the package. Package contents are a ZIPped version of the flow definition.  The flow package can be used to import the flow in another environment. See the [Import Flow Package](#operation/importPackage) for more information.  **Quotas**:<br/>40 req./user/min, 50 req./workspace/min  <small>ref: [getFlowPackage](#operation/getFlowPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_package_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str comment: comment to be displayed when flow is imported in a deployment package
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'comment']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_flow_package" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_flow_package`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'comment' in params:
            query_params.append(('comment', params['comment']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/flows/{id}/package', 'GET',
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

    def get_flow_package_dry_run(self, id, **kwargs):  # noqa: E501
        """Export flow - Dry run  # noqa: E501

        Performs a dry-run of generating a flow package and exporting it, which performs a check of all permissions required to export the package.  If they occur, permissions errors are reported in the response.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [getFlowPackageDryRun](#operation/getFlowPackageDryRun)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_package_dry_run(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_flow_package_dry_run_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_flow_package_dry_run_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_flow_package_dry_run_with_http_info(self, id, **kwargs):  # noqa: E501
        """Export flow - Dry run  # noqa: E501

        Performs a dry-run of generating a flow package and exporting it, which performs a check of all permissions required to export the package.  If they occur, permissions errors are reported in the response.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [getFlowPackageDryRun](#operation/getFlowPackageDryRun)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flow_package_dry_run_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: None
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
                    " to method get_flow_package_dry_run" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_flow_package_dry_run`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/flows/{id}/package/dryRun', 'GET',
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

    def get_flows_for_folder(self, id, **kwargs):  # noqa: E501
        """List flows in folder  # noqa: E501

        Get all flows contained in this folder.  <small>ref: [getFlowsForFolder](#operation/getFlowsForFolder)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flows_for_folder(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted24 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param str flows_filter: Which types of flows to list. One of ['all', 'shared', 'owned']
        :return: FlowList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_flows_for_folder_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_flows_for_folder_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_flows_for_folder_with_http_info(self, id, **kwargs):  # noqa: E501
        """List flows in folder  # noqa: E501

        Get all flows contained in this folder.  <small>ref: [getFlowsForFolder](#operation/getFlowsForFolder)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_flows_for_folder_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted24 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param str flows_filter: Which types of flows to list. One of ['all', 'shared', 'owned']
        :return: FlowList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'fields', 'embed', 'include_deleted', 'limit', 'offset', 'filter_type', 'sort', 'filter_fields', 'filter', 'include_count', 'flows_filter']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_flows_for_folder" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_flows_for_folder`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501
        if 'embed' in params:
            query_params.append(('embed', params['embed']))  # noqa: E501
        if 'include_deleted' in params:
            query_params.append(('includeDeleted', params['include_deleted']))  # noqa: E501
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
        if 'flows_filter' in params:
            query_params.append(('flowsFilter', params['flows_filter']))  # noqa: E501

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
            '/v4/folders/{id}/flows', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LFlowList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def import_package(self, **kwargs):  # noqa: E501
        """Import Flow package  # noqa: E501

        Import all flows from the given package. A `ZIP` file as exported by the [export Flow endpoint](#operation/getFlowPackage) is accepted.  Before you import, you can perform a dry-run to check for errors. See [Import Flow package - Dry run](#operation/importPackageDryRun).  This endpoint accept a `multipart/form` content type.  Here is how to send the `ZIP` package using [curl](https://curl.haxx.se/). ``` curl -X POST https://us1.alteryxcloud.com/v4/flows/package \\ -H 'authorization: Bearer <api-token>' \\ -H 'content-type: multipart/form-data' \\ -F 'data=@path/to/flow-package.zip' ```  The response lists the objects that have been created.  <small>ref: [importPackage](#operation/importPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_package(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportFlowPackageRequestZip file:
        :param list[LEnvironmentParameterMapping] environment_parameter_mapping:
        :param list[LConnectionIdMapping] connection_id_mapping:
        :param int folder_id:
        :param bool from_ui: If true, will return the list of imported environment parameters for confirmation if any are referenced in the flow.
        :param bool override_js_udfs: If true, will override the conflicting JS UDFS in the target environment which impacts all the existing flows that references it.
        :return: ImportFlowPackageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.import_package_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.import_package_with_http_info(**kwargs)  # noqa: E501
            return data

    def import_package_with_http_info(self, **kwargs):  # noqa: E501
        """Import Flow package  # noqa: E501

        Import all flows from the given package. A `ZIP` file as exported by the [export Flow endpoint](#operation/getFlowPackage) is accepted.  Before you import, you can perform a dry-run to check for errors. See [Import Flow package - Dry run](#operation/importPackageDryRun).  This endpoint accept a `multipart/form` content type.  Here is how to send the `ZIP` package using [curl](https://curl.haxx.se/). ``` curl -X POST https://us1.alteryxcloud.com/v4/flows/package \\ -H 'authorization: Bearer <api-token>' \\ -H 'content-type: multipart/form-data' \\ -F 'data=@path/to/flow-package.zip' ```  The response lists the objects that have been created.  <small>ref: [importPackage](#operation/importPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_package_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportFlowPackageRequestZip file:
        :param list[LEnvironmentParameterMapping] environment_parameter_mapping:
        :param list[LConnectionIdMapping] connection_id_mapping:
        :param int folder_id:
        :param bool from_ui: If true, will return the list of imported environment parameters for confirmation if any are referenced in the flow.
        :param bool override_js_udfs: If true, will override the conflicting JS UDFS in the target environment which impacts all the existing flows that references it.
        :return: ImportFlowPackageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file', 'environment_parameter_mapping', 'connection_id_mapping', 'folder_id', 'from_ui', 'override_js_udfs']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method import_package" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'folder_id' in params:
            query_params.append(('folderId', params['folder_id']))  # noqa: E501
        if 'from_ui' in params:
            query_params.append(('fromUI', params['from_ui']))  # noqa: E501
        if 'override_js_udfs' in params:
            query_params.append(('overrideJsUdfs', params['override_js_udfs']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'file' in params:
            form_params.append(('File', params['file']))  # noqa: E501
        if 'environment_parameter_mapping' in params:
            form_params.append(('environmentParameterMapping', params['environment_parameter_mapping']))  # noqa: E501
            collection_formats['environmentParameterMapping'] = 'multi'  # noqa: E501
        if 'connection_id_mapping' in params:
            form_params.append(('connectionIdMapping', params['connection_id_mapping']))  # noqa: E501
            collection_formats['connectionIdMapping'] = 'multi'  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/flows/package', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LImportFlowPackageResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def import_package_dry_run(self, **kwargs):  # noqa: E501
        """Import Flow package - Dry run  # noqa: E501

        Test importing flow package and return information about what objects would be created.  The same payload as for [Import Flow package](#operation/importPackage) is expected.  <small>ref: [importPackageDryRun](#operation/importPackageDryRun)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_package_dry_run(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportFlowPackageRequestZip file:
        :param list[LEnvironmentParameterMapping] environment_parameter_mapping:
        :param list[LConnectionIdMapping] connection_id_mapping:
        :param int folder_id:
        :return: ImportFlowPackageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.import_package_dry_run_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.import_package_dry_run_with_http_info(**kwargs)  # noqa: E501
            return data

    def import_package_dry_run_with_http_info(self, **kwargs):  # noqa: E501
        """Import Flow package - Dry run  # noqa: E501

        Test importing flow package and return information about what objects would be created.  The same payload as for [Import Flow package](#operation/importPackage) is expected.  <small>ref: [importPackageDryRun](#operation/importPackageDryRun)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_package_dry_run_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportFlowPackageRequestZip file:
        :param list[LEnvironmentParameterMapping] environment_parameter_mapping:
        :param list[LConnectionIdMapping] connection_id_mapping:
        :param int folder_id:
        :return: ImportFlowPackageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file', 'environment_parameter_mapping', 'connection_id_mapping', 'folder_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method import_package_dry_run" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'folder_id' in params:
            query_params.append(('folderId', params['folder_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'file' in params:
            form_params.append(('File', params['file']))  # noqa: E501
        if 'environment_parameter_mapping' in params:
            form_params.append(('environmentParameterMapping', params['environment_parameter_mapping']))  # noqa: E501
            collection_formats['environmentParameterMapping'] = 'multi'  # noqa: E501
        if 'connection_id_mapping' in params:
            form_params.append(('connectionIdMapping', params['connection_id_mapping']))  # noqa: E501
            collection_formats['connectionIdMapping'] = 'multi'  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/flows/package/dryRun', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LImportFlowPackageResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_flows(self, **kwargs):  # noqa: E501
        """List flows  # noqa: E501

        List existing flows  <small>ref: [listFlows](#operation/listFlows)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_flows(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted3 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param int folder_id: Only show flow from this folder
        :param str flows_filter: Which types of flows to list. One of ['all', 'shared', 'owned']
        :return: FlowList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_flows_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_flows_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_flows_with_http_info(self, **kwargs):  # noqa: E501
        """List flows  # noqa: E501

        List existing flows  <small>ref: [listFlows](#operation/listFlows)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_flows_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted3 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param int folder_id: Only show flow from this folder
        :param str flows_filter: Which types of flows to list. One of ['all', 'shared', 'owned']
        :return: FlowList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['fields', 'embed', 'include_deleted', 'limit', 'offset', 'filter_type', 'sort', 'filter_fields', 'filter', 'include_count', 'folder_id', 'flows_filter']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_flows" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501
        if 'embed' in params:
            query_params.append(('embed', params['embed']))  # noqa: E501
        if 'include_deleted' in params:
            query_params.append(('includeDeleted', params['include_deleted']))  # noqa: E501
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
        if 'folder_id' in params:
            query_params.append(('folderId', params['folder_id']))  # noqa: E501
        if 'flows_filter' in params:
            query_params.append(('flowsFilter', params['flows_filter']))  # noqa: E501

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
            '/v4/flows', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LFlowList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_flows_library(self, **kwargs):  # noqa: E501
        """Flow Library (list)  # noqa: E501

        List flows, with special filtering behaviour  <small>ref: [listFlowsLibrary](#operation/listFlowsLibrary)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_flows_library(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted20 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param str flows_filter: Which types of flows to list. One of ['all', 'shared', 'owned', 'forTransfer']
        :param bool exclude_folders: specifies if we want to hide folders
        :return: FlowLibraryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_flows_library_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_flows_library_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_flows_library_with_http_info(self, **kwargs):  # noqa: E501
        """Flow Library (list)  # noqa: E501

        List flows, with special filtering behaviour  <small>ref: [listFlowsLibrary](#operation/listFlowsLibrary)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_flows_library_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted20 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param str flows_filter: Which types of flows to list. One of ['all', 'shared', 'owned', 'forTransfer']
        :param bool exclude_folders: specifies if we want to hide folders
        :return: FlowLibraryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['fields', 'embed', 'include_deleted', 'limit', 'offset', 'filter_type', 'sort', 'filter_fields', 'filter', 'include_count', 'flows_filter', 'exclude_folders']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_flows_library" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501
        if 'embed' in params:
            query_params.append(('embed', params['embed']))  # noqa: E501
        if 'include_deleted' in params:
            query_params.append(('includeDeleted', params['include_deleted']))  # noqa: E501
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
        if 'flows_filter' in params:
            query_params.append(('flowsFilter', params['flows_filter']))  # noqa: E501
        if 'exclude_folders' in params:
            query_params.append(('excludeFolders', params['exclude_folders']))  # noqa: E501

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
            '/v4/flowsLibrary', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LFlowLibraryResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def move_flow(self, body, id, **kwargs):  # noqa: E501
        """Move Flow  # noqa: E501

        Move Flow to some directory  <small>ref: [moveFlow](#operation/moveFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.move_flow(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MoveFlowRequest body: (required)
        :param int id: (required)
        :return: Flow
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.move_flow_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.move_flow_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def move_flow_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Move Flow  # noqa: E501

        Move Flow to some directory  <small>ref: [moveFlow](#operation/moveFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.move_flow_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MoveFlowRequest body: (required)
        :param int id: (required)
        :return: Flow
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
                    " to method move_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `move_flow`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `move_flow`")  # noqa: E501

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
            '/v4/flows/{id}/move', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LFlow',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def patch_flow(self, body, id, **kwargs):  # noqa: E501
        """Patch flow  # noqa: E501

        Update an existing flow based on the specified identifier. > ℹ️ **NOTE**: You cannot add datasets to the flow through this endpoint. Moving pre-existing datasets into a flow is not supported in this release. Create the flow first and then when you create the datasets, associate them with the flow at the time of creation. - See [Create imported dataset](#operation/createImportedDataset) - See [Create wrangled dataset](#operation/createWrangledDataset)  <small>ref: [patchFlow](#operation/patchFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_flow(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param FlowUpdateRequest body: (required)
        :param int id: (required)
        :return: UpdatedObjectSchema
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.patch_flow_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.patch_flow_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def patch_flow_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Patch flow  # noqa: E501

        Update an existing flow based on the specified identifier. > ℹ️ **NOTE**: You cannot add datasets to the flow through this endpoint. Moving pre-existing datasets into a flow is not supported in this release. Create the flow first and then when you create the datasets, associate them with the flow at the time of creation. - See [Create imported dataset](#operation/createImportedDataset) - See [Create wrangled dataset](#operation/createWrangledDataset)  <small>ref: [patchFlow](#operation/patchFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_flow_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param FlowUpdateRequest body: (required)
        :param int id: (required)
        :return: UpdatedObjectSchema
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
                    " to method patch_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `patch_flow`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `patch_flow`")  # noqa: E501

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
            '/v4/flows/{id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LUpdatedObjectSchema',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def replace_dataset_in_flow(self, body, id, **kwargs):  # noqa: E501
        """Replace dataset  # noqa: E501

        Replace the dataset or the specified wrangled dataset (flow node) in the flow with a new imported or wrangled dataset. This allows one to perform the same action as the \"Replace\" action in the flow UI.  You can get the flow node id (wrangled dataset id) and the imported it from the URL when clicking on a node in the UI.  <small>ref: [replaceDatasetInFlow](#operation/replaceDatasetInFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_dataset_in_flow(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ReplaceDatasetPayload body: (required)
        :param int id: (required)
        :return: ReplaceDatasetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.replace_dataset_in_flow_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.replace_dataset_in_flow_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def replace_dataset_in_flow_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Replace dataset  # noqa: E501

        Replace the dataset or the specified wrangled dataset (flow node) in the flow with a new imported or wrangled dataset. This allows one to perform the same action as the \"Replace\" action in the flow UI.  You can get the flow node id (wrangled dataset id) and the imported it from the URL when clicking on a node in the UI.  <small>ref: [replaceDatasetInFlow](#operation/replaceDatasetInFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_dataset_in_flow_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ReplaceDatasetPayload body: (required)
        :param int id: (required)
        :return: ReplaceDatasetResponse
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
                    " to method replace_dataset_in_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `replace_dataset_in_flow`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `replace_dataset_in_flow`")  # noqa: E501

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
            '/v4/flows/{id}/replaceDataset', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LReplaceDatasetResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def run_flow(self, body, id, **kwargs):  # noqa: E501
        """Run Flow  # noqa: E501

        Run all adhoc destinations in a flow.  (deprecated) If a `scheduleExecutionId` is provided, run all scheduled destinations in the flow.  The request body can stay empty. You can optionally pass parameters: ``` {   \"runParameters\": {     \"overrides\": {       \"data\": [{\"key\": \"varRegion\", \"value\": \"02\"}]     }   } } ```  You can also pass Spark Options that will be used for the Job run. ``` {   \"sparkOptions\": [     {\"key\": \"spark.executor.memory\", \"value\": \"4GB\"}   ] } ```   Using recipe identifiers, you can specify a subset of outputs in the flow to run. See [runJobGroup](#operation/runJobGroup) for more information on specifying `wrangledDataset`. ``` {\"wrangledDatasetIds\": [2, 3]} ```  You can also override each outputs in the Flow using the recipe name. ``` {   \"overrides\": {     \"my recipe name\": {       \"profiler\": true,       \"writesettings\": [         {           \"path\": \"<path_to_output_file>\",           \"action\": \"create\",           \"format\": \"csv\",           \"compression\": \"none\",           \"header\": false,           \"asSingleFile\": false         }       ]     }   } } ```  An array of [jobGroup](#tag/JobGroup) results is returned. Use the ` flowRunId` if you want to track the status of the [flow](#tag/Flow) run. See [Get Flow Run Status](#operation/getFlowRunStatus) for more information.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [runFlow](#operation/runFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.run_flow(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param FlowRunRequest body: (required)
        :param int id: (required)
        :param str x_execution_id: Optional header to safely retry the request without accidentally performing the same operation twice. If a FlowRun with the same `executionId` already exist, the request will return a 304.
        :param bool run_async: Uses queue to run individual jobgroups asynchronously  and return immediately. Default value is false.
        :return: RunFlowResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.run_flow_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.run_flow_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def run_flow_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Run Flow  # noqa: E501

        Run all adhoc destinations in a flow.  (deprecated) If a `scheduleExecutionId` is provided, run all scheduled destinations in the flow.  The request body can stay empty. You can optionally pass parameters: ``` {   \"runParameters\": {     \"overrides\": {       \"data\": [{\"key\": \"varRegion\", \"value\": \"02\"}]     }   } } ```  You can also pass Spark Options that will be used for the Job run. ``` {   \"sparkOptions\": [     {\"key\": \"spark.executor.memory\", \"value\": \"4GB\"}   ] } ```   Using recipe identifiers, you can specify a subset of outputs in the flow to run. See [runJobGroup](#operation/runJobGroup) for more information on specifying `wrangledDataset`. ``` {\"wrangledDatasetIds\": [2, 3]} ```  You can also override each outputs in the Flow using the recipe name. ``` {   \"overrides\": {     \"my recipe name\": {       \"profiler\": true,       \"writesettings\": [         {           \"path\": \"<path_to_output_file>\",           \"action\": \"create\",           \"format\": \"csv\",           \"compression\": \"none\",           \"header\": false,           \"asSingleFile\": false         }       ]     }   } } ```  An array of [jobGroup](#tag/JobGroup) results is returned. Use the ` flowRunId` if you want to track the status of the [flow](#tag/Flow) run. See [Get Flow Run Status](#operation/getFlowRunStatus) for more information.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [runFlow](#operation/runFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.run_flow_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param FlowRunRequest body: (required)
        :param int id: (required)
        :param str x_execution_id: Optional header to safely retry the request without accidentally performing the same operation twice. If a FlowRun with the same `executionId` already exist, the request will return a 304.
        :param bool run_async: Uses queue to run individual jobgroups asynchronously  and return immediately. Default value is false.
        :return: RunFlowResult
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id', 'x_execution_id', 'run_async']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method run_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `run_flow`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `run_flow`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'run_async' in params:
            query_params.append(('runAsync', params['run_async']))  # noqa: E501

        header_params = {}
        if 'x_execution_id' in params:
            header_params['x-execution-id'] = params['x_execution_id']  # noqa: E501

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
            '/v4/flows/{id}/run', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LRunFlowResult',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def validate_flow(self, id, **kwargs):  # noqa: E501
        """Validate Flow  # noqa: E501

        Validate a flow's outputs for recipe errors. For the given flow, validate recipe errors in all outputs and their dependencies. This API returns a list of all recipes contained in the flow or in referenced flows which will be executed if the flow is run or scheduled. For each returned recipe, the API specifies errors, if any, and the flowId and flowNodeId which contain the recipe.  <small>ref: [validateFlow](#operation/validateFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_flow(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: FlowValidateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.validate_flow_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.validate_flow_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def validate_flow_with_http_info(self, id, **kwargs):  # noqa: E501
        """Validate Flow  # noqa: E501

        Validate a flow's outputs for recipe errors. For the given flow, validate recipe errors in all outputs and their dependencies. This API returns a list of all recipes contained in the flow or in referenced flows which will be executed if the flow is run or scheduled. For each returned recipe, the API specifies errors, if any, and the flowId and flowNodeId which contain the recipe.  <small>ref: [validateFlow](#operation/validateFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.validate_flow_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: FlowValidateResponse
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
                    " to method validate_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `validate_flow`")  # noqa: E501

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
            '/v4/flows/{id}/validate', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LFlowValidateResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
