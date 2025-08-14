# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

import pprint
import re  # noqa: F401

import six

class LWriteSettingCreateRequest(object):
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
        'path': 'str',
        'action': 'str',
        'format': 'str',
        'compression': 'str',
        'header': 'bool',
        'as_single_file': 'bool',
        'delim': 'str',
        'has_quotes': 'bool',
        'include_mismatches': 'bool',
        'output_object_id': 'int',
        'run_parameters': 'list[LRunParameterDestinationInfo]',
        'connection_id': 'str'
    }

    attribute_map = {
        'path': 'path',
        'action': 'action',
        'format': 'format',
        'compression': 'compression',
        'header': 'header',
        'as_single_file': 'asSingleFile',
        'delim': 'delim',
        'has_quotes': 'hasQuotes',
        'include_mismatches': 'includeMismatches',
        'output_object_id': 'outputObjectId',
        'run_parameters': 'runParameters',
        'connection_id': 'connectionId'
    }

    def __init__(self, path=None, action=None, format=None, compression=None, header=None, as_single_file=None, delim=None, has_quotes=None, include_mismatches=None, output_object_id=None, run_parameters=None, connection_id=None):  # noqa: E501
        """LWriteSettingCreateRequest - a model defined in Swagger"""  # noqa: E501
        self._path = None
        self._action = None
        self._format = None
        self._compression = None
        self._header = None
        self._as_single_file = None
        self._delim = None
        self._has_quotes = None
        self._include_mismatches = None
        self._output_object_id = None
        self._run_parameters = None
        self._connection_id = None
        self.discriminator = None
        self.path = path
        self.action = action
        self.format = format
        if compression is not None:
            self.compression = compression
        if header is not None:
            self.header = header
        if as_single_file is not None:
            self.as_single_file = as_single_file
        if delim is not None:
            self.delim = delim
        if has_quotes is not None:
            self.has_quotes = has_quotes
        if include_mismatches is not None:
            self.include_mismatches = include_mismatches
        if output_object_id is not None:
            self.output_object_id = output_object_id
        if run_parameters is not None:
            self.run_parameters = run_parameters
        if connection_id is not None:
            self.connection_id = connection_id

    @property
    def path(self):
        """Gets the path of this LWriteSettingCreateRequest.  # noqa: E501

        The fully qualified path to the output location where to write the results.  # noqa: E501

        :return: The path of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this LWriteSettingCreateRequest.

        The fully qualified path to the output location where to write the results.  # noqa: E501

        :param path: The path of this LWriteSettingCreateRequest.  # noqa: E501
        :type: str
        """
        if path is None:
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501

        self._path = path

    @property
    def action(self):
        """Gets the action of this LWriteSettingCreateRequest.  # noqa: E501

        If the output file or directory exists,   you can specify one of the following actions * `create` - Create a new, parallel location, preserving the old results. * `append` - Add the new results to the old results. * `overwrite` - Replace the old results with the new results.  # noqa: E501

        :return: The action of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this LWriteSettingCreateRequest.

        If the output file or directory exists,   you can specify one of the following actions * `create` - Create a new, parallel location, preserving the old results. * `append` - Add the new results to the old results. * `overwrite` - Replace the old results with the new results.  # noqa: E501

        :param action: The action of this LWriteSettingCreateRequest.  # noqa: E501
        :type: str
        """
        if action is None:
            raise ValueError("Invalid value for `action`, must not be `None`")  # noqa: E501
        allowed_values = ["create", "append", "overwrite"]  # noqa: E501
        if action not in allowed_values:
            raise ValueError(
                "Invalid value for `action` ({0}), must be one of {1}"  # noqa: E501
                .format(action, allowed_values)
            )

        self._action = action

    @property
    def format(self):
        """Gets the format of this LWriteSettingCreateRequest.  # noqa: E501

        Output format for the results. Specify one of the supported values. * `csv` - CSV format. When using `csv`, you can specify a custom delimiter using the `delim` parameter. * `json` - JSON format * `avro` - Avro format * `pqt` - Parquet format * `hyper` - Tableau Hyper format  # noqa: E501

        :return: The format of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this LWriteSettingCreateRequest.

        Output format for the results. Specify one of the supported values. * `csv` - CSV format. When using `csv`, you can specify a custom delimiter using the `delim` parameter. * `json` - JSON format * `avro` - Avro format * `pqt` - Parquet format * `hyper` - Tableau Hyper format  # noqa: E501

        :param format: The format of this LWriteSettingCreateRequest.  # noqa: E501
        :type: str
        """
        if format is None:
            raise ValueError("Invalid value for `format`, must not be `None`")  # noqa: E501
        allowed_values = ["csv", "json", "avro", "pqt", "hyper"]  # noqa: E501
        if format not in allowed_values:
            raise ValueError(
                "Invalid value for `format` ({0}), must be one of {1}"  # noqa: E501
                .format(format, allowed_values)
            )

        self._format = format

    @property
    def compression(self):
        """Gets the compression of this LWriteSettingCreateRequest.  # noqa: E501

        For csv and json results, you can optionally compress them using `bzip2` or `gzip` compression. Default is none. > ℹ️ **NOTE**: If compression is applied, the filename in the `path` value must end with the appropriate extension for the type of compression: `.gz` for *gzip* and `.bz2` for *bzip2* * `none` - No compression * `gzip` - Use `gzip` compression * `bzip2` - Use `bzip2` compression * `snappy` - Use `snappy` compression  # noqa: E501

        :return: The compression of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._compression

    @compression.setter
    def compression(self, compression):
        """Sets the compression of this LWriteSettingCreateRequest.

        For csv and json results, you can optionally compress them using `bzip2` or `gzip` compression. Default is none. > ℹ️ **NOTE**: If compression is applied, the filename in the `path` value must end with the appropriate extension for the type of compression: `.gz` for *gzip* and `.bz2` for *bzip2* * `none` - No compression * `gzip` - Use `gzip` compression * `bzip2` - Use `bzip2` compression * `snappy` - Use `snappy` compression  # noqa: E501

        :param compression: The compression of this LWriteSettingCreateRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["none", "gzip", "bzip2", "snappy"]  # noqa: E501
        if compression not in allowed_values:
            raise ValueError(
                "Invalid value for `compression` ({0}), must be one of {1}"  # noqa: E501
                .format(compression, allowed_values)
            )

        self._compression = compression

    @property
    def header(self):
        """Gets the header of this LWriteSettingCreateRequest.  # noqa: E501

        For csv results with action set to `create` or `append`, this value determines if a header row with column names is inserted at the top of the results. Default is `false`.  # noqa: E501

        :return: The header of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._header

    @header.setter
    def header(self, header):
        """Sets the header of this LWriteSettingCreateRequest.

        For csv results with action set to `create` or `append`, this value determines if a header row with column names is inserted at the top of the results. Default is `false`.  # noqa: E501

        :param header: The header of this LWriteSettingCreateRequest.  # noqa: E501
        :type: bool
        """

        self._header = header

    @property
    def as_single_file(self):
        """Gets the as_single_file of this LWriteSettingCreateRequest.  # noqa: E501

        For `csv` and `json` results, this value determines if the results are concatenated into a single file or stored as multiple files. Default is `false`.  # noqa: E501

        :return: The as_single_file of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._as_single_file

    @as_single_file.setter
    def as_single_file(self, as_single_file):
        """Sets the as_single_file of this LWriteSettingCreateRequest.

        For `csv` and `json` results, this value determines if the results are concatenated into a single file or stored as multiple files. Default is `false`.  # noqa: E501

        :param as_single_file: The as_single_file of this LWriteSettingCreateRequest.  # noqa: E501
        :type: bool
        """

        self._as_single_file = as_single_file

    @property
    def delim(self):
        """Gets the delim of this LWriteSettingCreateRequest.  # noqa: E501

        The delimiter between field values in an output row. Only relevant if the chosen `format` is `csv`  # noqa: E501

        :return: The delim of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._delim

    @delim.setter
    def delim(self, delim):
        """Sets the delim of this LWriteSettingCreateRequest.

        The delimiter between field values in an output row. Only relevant if the chosen `format` is `csv`  # noqa: E501

        :param delim: The delim of this LWriteSettingCreateRequest.  # noqa: E501
        :type: str
        """

        self._delim = delim

    @property
    def has_quotes(self):
        """Gets the has_quotes of this LWriteSettingCreateRequest.  # noqa: E501

        If true, each field in the output is wrapped in double-quotes.  # noqa: E501

        :return: The has_quotes of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._has_quotes

    @has_quotes.setter
    def has_quotes(self, has_quotes):
        """Sets the has_quotes of this LWriteSettingCreateRequest.

        If true, each field in the output is wrapped in double-quotes.  # noqa: E501

        :param has_quotes: The has_quotes of this LWriteSettingCreateRequest.  # noqa: E501
        :type: bool
        """

        self._has_quotes = has_quotes

    @property
    def include_mismatches(self):
        """Gets the include_mismatches of this LWriteSettingCreateRequest.  # noqa: E501

        If true, write out mismatched values as a string.  # noqa: E501

        :return: The include_mismatches of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._include_mismatches

    @include_mismatches.setter
    def include_mismatches(self, include_mismatches):
        """Sets the include_mismatches of this LWriteSettingCreateRequest.

        If true, write out mismatched values as a string.  # noqa: E501

        :param include_mismatches: The include_mismatches of this LWriteSettingCreateRequest.  # noqa: E501
        :type: bool
        """

        self._include_mismatches = include_mismatches

    @property
    def output_object_id(self):
        """Gets the output_object_id of this LWriteSettingCreateRequest.  # noqa: E501

        [outputObject](#tag/OutputObject) to attach this [writeSetting](#tag/WriteSetting) to.  # noqa: E501

        :return: The output_object_id of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: int
        """
        return self._output_object_id

    @output_object_id.setter
    def output_object_id(self, output_object_id):
        """Sets the output_object_id of this LWriteSettingCreateRequest.

        [outputObject](#tag/OutputObject) to attach this [writeSetting](#tag/WriteSetting) to.  # noqa: E501

        :param output_object_id: The output_object_id of this LWriteSettingCreateRequest.  # noqa: E501
        :type: int
        """

        self._output_object_id = output_object_id

    @property
    def run_parameters(self):
        """Gets the run_parameters of this LWriteSettingCreateRequest.  # noqa: E501

        Optional Parameters that can be used to parameterized the path  # noqa: E501

        :return: The run_parameters of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: list[LRunParameterDestinationInfo]
        """
        return self._run_parameters

    @run_parameters.setter
    def run_parameters(self, run_parameters):
        """Sets the run_parameters of this LWriteSettingCreateRequest.

        Optional Parameters that can be used to parameterized the path  # noqa: E501

        :param run_parameters: The run_parameters of this LWriteSettingCreateRequest.  # noqa: E501
        :type: list[LRunParameterDestinationInfo]
        """

        self._run_parameters = run_parameters

    @property
    def connection_id(self):
        """Gets the connection_id of this LWriteSettingCreateRequest.  # noqa: E501

        Internal identifier of the connection to use when writing to a SFTP destination.  # noqa: E501

        :return: The connection_id of this LWriteSettingCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._connection_id

    @connection_id.setter
    def connection_id(self, connection_id):
        """Sets the connection_id of this LWriteSettingCreateRequest.

        Internal identifier of the connection to use when writing to a SFTP destination.  # noqa: E501

        :param connection_id: The connection_id of this LWriteSettingCreateRequest.  # noqa: E501
        :type: str
        """

        self._connection_id = connection_id

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
        if issubclass(LWriteSettingCreateRequest, dict):
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
        if not isinstance(other, LWriteSettingCreateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
