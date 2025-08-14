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


class ScheduleApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
     
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def count_schedules(self, **kwargs):  # noqa: E501
        """Count schedules  # noqa: E501

        count schedules owned by the current user  <small>ref: [countSchedules](#operation/countSchedules)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_schedules(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str filter: Filter schedules using the attached flow name
        :param list[str] task_type_filter: Filter schedules by task types. If not specified, all types are allowed.
        :param str asset_id: Filter by id of asset. The type of the asset must be defined with query parameter taskTypeFilter
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :return: Count
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.count_schedules_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.count_schedules_with_http_info(**kwargs)  # noqa: E501
            return data

    def count_schedules_with_http_info(self, **kwargs):  # noqa: E501
        """Count schedules  # noqa: E501

        count schedules owned by the current user  <small>ref: [countSchedules](#operation/countSchedules)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_schedules_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str filter: Filter schedules using the attached flow name
        :param list[str] task_type_filter: Filter schedules by task types. If not specified, all types are allowed.
        :param str asset_id: Filter by id of asset. The type of the asset must be defined with query parameter taskTypeFilter
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :return: Count
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['filter', 'task_type_filter', 'asset_id', 'filter_type', 'sort', 'include_count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method count_schedules" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501
        if 'task_type_filter' in params:
            query_params.append(('taskTypeFilter', params['task_type_filter']))  # noqa: E501
            collection_formats['taskTypeFilter'] = 'multi'  # noqa: E501
        if 'asset_id' in params:
            query_params.append(('assetId', params['asset_id']))  # noqa: E501
        if 'filter_type' in params:
            query_params.append(('filterType', params['filter_type']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
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
            '/v4/schedules/count', 'GET',
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

    def create_schedule(self, body, **kwargs):  # noqa: E501
        """Create a schedule  # noqa: E501

        Creates a new schedule. > ℹ️ **NOTE**: Cron expressions are using Quartz cron format, see [Quartz Cron Format](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html)  <small>ref: [createSchedule](#operation/createSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_schedule(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ScheduleCreateRequest body: (required)
        :return: Schedule
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_schedule_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_schedule_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_schedule_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create a schedule  # noqa: E501

        Creates a new schedule. > ℹ️ **NOTE**: Cron expressions are using Quartz cron format, see [Quartz Cron Format](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html)  <small>ref: [createSchedule](#operation/createSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_schedule_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ScheduleCreateRequest body: (required)
        :return: Schedule
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
                    " to method create_schedule" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_schedule`")  # noqa: E501

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
            '/v4/schedules', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LSchedule',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_schedule(self, id, **kwargs):  # noqa: E501
        """Delete schedule  # noqa: E501

        Delete an existing schedule  <small>ref: [deleteSchedule](#operation/deleteSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_schedule(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_schedule_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_schedule_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def delete_schedule_with_http_info(self, id, **kwargs):  # noqa: E501
        """Delete schedule  # noqa: E501

        Delete an existing schedule  <small>ref: [deleteSchedule](#operation/deleteSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_schedule_with_http_info(id, async_req=True)
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
                    " to method delete_schedule" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_schedule`")  # noqa: E501

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
            '/v4/schedules/{id}', 'DELETE',
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

    def disable_schedule(self, id, **kwargs):  # noqa: E501
        """Disable schedule  # noqa: E501

        Disable a schedule  <small>ref: [disableSchedule](#operation/disableSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.disable_schedule(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param object body:
        :return: Schedule
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.disable_schedule_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.disable_schedule_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def disable_schedule_with_http_info(self, id, **kwargs):  # noqa: E501
        """Disable schedule  # noqa: E501

        Disable a schedule  <small>ref: [disableSchedule](#operation/disableSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.disable_schedule_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param object body:
        :return: Schedule
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method disable_schedule" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `disable_schedule`")  # noqa: E501

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
            '/v4/schedules/{id}/disable', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LSchedule',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def enable_schedule(self, id, **kwargs):  # noqa: E501
        """Enable schedule  # noqa: E501

        Enable a schedule  <small>ref: [enableSchedule](#operation/enableSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.enable_schedule(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param object body:
        :return: Schedule
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.enable_schedule_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.enable_schedule_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def enable_schedule_with_http_info(self, id, **kwargs):  # noqa: E501
        """Enable schedule  # noqa: E501

        Enable a schedule  <small>ref: [enableSchedule](#operation/enableSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.enable_schedule_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param object body:
        :return: Schedule
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method enable_schedule" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `enable_schedule`")  # noqa: E501

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
            '/v4/schedules/{id}/enable', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LSchedule',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_schedule(self, id, **kwargs):  # noqa: E501
        """Get schedule  # noqa: E501

        Fetch a schedule  <small>ref: [getSchedule](#operation/getSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_schedule(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: ScheduleResponseWithTask
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_schedule_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_schedule_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_schedule_with_http_info(self, id, **kwargs):  # noqa: E501
        """Get schedule  # noqa: E501

        Fetch a schedule  <small>ref: [getSchedule](#operation/getSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_schedule_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: ScheduleResponseWithTask
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
                    " to method get_schedule" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_schedule`")  # noqa: E501

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
            '/v4/schedules/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LScheduleResponseWithTask',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_schedules(self, **kwargs):  # noqa: E501
        """List schedules  # noqa: E501

        list schedules owned by the current user  <small>ref: [listSchedules](#operation/listSchedules)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_schedules(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Maximum number of objects to fetch. Value from 1 to 1000. Default is 10.
        :param str filter: Filter schedules using the attached flow name
        :param list[str] task_type_filter: Filter schedules by task types. If not specified, all types are allowed.
        :param str asset_id: Filter by id of asset. The type of the asset must be defined with query parameter taskTypeFilter
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :return: ScheduleResponseWithTaskList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_schedules_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_schedules_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_schedules_with_http_info(self, **kwargs):  # noqa: E501
        """List schedules  # noqa: E501

        list schedules owned by the current user  <small>ref: [listSchedules](#operation/listSchedules)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_schedules_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Maximum number of objects to fetch. Value from 1 to 1000. Default is 10.
        :param str filter: Filter schedules using the attached flow name
        :param list[str] task_type_filter: Filter schedules by task types. If not specified, all types are allowed.
        :param str asset_id: Filter by id of asset. The type of the asset must be defined with query parameter taskTypeFilter
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :return: ScheduleResponseWithTaskList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['limit', 'filter', 'task_type_filter', 'asset_id', 'offset', 'filter_type', 'sort', 'include_count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_schedules" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501
        if 'task_type_filter' in params:
            query_params.append(('taskTypeFilter', params['task_type_filter']))  # noqa: E501
            collection_formats['taskTypeFilter'] = 'multi'  # noqa: E501
        if 'asset_id' in params:
            query_params.append(('assetId', params['asset_id']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'filter_type' in params:
            query_params.append(('filterType', params['filter_type']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
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
            '/v4/schedules', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LScheduleResponseWithTaskList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def transfer_ownership(self, body, **kwargs):  # noqa: E501
        """Transfer ownership  # noqa: E501

        Transfer list of schedules to another user  <small>ref: [transferOwnership](#operation/transferOwnership)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.transfer_ownership(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SchedulesTransferRequest body: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.transfer_ownership_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.transfer_ownership_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def transfer_ownership_with_http_info(self, body, **kwargs):  # noqa: E501
        """Transfer ownership  # noqa: E501

        Transfer list of schedules to another user  <small>ref: [transferOwnership](#operation/transferOwnership)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.transfer_ownership_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SchedulesTransferRequest body: (required)
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
                    " to method transfer_ownership" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `transfer_ownership`")  # noqa: E501

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
            '/v4/schedules/transferOwnership', 'POST',
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

    def update_schedule(self, body, id, **kwargs):  # noqa: E501
        """Update a schedule  # noqa: E501

        Update an existing schedule  <small>ref: [updateSchedule](#operation/updateSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_schedule(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ScheduleUpdateRequest body: (required)
        :param int id: (required)
        :return: UpdatedObjectSchema
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_schedule_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_schedule_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def update_schedule_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Update a schedule  # noqa: E501

        Update an existing schedule  <small>ref: [updateSchedule](#operation/updateSchedule)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_schedule_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ScheduleUpdateRequest body: (required)
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
                    " to method update_schedule" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_schedule`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_schedule`")  # noqa: E501

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
            '/v4/schedules/{id}', 'PUT',
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
