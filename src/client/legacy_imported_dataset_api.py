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


class ImportedDatasetApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
     
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_imported_dataset_to_flow(self, body, id, **kwargs):  # noqa: E501
        """Add Imported Dataset to Flow  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Add the specified imported dataset to a flow based on its internal identifier. > ℹ️ **NOTE**: Datasets can be added to flows based on the permissions of the access token used on this endpoint. Datasets can be added to flows that are shared by the user.  <small>ref: [addImportedDatasetToFlow](#operation/addImportedDatasetToFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_imported_dataset_to_flow(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AddDatasetToFlowRequest body: (required)
        :param int id: (required)
        :return: ParsingNode
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.add_imported_dataset_to_flow_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.add_imported_dataset_to_flow_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def add_imported_dataset_to_flow_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Add Imported Dataset to Flow  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Add the specified imported dataset to a flow based on its internal identifier. > ℹ️ **NOTE**: Datasets can be added to flows based on the permissions of the access token used on this endpoint. Datasets can be added to flows that are shared by the user.  <small>ref: [addImportedDatasetToFlow](#operation/addImportedDatasetToFlow)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_imported_dataset_to_flow_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param AddDatasetToFlowRequest body: (required)
        :param int id: (required)
        :return: ParsingNode
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
                    " to method add_imported_dataset_to_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `add_imported_dataset_to_flow`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `add_imported_dataset_to_flow`")  # noqa: E501

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
            '/v4/importedDatasets/{id}/addToFlow', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LParsingNode',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def async_refresh_schema(self, id, **kwargs):  # noqa: E501
        """Fetch and update latest datasource schema  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Fetches and updates the latest schema of a datasource  <small>ref: [asyncRefreshSchema](#operation/asyncRefreshSchema)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.async_refresh_schema(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param object body:
        :param str format: Control format behaviour for datasets.
        :param str header_strategy: Control header behaviour for datasets.
        :param bool sanitize_column_names: Control sanitizeColumnNames behaviour for datasets.
        :return: AsyncRefreshSchemaResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.async_refresh_schema_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.async_refresh_schema_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def async_refresh_schema_with_http_info(self, id, **kwargs):  # noqa: E501
        """Fetch and update latest datasource schema  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Fetches and updates the latest schema of a datasource  <small>ref: [asyncRefreshSchema](#operation/asyncRefreshSchema)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.async_refresh_schema_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param object body:
        :param str format: Control format behaviour for datasets.
        :param str header_strategy: Control header behaviour for datasets.
        :param bool sanitize_column_names: Control sanitizeColumnNames behaviour for datasets.
        :return: AsyncRefreshSchemaResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'body', 'format', 'header_strategy', 'sanitize_column_names']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method async_refresh_schema" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `async_refresh_schema`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'header_strategy' in params:
            query_params.append(('headerStrategy', params['header_strategy']))  # noqa: E501
        if 'sanitize_column_names' in params:
            query_params.append(('sanitizeColumnNames', params['sanitize_column_names']))  # noqa: E501

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
            '/v4/importedDatasets/{id}/asyncRefreshSchema', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LAsyncRefreshSchemaResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def copy_data_source(self, body, id, **kwargs):  # noqa: E501
        """Copy imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Create a copy of an imported dataset  <small>ref: [copyDataSource](#operation/copyDataSource)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.copy_data_source(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CopyImportedDatasetRequest body: (required)
        :param int id: (required)
        :return: DataSource
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.copy_data_source_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.copy_data_source_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def copy_data_source_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Copy imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Create a copy of an imported dataset  <small>ref: [copyDataSource](#operation/copyDataSource)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.copy_data_source_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CopyImportedDatasetRequest body: (required)
        :param int id: (required)
        :return: DataSource
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
                    " to method copy_data_source" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `copy_data_source`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `copy_data_source`")  # noqa: E501

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
            '/v4/importedDatasets/{id}/copy', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LDataSource',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def count_dataset_library(self, **kwargs):  # noqa: E501
        """Count Datasets  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Count Alteryx Analytics Cloud datasets.   Gives counts for various types of datasets matching the provided filters.  <small>ref: [countDatasetLibrary](#operation/countDatasetLibrary)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_dataset_library(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ownership_filter: Which set of datasets to count. One of [`all`, `shared`, `owned`]
        :param bool schematized: If included, filter to only show schematized imported datasets.
        :param int current_flow_id: Required for including `recipes`. If included, and datasetsFilter includes `recipes`, response will include recipes in the current flow.
        :param int datasource_flow_id: When included, filter included datasets to only include those associated to the given flow.
        :param int flow_id: When provided, count datasets associated with this flow before other datasets.
        :param DatasetsFilter1 datasets_filter: Which types of datasets to list. Valid choices are: [`all`, `imported`, `reference`, `recipe`]
        :param str filter: Value for fuzzy-filtering objects. See `filterFields`.
        :param int user_id_filter: allows admin to filter datasets based on userId
        :return: DatasetLibraryCount
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.count_dataset_library_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.count_dataset_library_with_http_info(**kwargs)  # noqa: E501
            return data

    def count_dataset_library_with_http_info(self, **kwargs):  # noqa: E501
        """Count Datasets  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Count Alteryx Analytics Cloud datasets.   Gives counts for various types of datasets matching the provided filters.  <small>ref: [countDatasetLibrary](#operation/countDatasetLibrary)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.count_dataset_library_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ownership_filter: Which set of datasets to count. One of [`all`, `shared`, `owned`]
        :param bool schematized: If included, filter to only show schematized imported datasets.
        :param int current_flow_id: Required for including `recipes`. If included, and datasetsFilter includes `recipes`, response will include recipes in the current flow.
        :param int datasource_flow_id: When included, filter included datasets to only include those associated to the given flow.
        :param int flow_id: When provided, count datasets associated with this flow before other datasets.
        :param DatasetsFilter1 datasets_filter: Which types of datasets to list. Valid choices are: [`all`, `imported`, `reference`, `recipe`]
        :param str filter: Value for fuzzy-filtering objects. See `filterFields`.
        :param int user_id_filter: allows admin to filter datasets based on userId
        :return: DatasetLibraryCount
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ownership_filter', 'schematized', 'current_flow_id', 'datasource_flow_id', 'flow_id', 'datasets_filter', 'filter', 'user_id_filter']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method count_dataset_library" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ownership_filter' in params:
            query_params.append(('ownershipFilter', params['ownership_filter']))  # noqa: E501
        if 'schematized' in params:
            query_params.append(('schematized', params['schematized']))  # noqa: E501
        if 'current_flow_id' in params:
            query_params.append(('currentFlowId', params['current_flow_id']))  # noqa: E501
        if 'datasource_flow_id' in params:
            query_params.append(('datasourceFlowId', params['datasource_flow_id']))  # noqa: E501
        if 'flow_id' in params:
            query_params.append(('flowId', params['flow_id']))  # noqa: E501
        if 'datasets_filter' in params:
            query_params.append(('datasetsFilter', params['datasets_filter']))  # noqa: E501
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501
        if 'user_id_filter' in params:
            query_params.append(('userIdFilter', params['user_id_filter']))  # noqa: E501

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
            '/v4/datasetLibrary/count', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LDatasetLibraryCount',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_imported_dataset(self, body, **kwargs):  # noqa: E501
        """Create imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Create an imported dataset from an available resource. Created dataset is owned by the authenticated user.  In general, importing a file is done using the following payload: ``` {   \"uri\": \"protocol://path-to-file\",   \"name\": \"my dataset\",   \"detectStructure\": true } ```  See more examples in the *Request Samples* section.  > ✅ **TIP**: When an imported dataset is created via API, it is always imported as an unstructured dataset by default. To import a dataset with the inferred recipe, add `detectStructure: true` in the payload.   > ℹ️ **NOTE**: Do not create an imported dataset from a file that is being used by another imported dataset. If you delete the newly created imported dataset, the file is removed, and the other dataset is corrupted. Use a new file or make a copy of the first file first.  > ℹ️ **NOTE**: Importing a Microsoft Excel file or a file that need to be converted using the API is not supported yet.    **Quotas**:<br/>40 req./user/min, 60 req./workspace/min  <small>ref: [createImportedDataset](#operation/createImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_imported_dataset(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportedDatasetCreateRequest body: (required)
        :return: ImportedDataset
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_imported_dataset_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_imported_dataset_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_imported_dataset_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Create an imported dataset from an available resource. Created dataset is owned by the authenticated user.  In general, importing a file is done using the following payload: ``` {   \"uri\": \"protocol://path-to-file\",   \"name\": \"my dataset\",   \"detectStructure\": true } ```  See more examples in the *Request Samples* section.  > ✅ **TIP**: When an imported dataset is created via API, it is always imported as an unstructured dataset by default. To import a dataset with the inferred recipe, add `detectStructure: true` in the payload.   > ℹ️ **NOTE**: Do not create an imported dataset from a file that is being used by another imported dataset. If you delete the newly created imported dataset, the file is removed, and the other dataset is corrupted. Use a new file or make a copy of the first file first.  > ℹ️ **NOTE**: Importing a Microsoft Excel file or a file that need to be converted using the API is not supported yet.    **Quotas**:<br/>40 req./user/min, 60 req./workspace/min  <small>ref: [createImportedDataset](#operation/createImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_imported_dataset_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportedDatasetCreateRequest body: (required)
        :return: ImportedDataset
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
                    " to method create_imported_dataset" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_imported_dataset`")  # noqa: E501

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
            '/v4/importedDatasets', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LImportedDataset',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_imported_dataset(self, id, **kwargs):  # noqa: E501
        """Delete imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Delete an existing imported dataset.  <small>ref: [deleteImportedDataset](#operation/deleteImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_imported_dataset(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_imported_dataset_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_imported_dataset_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def delete_imported_dataset_with_http_info(self, id, **kwargs):  # noqa: E501
        """Delete imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Delete an existing imported dataset.  <small>ref: [deleteImportedDataset](#operation/deleteImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_imported_dataset_with_http_info(id, async_req=True)
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
                    " to method delete_imported_dataset" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_imported_dataset`")  # noqa: E501

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
            '/v4/importedDatasets/{id}', 'DELETE',
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

    def get_imported_dataset(self, id, **kwargs):  # noqa: E501
        """Get imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Get the specified imported dataset.  Use the following embedded reference to embed in the response data about the connection used to acquire the source dataset if it was created from a custom connection. See [embedding resources](#section/Overview/Embedding-Resources) for more information. ``` /v4/importedDatasets/{id}?embed=connection ```  <small>ref: [getImportedDataset](#operation/getImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_imported_dataset(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted26 include_deleted: Whether to include all or some of the nested deleted objects.
        :param bool include_associated_subjects: If includeAssociatedSubjects is true, it will include entitlement associated subjects in the response
        :return: ImportedDataset
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_imported_dataset_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_imported_dataset_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_imported_dataset_with_http_info(self, id, **kwargs):  # noqa: E501
        """Get imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Get the specified imported dataset.  Use the following embedded reference to embed in the response data about the connection used to acquire the source dataset if it was created from a custom connection. See [embedding resources](#section/Overview/Embedding-Resources) for more information. ``` /v4/importedDatasets/{id}?embed=connection ```  <small>ref: [getImportedDataset](#operation/getImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_imported_dataset_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :param str fields: Semi-colons-separated list of fields
        :param str embed: Comma-separated list of objects to pull in as part of the response. See [Embedding Resources](#section/Overview/Embedding-Resources) for more information.
        :param IncludeDeleted26 include_deleted: Whether to include all or some of the nested deleted objects.
        :param bool include_associated_subjects: If includeAssociatedSubjects is true, it will include entitlement associated subjects in the response
        :return: ImportedDataset
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'fields', 'embed', 'include_deleted', 'include_associated_subjects']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_imported_dataset" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_imported_dataset`")  # noqa: E501

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
        if 'include_associated_subjects' in params:
            query_params.append(('includeAssociatedSubjects', params['include_associated_subjects']))  # noqa: E501

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
            '/v4/importedDatasets/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LImportedDataset',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_inputs_for_output_object(self, id, **kwargs):  # noqa: E501
        """List inputs for Output Object  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  List all the inputs that are linked to this output object. Also include data sources that are present in referenced flows.  <small>ref: [getInputsForOutputObject](#operation/getInputsForOutputObject)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_inputs_for_output_object(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: (required)
        :return: ImportedDatasetList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_inputs_for_output_object_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_inputs_for_output_object_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_inputs_for_output_object_with_http_info(self, id, **kwargs):  # noqa: E501
        """List inputs for Output Object  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  List all the inputs that are linked to this output object. Also include data sources that are present in referenced flows.  <small>ref: [getInputsForOutputObject](#operation/getInputsForOutputObject)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_inputs_for_output_object_with_http_info(id, async_req=True)
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
                    " to method get_inputs_for_output_object" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_inputs_for_output_object`")  # noqa: E501

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
            '/v4/outputObjects/{id}/inputs', 'GET',
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

    def list_dataset_library(self, datasets_filter, **kwargs):  # noqa: E501
        """List Datasets  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  List Alteryx Analytics Cloud datasets.   This can be used to list both imported and reference datasets throughout the system, as well as recipes in a given flow.  <small>ref: [listDatasetLibrary](#operation/listDatasetLibrary)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_dataset_library(datasets_filter, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DatasetsFilter datasets_filter: Which types of datasets to list. Valid choices are: [`all`, `imported`, `reference`, `recipe`] (required)
        :param str ownership_filter: Which set of datasets to list. One of [`all`, `shared`, `owned`]
        :param bool schematized: If included, filter to only show schematized imported datasets.
        :param int current_flow_id: Required for including `recipes`. If included, and datasetsFilter includes `recipes`, response will include recipes in the current flow.
        :param int datasource_flow_id: When included, filter included datasets to only include those associated to the given flow.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param int flow_id: When provided, list datasets associated with this flow before other datasets.
        :param int user_id_filter: allows admin to filter datasets based on userId
        :param bool include_associated_subjects: If includeAssociatedSubjects is true, it will include entitlements associated subjects in the response
        :param bool hidden: If hidden is set to true, the response will include all datasets (including hidden).
        :param int connection_id: When provided, list datasets associated with this connectionId. This can also be used along with the parameter baseStorage
        :param bool base_storage: When provided, list datasets from base storage. This can also be used along with the parameter connectionId
        :return: DatasetLibraryListObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_dataset_library_with_http_info(datasets_filter, **kwargs)  # noqa: E501
        else:
            (data) = self.list_dataset_library_with_http_info(datasets_filter, **kwargs)  # noqa: E501
            return data

    def list_dataset_library_with_http_info(self, datasets_filter, **kwargs):  # noqa: E501
        """List Datasets  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  List Alteryx Analytics Cloud datasets.   This can be used to list both imported and reference datasets throughout the system, as well as recipes in a given flow.  <small>ref: [listDatasetLibrary](#operation/listDatasetLibrary)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_dataset_library_with_http_info(datasets_filter, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DatasetsFilter datasets_filter: Which types of datasets to list. Valid choices are: [`all`, `imported`, `reference`, `recipe`] (required)
        :param str ownership_filter: Which set of datasets to list. One of [`all`, `shared`, `owned`]
        :param bool schematized: If included, filter to only show schematized imported datasets.
        :param int current_flow_id: Required for including `recipes`. If included, and datasetsFilter includes `recipes`, response will include recipes in the current flow.
        :param int datasource_flow_id: When included, filter included datasets to only include those associated to the given flow.
        :param int limit: Maximum number of objects to fetch.
        :param int offset: Offset after which to start returning objects. For use with `limit`.
        :param str filter_type: Defined the filter type, one of [\"fuzzy\", \"contains\", \"exact\", \"exactIgnoreCase\"]. For use with `filter`.
        :param str sort: Defines sort order for returned objects
        :param str filter: Value for filtering objects. See `filterFields`.
        :param bool include_count: If includeCount is true, it will include the total number of objects as a count object in the response
        :param int flow_id: When provided, list datasets associated with this flow before other datasets.
        :param int user_id_filter: allows admin to filter datasets based on userId
        :param bool include_associated_subjects: If includeAssociatedSubjects is true, it will include entitlements associated subjects in the response
        :param bool hidden: If hidden is set to true, the response will include all datasets (including hidden).
        :param int connection_id: When provided, list datasets associated with this connectionId. This can also be used along with the parameter baseStorage
        :param bool base_storage: When provided, list datasets from base storage. This can also be used along with the parameter connectionId
        :return: DatasetLibraryListObject
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['datasets_filter', 'ownership_filter', 'schematized', 'current_flow_id', 'datasource_flow_id', 'limit', 'offset', 'filter_type', 'sort', 'filter', 'include_count', 'flow_id', 'user_id_filter', 'include_associated_subjects', 'hidden', 'connection_id', 'base_storage']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_dataset_library" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'datasets_filter' is set
        if ('datasets_filter' not in params or
                params['datasets_filter'] is None):
            raise ValueError("Missing the required parameter `datasets_filter` when calling `list_dataset_library`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ownership_filter' in params:
            query_params.append(('ownershipFilter', params['ownership_filter']))  # noqa: E501
        if 'schematized' in params:
            query_params.append(('schematized', params['schematized']))  # noqa: E501
        if 'current_flow_id' in params:
            query_params.append(('currentFlowId', params['current_flow_id']))  # noqa: E501
        if 'datasource_flow_id' in params:
            query_params.append(('datasourceFlowId', params['datasource_flow_id']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'filter_type' in params:
            query_params.append(('filterType', params['filter_type']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501
        if 'include_count' in params:
            query_params.append(('includeCount', params['include_count']))  # noqa: E501
        if 'datasets_filter' in params:
            query_params.append(('datasetsFilter', params['datasets_filter']))  # noqa: E501
        if 'flow_id' in params:
            query_params.append(('flowId', params['flow_id']))  # noqa: E501
        if 'user_id_filter' in params:
            query_params.append(('userIdFilter', params['user_id_filter']))  # noqa: E501
        if 'include_associated_subjects' in params:
            query_params.append(('includeAssociatedSubjects', params['include_associated_subjects']))  # noqa: E501
        if 'hidden' in params:
            query_params.append(('hidden', params['hidden']))  # noqa: E501
        if 'connection_id' in params:
            query_params.append(('connectionId', params['connection_id']))  # noqa: E501
        if 'base_storage' in params:
            query_params.append(('baseStorage', params['base_storage']))  # noqa: E501

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
            '/v4/datasetLibrary', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LDatasetLibraryListObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def patch_imported_dataset(self, body, id, **kwargs):  # noqa: E501
        """Patch imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Modify the specified imported dataset. Only the name and description properties should be modified.  <small>ref: [patchImportedDataset](#operation/patchImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_imported_dataset(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportedDatasetUpdateRequest body: (required)
        :param int id: (required)
        :return: ImportedDataset
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.patch_imported_dataset_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.patch_imported_dataset_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def patch_imported_dataset_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Patch imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Modify the specified imported dataset. Only the name and description properties should be modified.  <small>ref: [patchImportedDataset](#operation/patchImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_imported_dataset_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ImportedDatasetUpdateRequest body: (required)
        :param int id: (required)
        :return: ImportedDataset
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
                    " to method patch_imported_dataset" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `patch_imported_dataset`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `patch_imported_dataset`")  # noqa: E501

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
            '/v4/importedDatasets/{id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LImportedDataset',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_imported_dataset(self, body, id, **kwargs):  # noqa: E501
        """Update imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Modify the specified imported dataset. Name, path, bucket etc. for gcs can be modified.  > ℹ️ **NOTE**: Samples will not be updated for the recipes. This results in the recipe showing samples of the older data.  <small>ref: [updateImportedDataset](#operation/updateImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_imported_dataset(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateImportedDatasetRequest body: (required)
        :param int id: (required)
        :return: ImportedDataset
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_imported_dataset_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_imported_dataset_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def update_imported_dataset_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """Update imported dataset  # noqa: E501

        > ⚠️ **Deprecated**: Please migrate to newer APIs before 31st Dec 2024. New API link - upcoming  Modify the specified imported dataset. Name, path, bucket etc. for gcs can be modified.  > ℹ️ **NOTE**: Samples will not be updated for the recipes. This results in the recipe showing samples of the older data.  <small>ref: [updateImportedDataset](#operation/updateImportedDataset)</small>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_imported_dataset_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateImportedDatasetRequest body: (required)
        :param int id: (required)
        :return: ImportedDataset
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
                    " to method update_imported_dataset" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_imported_dataset`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_imported_dataset`")  # noqa: E501

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
            '/v4/importedDatasets/{id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LImportedDataset',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
