# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

import pprint
import re  # noqa: F401

import six

class LRuntimeMetadataInfo(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'default_type_treatment': 'LTypeClassificationInfo',
        'type_map': 'list[object]',
        'metadata_accessors': 'object',
        'path_metadata': 'object',
        'limit': 'object',
        'error_handlers': 'object',
        'import_performance': 'object'
    }

    attribute_map = {
        'default_type_treatment': 'defaultTypeTreatment',
        'type_map': 'typeMap',
        'metadata_accessors': 'metadataAccessors',
        'path_metadata': 'pathMetadata',
        'limit': 'limit',
        'error_handlers': 'errorHandlers',
        'import_performance': 'importPerformance'
    }

    def __init__(self, default_type_treatment=None, type_map=None, metadata_accessors=None, path_metadata=None, limit=None, error_handlers=None, import_performance=None):  # noqa: E501
        """LRuntimeMetadataInfo - a model defined in Swagger"""  # noqa: E501
        self._default_type_treatment = None
        self._type_map = None
        self._metadata_accessors = None
        self._path_metadata = None
        self._limit = None
        self._error_handlers = None
        self._import_performance = None
        self.discriminator = None
        if default_type_treatment is not None:
            self.default_type_treatment = default_type_treatment
        if type_map is not None:
            self.type_map = type_map
        if metadata_accessors is not None:
            self.metadata_accessors = metadata_accessors
        if path_metadata is not None:
            self.path_metadata = path_metadata
        if limit is not None:
            self.limit = limit
        if error_handlers is not None:
            self.error_handlers = error_handlers
        if import_performance is not None:
            self.import_performance = import_performance

    @property
    def default_type_treatment(self):
        """Gets the default_type_treatment of this LRuntimeMetadataInfo.  # noqa: E501


        :return: The default_type_treatment of this LRuntimeMetadataInfo.  # noqa: E501
        :rtype: LTypeClassificationInfo
        """
        return self._default_type_treatment

    @default_type_treatment.setter
    def default_type_treatment(self, default_type_treatment):
        """Sets the default_type_treatment of this LRuntimeMetadataInfo.


        :param default_type_treatment: The default_type_treatment of this LRuntimeMetadataInfo.  # noqa: E501
        :type: LTypeClassificationInfo
        """

        self._default_type_treatment = default_type_treatment

    @property
    def type_map(self):
        """Gets the type_map of this LRuntimeMetadataInfo.  # noqa: E501


        :return: The type_map of this LRuntimeMetadataInfo.  # noqa: E501
        :rtype: list[object]
        """
        return self._type_map

    @type_map.setter
    def type_map(self, type_map):
        """Sets the type_map of this LRuntimeMetadataInfo.


        :param type_map: The type_map of this LRuntimeMetadataInfo.  # noqa: E501
        :type: list[object]
        """

        self._type_map = type_map

    @property
    def metadata_accessors(self):
        """Gets the metadata_accessors of this LRuntimeMetadataInfo.  # noqa: E501


        :return: The metadata_accessors of this LRuntimeMetadataInfo.  # noqa: E501
        :rtype: object
        """
        return self._metadata_accessors

    @metadata_accessors.setter
    def metadata_accessors(self, metadata_accessors):
        """Sets the metadata_accessors of this LRuntimeMetadataInfo.


        :param metadata_accessors: The metadata_accessors of this LRuntimeMetadataInfo.  # noqa: E501
        :type: object
        """

        self._metadata_accessors = metadata_accessors

    @property
    def path_metadata(self):
        """Gets the path_metadata of this LRuntimeMetadataInfo.  # noqa: E501


        :return: The path_metadata of this LRuntimeMetadataInfo.  # noqa: E501
        :rtype: object
        """
        return self._path_metadata

    @path_metadata.setter
    def path_metadata(self, path_metadata):
        """Sets the path_metadata of this LRuntimeMetadataInfo.


        :param path_metadata: The path_metadata of this LRuntimeMetadataInfo.  # noqa: E501
        :type: object
        """

        self._path_metadata = path_metadata

    @property
    def limit(self):
        """Gets the limit of this LRuntimeMetadataInfo.  # noqa: E501


        :return: The limit of this LRuntimeMetadataInfo.  # noqa: E501
        :rtype: object
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this LRuntimeMetadataInfo.


        :param limit: The limit of this LRuntimeMetadataInfo.  # noqa: E501
        :type: object
        """

        self._limit = limit

    @property
    def error_handlers(self):
        """Gets the error_handlers of this LRuntimeMetadataInfo.  # noqa: E501


        :return: The error_handlers of this LRuntimeMetadataInfo.  # noqa: E501
        :rtype: object
        """
        return self._error_handlers

    @error_handlers.setter
    def error_handlers(self, error_handlers):
        """Sets the error_handlers of this LRuntimeMetadataInfo.


        :param error_handlers: The error_handlers of this LRuntimeMetadataInfo.  # noqa: E501
        :type: object
        """

        self._error_handlers = error_handlers

    @property
    def import_performance(self):
        """Gets the import_performance of this LRuntimeMetadataInfo.  # noqa: E501


        :return: The import_performance of this LRuntimeMetadataInfo.  # noqa: E501
        :rtype: object
        """
        return self._import_performance

    @import_performance.setter
    def import_performance(self, import_performance):
        """Sets the import_performance of this LRuntimeMetadataInfo.


        :param import_performance: The import_performance of this LRuntimeMetadataInfo.  # noqa: E501
        :type: object
        """

        self._import_performance = import_performance

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(LRuntimeMetadataInfo, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, LRuntimeMetadataInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
