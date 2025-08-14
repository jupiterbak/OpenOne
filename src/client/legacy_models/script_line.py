# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

import pprint
import re  # noqa: F401

import six

class LScriptLine(object):
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
        'column_metadata': 'object',
        'encoding': 'str',
        'edit_script_line': 'object',
        'task': 'object',
        'table_data': 'object',
        'hash': 'str',
        'id': 'LAnyOfscriptLineId',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'creator': 'object',
        'updater': 'object'
    }

    attribute_map = {
        'column_metadata': 'columnMetadata',
        'encoding': 'encoding',
        'edit_script_line': 'editScriptLine',
        'task': 'task',
        'table_data': 'tableData',
        'hash': 'hash',
        'id': 'id',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'creator': 'creator',
        'updater': 'updater'
    }

    def __init__(self, column_metadata=None, encoding=None, edit_script_line=None, task=None, table_data=None, hash=None, id=None, created_at=None, updated_at=None, creator=None, updater=None):  # noqa: E501
        """LScriptLine - a model defined in Swagger"""  # noqa: E501
        self._column_metadata = None
        self._encoding = None
        self._edit_script_line = None
        self._task = None
        self._table_data = None
        self._hash = None
        self._id = None
        self._created_at = None
        self._updated_at = None
        self._creator = None
        self._updater = None
        self.discriminator = None
        if column_metadata is not None:
            self.column_metadata = column_metadata
        if encoding is not None:
            self.encoding = encoding
        if edit_script_line is not None:
            self.edit_script_line = edit_script_line
        if task is not None:
            self.task = task
        if table_data is not None:
            self.table_data = table_data
        if hash is not None:
            self.hash = hash
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        if creator is not None:
            self.creator = creator
        if updater is not None:
            self.updater = updater

    @property
    def column_metadata(self):
        """Gets the column_metadata of this LScriptLine.  # noqa: E501


        :return: The column_metadata of this LScriptLine.  # noqa: E501
        :rtype: object
        """
        return self._column_metadata

    @column_metadata.setter
    def column_metadata(self, column_metadata):
        """Sets the column_metadata of this LScriptLine.


        :param column_metadata: The column_metadata of this LScriptLine.  # noqa: E501
        :type: object
        """

        self._column_metadata = column_metadata

    @property
    def encoding(self):
        """Gets the encoding of this LScriptLine.  # noqa: E501


        :return: The encoding of this LScriptLine.  # noqa: E501
        :rtype: str
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        """Sets the encoding of this LScriptLine.


        :param encoding: The encoding of this LScriptLine.  # noqa: E501
        :type: str
        """

        self._encoding = encoding

    @property
    def edit_script_line(self):
        """Gets the edit_script_line of this LScriptLine.  # noqa: E501


        :return: The edit_script_line of this LScriptLine.  # noqa: E501
        :rtype: object
        """
        return self._edit_script_line

    @edit_script_line.setter
    def edit_script_line(self, edit_script_line):
        """Sets the edit_script_line of this LScriptLine.


        :param edit_script_line: The edit_script_line of this LScriptLine.  # noqa: E501
        :type: object
        """

        self._edit_script_line = edit_script_line

    @property
    def task(self):
        """Gets the task of this LScriptLine.  # noqa: E501


        :return: The task of this LScriptLine.  # noqa: E501
        :rtype: object
        """
        return self._task

    @task.setter
    def task(self, task):
        """Sets the task of this LScriptLine.


        :param task: The task of this LScriptLine.  # noqa: E501
        :type: object
        """

        self._task = task

    @property
    def table_data(self):
        """Gets the table_data of this LScriptLine.  # noqa: E501


        :return: The table_data of this LScriptLine.  # noqa: E501
        :rtype: object
        """
        return self._table_data

    @table_data.setter
    def table_data(self, table_data):
        """Sets the table_data of this LScriptLine.


        :param table_data: The table_data of this LScriptLine.  # noqa: E501
        :type: object
        """

        self._table_data = table_data

    @property
    def hash(self):
        """Gets the hash of this LScriptLine.  # noqa: E501


        :return: The hash of this LScriptLine.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this LScriptLine.


        :param hash: The hash of this LScriptLine.  # noqa: E501
        :type: str
        """

        self._hash = hash

    @property
    def id(self):
        """Gets the id of this LScriptLine.  # noqa: E501


        :return: The id of this LScriptLine.  # noqa: E501
        :rtype: LAnyOfscriptLineId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this LScriptLine.


        :param id: The id of this LScriptLine.  # noqa: E501
        :type: LAnyOfscriptLineId
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_at(self):
        """Gets the created_at of this LScriptLine.  # noqa: E501

        The time this object was first created.  # noqa: E501

        :return: The created_at of this LScriptLine.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this LScriptLine.

        The time this object was first created.  # noqa: E501

        :param created_at: The created_at of this LScriptLine.  # noqa: E501
        :type: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this LScriptLine.  # noqa: E501

        The time this object was last updated.  # noqa: E501

        :return: The updated_at of this LScriptLine.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this LScriptLine.

        The time this object was last updated.  # noqa: E501

        :param updated_at: The updated_at of this LScriptLine.  # noqa: E501
        :type: datetime
        """
        if updated_at is None:
            raise ValueError("Invalid value for `updated_at`, must not be `None`")  # noqa: E501

        self._updated_at = updated_at

    @property
    def creator(self):
        """Gets the creator of this LScriptLine.  # noqa: E501


        :return: The creator of this LScriptLine.  # noqa: E501
        :rtype: object
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this LScriptLine.


        :param creator: The creator of this LScriptLine.  # noqa: E501
        :type: object
        """

        self._creator = creator

    @property
    def updater(self):
        """Gets the updater of this LScriptLine.  # noqa: E501


        :return: The updater of this LScriptLine.  # noqa: E501
        :rtype: object
        """
        return self._updater

    @updater.setter
    def updater(self, updater):
        """Sets the updater of this LScriptLine.


        :param updater: The updater of this LScriptLine.  # noqa: E501
        :type: object
        """

        self._updater = updater

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
        if issubclass(LScriptLine, dict):
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
        if not isinstance(other, LScriptLine):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
