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


class PlanApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
     
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def count_plans(self, **kwargs):  # noqa: E501
        """Count plans  # noqa: E501

        Get number of plans  <small>ref: [countPlans](#operation/countPlans)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_plans(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ownership_filter: Filter plans by ownership.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :return: Count
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.count_plans_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.count_plans_with_http_info(**kwargs)  # noqa: E501
            return data

    def count_plans_with_http_info(self, **kwargs):  # noqa: E501
        """Count plans  # noqa: E501

        Get number of plans  <small>ref: [countPlans](#operation/countPlans)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_plans_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ownership_filter: Filter plans by ownership.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :return: Count
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ownership_filter', 'filter_type', 'filter_fields', 'filter']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method count_plans" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ownership_filter' in params:
            query_params.append(('ownershipFilter', params['ownership_filter']))  # noqa: E501
        if 'filter_type' in params:
            query_params.append(('filterType', params['filter_type']))  # noqa: E501
        if 'filter_fields' in params:
            query_params.append(('filterFields', params['filter_fields']))  # noqa: E501
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501

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
            '/v4/plans/count', 'GET',
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

    def create_plan(self, body, **kwargs):  # noqa: E501
        """Create plan  # noqa: E501

        Create a new plan  <small>ref: [createPlan](#operation/createPlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_plan(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PlanCreateRequest body: (required)
        :return: Plan
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_plan_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_plan_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_plan_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create plan  # noqa: E501

        Create a new plan  <small>ref: [createPlan](#operation/createPlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_plan_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PlanCreateRequest body: (required)
        :return: Plan
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
                    " to method create_plan" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_plan`")  # noqa: E501

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
            '/v4/plans', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LPlan',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_plan(self, id, **kwargs):  # noqa: E501
        """Delete plan  # noqa: E501

        Delete plan and remove associated schedules.  <small>ref: [deletePlan](#operation/deletePlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_plan(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_plan_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_plan_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def delete_plan_with_http_info(self, id, **kwargs):  # noqa: E501
        """Delete plan  # noqa: E501

        Delete plan and remove associated schedules.  <small>ref: [deletePlan](#operation/deletePlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_plan_with_http_info(id, async_req=True)
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
                    " to method delete_plan" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_plan`")  # noqa: E501

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
            '/v4/plans/{id}', 'DELETE',
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

    def delete_plan_permissions(self, id, subject_id, **kwargs):  # noqa: E501
        """Delete plan permissions for a user  # noqa: E501

        Delete permissions to a plan.  <small>ref: [deletePlanPermissions](#operation/deletePlanPermissions)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_plan_permissions(id, subject_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param int subject_id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_plan_permissions_with_http_info(id, subject_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_plan_permissions_with_http_info(id, subject_id, **kwargs)  # noqa: E501
            return data

    def delete_plan_permissions_with_http_info(self, id, subject_id, **kwargs):  # noqa: E501
        """Delete plan permissions for a user  # noqa: E501

        Delete permissions to a plan.  <small>ref: [deletePlanPermissions](#operation/deletePlanPermissions)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_plan_permissions_with_http_info(id, subject_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param int subject_id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'subject_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_plan_permissions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_plan_permissions`")  # noqa: E501
        # verify the required parameter 'subject_id' is set
        if ('subject_id' not in params or
                params['subject_id'] is None):
            raise ValueError("Missing the required parameter `subject_id` when calling `delete_plan_permissions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501
        if 'subject_id' in params:
            path_params['subjectId'] = params['subject_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/plans/{id}/permissions/{subjectId}', 'DELETE',
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

    def get_plan_package(self, id, **kwargs):  # noqa: E501
        """Export plan  # noqa: E501

        Retrieve a package containing the definition of the specified plan.  Response body is the contents of the package. Package contents are a ZIPped version of the plan definition.  The plan package can be used to import the plan in another environment. See the [Import Plan Package](#operation/importPackage) for more information.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [getPlanPackage](#operation/getPlanPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_plan_package(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str comment: comment to be displayed when plan is imported in a deployment package
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_plan_package_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_plan_package_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_plan_package_with_http_info(self, id, **kwargs):  # noqa: E501
        """Export plan  # noqa: E501

        Retrieve a package containing the definition of the specified plan.  Response body is the contents of the package. Package contents are a ZIPped version of the plan definition.  The plan package can be used to import the plan in another environment. See the [Import Plan Package](#operation/importPackage) for more information.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [getPlanPackage](#operation/getPlanPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_plan_package_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str comment: comment to be displayed when plan is imported in a deployment package
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
                    " to method get_plan_package" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_plan_package`")  # noqa: E501

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
            '/v4/plans/{id}/package', 'GET',
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

    def get_plan_permissions(self, id, **kwargs):  # noqa: E501
        """List permissions for plan  # noqa: E501

        Get a list of users with whom the plan is shared.  <small>ref: [getPlanPermissions](#operation/getPlanPermissions)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_plan_permissions(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: PlanPermissionPersonResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_plan_permissions_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_plan_permissions_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_plan_permissions_with_http_info(self, id, **kwargs):  # noqa: E501
        """List permissions for plan  # noqa: E501

        Get a list of users with whom the plan is shared.  <small>ref: [getPlanPermissions](#operation/getPlanPermissions)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_plan_permissions_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: PlanPermissionPersonResponse
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
                    " to method get_plan_permissions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_plan_permissions`")  # noqa: E501

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
            '/v4/plans/{id}/permissions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LPlanPermissionPersonResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_schedules_for_plan(self, id, **kwargs):  # noqa: E501
        """List plan schedules  # noqa: E501

        List of all schedules configured in the plan.  <small>ref: [getSchedulesForPlan](#operation/getSchedulesForPlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_schedules_for_plan(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: ScheduleHistoryList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_schedules_for_plan_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_schedules_for_plan_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_schedules_for_plan_with_http_info(self, id, **kwargs):  # noqa: E501
        """List plan schedules  # noqa: E501

        List of all schedules configured in the plan.  <small>ref: [getSchedulesForPlan](#operation/getSchedulesForPlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_schedules_for_plan_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: ScheduleHistoryList
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
                    " to method get_schedules_for_plan" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_schedules_for_plan`")  # noqa: E501

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
            '/v4/plans/{id}/schedules', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LScheduleHistoryList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def import_plan_package(self, **kwargs):  # noqa: E501
        """Import plan package  # noqa: E501

        Import the plan and associated flows from the given package. A `ZIP` file as exported by the [export plan endpoint](#operation/getPlanPackage) is accepted.  Before you import, you can perform a dry-run to check for errors. See [Import plan package - dry run](#operation/importPackageDryRun).  This endpoint accept a `multipart/form` content type.  Here is how to send the `ZIP` package using [curl](https://curl.haxx.se/). ``` curl -X POST https://us1.alteryxcloud.com/v4/plans/package \\ -H 'authorization: Bearer <api-token>' \\ -H 'content-type: multipart/form-data' \\ -F 'data=@path/to/plan-package.zip' ```  The response lists the objects that have been created.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [importPlanPackage](#operation/importPlanPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_plan_package(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportPlanDataRequest body:
        :param int folder_id:
        :param bool from_ui: If true, will return the list of imported environment parameters for confirmation if any are referenced in the plan.
        :return: ImportPlanPackageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.import_plan_package_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.import_plan_package_with_http_info(**kwargs)  # noqa: E501
            return data

    def import_plan_package_with_http_info(self, **kwargs):  # noqa: E501
        """Import plan package  # noqa: E501

        Import the plan and associated flows from the given package. A `ZIP` file as exported by the [export plan endpoint](#operation/getPlanPackage) is accepted.  Before you import, you can perform a dry-run to check for errors. See [Import plan package - dry run](#operation/importPackageDryRun).  This endpoint accept a `multipart/form` content type.  Here is how to send the `ZIP` package using [curl](https://curl.haxx.se/). ``` curl -X POST https://us1.alteryxcloud.com/v4/plans/package \\ -H 'authorization: Bearer <api-token>' \\ -H 'content-type: multipart/form-data' \\ -F 'data=@path/to/plan-package.zip' ```  The response lists the objects that have been created.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [importPlanPackage](#operation/importPlanPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_plan_package_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportPlanDataRequest body:
        :param int folder_id:
        :param bool from_ui: If true, will return the list of imported environment parameters for confirmation if any are referenced in the plan.
        :return: ImportPlanPackageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'folder_id', 'from_ui']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method import_plan_package" % key
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
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/plans/package', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LImportPlanPackageResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def import_plan_package(self, **kwargs):  # noqa: E501
        """Import plan package  # noqa: E501

        Import the plan and associated flows from the given package. A `ZIP` file as exported by the [export plan endpoint](#operation/getPlanPackage) is accepted.  Before you import, you can perform a dry-run to check for errors. See [Import plan package - dry run](#operation/importPackageDryRun).  This endpoint accept a `multipart/form` content type.  Here is how to send the `ZIP` package using [curl](https://curl.haxx.se/). ``` curl -X POST https://us1.alteryxcloud.com/v4/plans/package \\ -H 'authorization: Bearer <api-token>' \\ -H 'content-type: multipart/form-data' \\ -F 'data=@path/to/plan-package.zip' ```  The response lists the objects that have been created.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [importPlanPackage](#operation/importPlanPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_plan_package(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportPlanPackageRequestZip file:
        :param list[LEnvironmentParameterMapping] environment_parameter_mapping:
        :param list[LConnectionIdMapping] connection_id_mapping:
        :param int folder_id:
        :param bool from_ui: If true, will return the list of imported environment parameters for confirmation if any are referenced in the plan.
        :return: ImportPlanPackageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.import_plan_package_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.import_plan_package_with_http_info(**kwargs)  # noqa: E501
            return data

    def import_plan_package_with_http_info(self, **kwargs):  # noqa: E501
        """Import plan package  # noqa: E501

        Import the plan and associated flows from the given package. A `ZIP` file as exported by the [export plan endpoint](#operation/getPlanPackage) is accepted.  Before you import, you can perform a dry-run to check for errors. See [Import plan package - dry run](#operation/importPackageDryRun).  This endpoint accept a `multipart/form` content type.  Here is how to send the `ZIP` package using [curl](https://curl.haxx.se/). ``` curl -X POST https://us1.alteryxcloud.com/v4/plans/package \\ -H 'authorization: Bearer <api-token>' \\ -H 'content-type: multipart/form-data' \\ -F 'data=@path/to/plan-package.zip' ```  The response lists the objects that have been created.  **Quotas**:<br/>20 req./user/min, 40 req./workspace/min  <small>ref: [importPlanPackage](#operation/importPlanPackage)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.import_plan_package_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportPlanPackageRequestZip file:
        :param list[LEnvironmentParameterMapping] environment_parameter_mapping:
        :param list[LConnectionIdMapping] connection_id_mapping:
        :param int folder_id:
        :param bool from_ui: If true, will return the list of imported environment parameters for confirmation if any are referenced in the plan.
        :return: ImportPlanPackageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file', 'environment_parameter_mapping', 'connection_id_mapping', 'folder_id', 'from_ui']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method import_plan_package" % key
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
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v4/plans/package', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LImportPlanPackageResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_plans(self, **kwargs):  # noqa: E501
        """List plans  # noqa: E501

        List existing plans  <small>ref: [listPlans](#operation/listPlans)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_plans(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted7 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param bool include_associated_people: If true, the returned plans will include a list of people with access.
        :param str ownership_filter: Filter plans by ownership. Valid values are 'all', 'shared', and 'owned'.
        :return: PlanList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_plans_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_plans_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_plans_with_http_info(self, **kwargs):  # noqa: E501
        """List plans  # noqa: E501

        List existing plans  <small>ref: [listPlans](#operation/listPlans)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_plans_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted7 include_deleted: Whether to include all or some of the nested deleted objects.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter_fields: comma-separated list of fields to match the `filter` parameter against.
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param bool include_associated_people: If true, the returned plans will include a list of people with access.
        :param str ownership_filter: Filter plans by ownership. Valid values are 'all', 'shared', and 'owned'.
        :return: PlanList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['fields', 'embed', 'include_deleted', 'limit', 'offset', 'filter_type', 'sort', 'filter_fields', 'filter', 'include_count', 'include_associated_people', 'ownership_filter']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_plans" % key
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
        if 'include_associated_people' in params:
            query_params.append(('includeAssociatedPeople', params['include_associated_people']))  # noqa: E501
        if 'ownership_filter' in params:
            query_params.append(('ownershipFilter', params['ownership_filter']))  # noqa: E501

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
            '/v4/plans', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LPlanList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def plan_run_parameters(self, id, **kwargs):  # noqa: E501
        """List run parameters  # noqa: E501

        List run parameters of a plan. Parameters will be grouped by plannode. Each element in the returned list will only contain resources that have run parameters defined.  <small>ref: [planRunParameters](#operation/planRunParameters)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.plan_run_parameters(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: RunParameterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.plan_run_parameters_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.plan_run_parameters_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def plan_run_parameters_with_http_info(self, id, **kwargs):  # noqa: E501
        """List run parameters  # noqa: E501

        List run parameters of a plan. Parameters will be grouped by plannode. Each element in the returned list will only contain resources that have run parameters defined.  <small>ref: [planRunParameters](#operation/planRunParameters)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.plan_run_parameters_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: RunParameterResponse
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
                    " to method plan_run_parameters" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `plan_run_parameters`")  # noqa: E501

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
            '/v4/plans/{id}/runParameters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LRunParameterResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read_full(self, id, **kwargs):  # noqa: E501
        """Read plan with all attributes  # noqa: E501

        Read full plan with all its nodes, tasks, and edges.  <small>ref: [readFull](#operation/readFull)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_full(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted38 include_deleted: Whether to include all or some of the nested deleted objects.
        :param bool include_associated_people: If true, the returned plan will include a list of people with access.
        :param bool include_creator_info: If true, the returned plan will include info about the creators of the flows and plan such as name and email address.
        :return: Plan
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.read_full_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.read_full_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def read_full_with_http_info(self, id, **kwargs):  # noqa: E501
        """Read plan with all attributes  # noqa: E501

        Read full plan with all its nodes, tasks, and edges.  <small>ref: [readFull](#operation/readFull)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_full_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted38 include_deleted: Whether to include all or some of the nested deleted objects.
        :param bool include_associated_people: If true, the returned plan will include a list of people with access.
        :param bool include_creator_info: If true, the returned plan will include info about the creators of the flows and plan such as name and email address.
        :return: Plan
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'fields', 'embed', 'include_deleted', 'include_associated_people', 'include_creator_info']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read_full" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `read_full`")  # noqa: E501

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
        if 'include_associated_people' in params:
            query_params.append(('includeAssociatedPeople', params['include_associated_people']))  # noqa: E501
        if 'include_creator_info' in params:
            query_params.append(('includeCreatorInfo', params['include_creator_info']))  # noqa: E501

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
            '/v4/plans/{id}/full', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LPlan',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def run_plan(self, id, **kwargs):  # noqa: E501
        """Run plan  # noqa: E501

        Run the plan. A new snapshot will be created if required.  If some flows or outputs referenced by the plan tasks have been deleted, it will return a `MissingFlowReferences` validation status.  If the plan is valid, it will be queued for execution. This endpoint returns a `planSnapshotRunId` that can be used to track the plan execution status using [getPlanSnapshotRun](#operation/getPlanSnapshotRun).  **Quotas**:<br/>30 req./user/min, 60 req./workspace/min  <small>ref: [runPlan](#operation/runPlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.run_plan(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param RunPlanBody body:
        :param str x_execution_id: Optional header to safely retry the request without accidentally performing the same operation twice. If a `PlanSnapshotRun` with the same `executionId` already exists, the request will return a `304`.
        :return: RunPlanResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.run_plan_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.run_plan_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def run_plan_with_http_info(self, id, **kwargs):  # noqa: E501
        """Run plan  # noqa: E501

        Run the plan. A new snapshot will be created if required.  If some flows or outputs referenced by the plan tasks have been deleted, it will return a `MissingFlowReferences` validation status.  If the plan is valid, it will be queued for execution. This endpoint returns a `planSnapshotRunId` that can be used to track the plan execution status using [getPlanSnapshotRun](#operation/getPlanSnapshotRun).  **Quotas**:<br/>30 req./user/min, 60 req./workspace/min  <small>ref: [runPlan](#operation/runPlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.run_plan_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param RunPlanBody body:
        :param str x_execution_id: Optional header to safely retry the request without accidentally performing the same operation twice. If a `PlanSnapshotRun` with the same `executionId` already exists, the request will return a `304`.
        :return: RunPlanResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'body', 'x_execution_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method run_plan" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `run_plan`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

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
            '/v4/plans/{id}/run', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LRunPlanResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def share_plan(self, body, id, **kwargs):  # noqa: E501
        """Share Plan  # noqa: E501

        Share a plan with other users. Collaborators can edit the plan.  <small>ref: [sharePlan](#operation/sharePlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.share_plan(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SharePlanRequest body: (required)
        :param int id: (required)
        :return: SharePlanResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.share_plan_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.share_plan_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def share_plan_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Share Plan  # noqa: E501

        Share a plan with other users. Collaborators can edit the plan.  <small>ref: [sharePlan](#operation/sharePlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.share_plan_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SharePlanRequest body: (required)
        :param int id: (required)
        :return: SharePlanResponse
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
                    " to method share_plan" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `share_plan`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `share_plan`")  # noqa: E501

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
            '/v4/plans/{id}/permissions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LSharePlanResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_plan(self, body, id, **kwargs):  # noqa: E501
        """Update plan  # noqa: E501

        Update plan properties, e.g. name and description  <small>ref: [updatePlan](#operation/updatePlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_plan(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PlanUpdateRequest body: (required)
        :param int id: (required)
        :return: Plan
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_plan_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_plan_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def update_plan_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Update plan  # noqa: E501

        Update plan properties, e.g. name and description  <small>ref: [updatePlan](#operation/updatePlan)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_plan_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PlanUpdateRequest body: (required)
        :param int id: (required)
        :return: Plan
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
                    " to method update_plan" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_plan`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_plan`")  # noqa: E501

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
            '/v4/plans/{id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LPlan',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
