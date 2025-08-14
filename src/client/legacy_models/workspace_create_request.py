# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

import pprint
import re  # noqa: F401

import six

class LWorkspaceCreateRequest(object):
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
        'name': 'str',
        'tier': 'str',
        'state': 'str',
        'last_state_change': 'datetime',
        'custom_url': 'str',
        'max_user_number': 'int',
        'emrcluster': 'object',
        'emr_config_id': 'int'
    }

    attribute_map = {
        'name': 'name',
        'tier': 'tier',
        'state': 'state',
        'last_state_change': 'lastStateChange',
        'custom_url': 'custom_url',
        'max_user_number': 'max_user_number',
        'emrcluster': 'emrcluster',
        'emr_config_id': 'emrConfigId'
    }

    def __init__(self, name=None, tier=None, state=None, last_state_change=None, custom_url=None, max_user_number=None, emrcluster=None, emr_config_id=None):  # noqa: E501
        """LWorkspaceCreateRequest - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._tier = None
        self._state = None
        self._last_state_change = None
        self._custom_url = None
        self._max_user_number = None
        self._emrcluster = None
        self._emr_config_id = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if tier is not None:
            self.tier = tier
        if state is not None:
            self.state = state
        if last_state_change is not None:
            self.last_state_change = last_state_change
        if custom_url is not None:
            self.custom_url = custom_url
        if max_user_number is not None:
            self.max_user_number = max_user_number
        if emrcluster is not None:
            self.emrcluster = emrcluster
        if emr_config_id is not None:
            self.emr_config_id = emr_config_id

    @property
    def name(self):
        """Gets the name of this LWorkspaceCreateRequest.  # noqa: E501

        Workspace name  # noqa: E501

        :return: The name of this LWorkspaceCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LWorkspaceCreateRequest.

        Workspace name  # noqa: E501

        :param name: The name of this LWorkspaceCreateRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def tier(self):
        """Gets the tier of this LWorkspaceCreateRequest.  # noqa: E501


        :return: The tier of this LWorkspaceCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._tier

    @tier.setter
    def tier(self, tier):
        """Sets the tier of this LWorkspaceCreateRequest.


        :param tier: The tier of this LWorkspaceCreateRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["free", "pro", "none", "legacy", "standard", "premium", "standard-free", "starter", "professional", "professional_trial", "enterprise_cloud", "enterprise_cloud_trial", "starter22", "professional22", "enterprise_cloud22", "enterprise_cloud22_trial", "looker_freemium", "platform_packaging"]  # noqa: E501
        if tier not in allowed_values:
            raise ValueError(
                "Invalid value for `tier` ({0}), must be one of {1}"  # noqa: E501
                .format(tier, allowed_values)
            )

        self._tier = tier

    @property
    def state(self):
        """Gets the state of this LWorkspaceCreateRequest.  # noqa: E501


        :return: The state of this LWorkspaceCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this LWorkspaceCreateRequest.


        :param state: The state of this LWorkspaceCreateRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["active", "hidden", "pending_purge"]  # noqa: E501
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"  # noqa: E501
                .format(state, allowed_values)
            )

        self._state = state

    @property
    def last_state_change(self):
        """Gets the last_state_change of this LWorkspaceCreateRequest.  # noqa: E501


        :return: The last_state_change of this LWorkspaceCreateRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._last_state_change

    @last_state_change.setter
    def last_state_change(self, last_state_change):
        """Sets the last_state_change of this LWorkspaceCreateRequest.


        :param last_state_change: The last_state_change of this LWorkspaceCreateRequest.  # noqa: E501
        :type: datetime
        """

        self._last_state_change = last_state_change

    @property
    def custom_url(self):
        """Gets the custom_url of this LWorkspaceCreateRequest.  # noqa: E501

        Workspace URL  # noqa: E501

        :return: The custom_url of this LWorkspaceCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._custom_url

    @custom_url.setter
    def custom_url(self, custom_url):
        """Sets the custom_url of this LWorkspaceCreateRequest.

        Workspace URL  # noqa: E501

        :param custom_url: The custom_url of this LWorkspaceCreateRequest.  # noqa: E501
        :type: str
        """

        self._custom_url = custom_url

    @property
    def max_user_number(self):
        """Gets the max_user_number of this LWorkspaceCreateRequest.  # noqa: E501

        Maximum number of users for the workspace  # noqa: E501

        :return: The max_user_number of this LWorkspaceCreateRequest.  # noqa: E501
        :rtype: int
        """
        return self._max_user_number

    @max_user_number.setter
    def max_user_number(self, max_user_number):
        """Sets the max_user_number of this LWorkspaceCreateRequest.

        Maximum number of users for the workspace  # noqa: E501

        :param max_user_number: The max_user_number of this LWorkspaceCreateRequest.  # noqa: E501
        :type: int
        """

        self._max_user_number = max_user_number

    @property
    def emrcluster(self):
        """Gets the emrcluster of this LWorkspaceCreateRequest.  # noqa: E501


        :return: The emrcluster of this LWorkspaceCreateRequest.  # noqa: E501
        :rtype: object
        """
        return self._emrcluster

    @emrcluster.setter
    def emrcluster(self, emrcluster):
        """Sets the emrcluster of this LWorkspaceCreateRequest.


        :param emrcluster: The emrcluster of this LWorkspaceCreateRequest.  # noqa: E501
        :type: object
        """

        self._emrcluster = emrcluster

    @property
    def emr_config_id(self):
        """Gets the emr_config_id of this LWorkspaceCreateRequest.  # noqa: E501


        :return: The emr_config_id of this LWorkspaceCreateRequest.  # noqa: E501
        :rtype: int
        """
        return self._emr_config_id

    @emr_config_id.setter
    def emr_config_id(self, emr_config_id):
        """Sets the emr_config_id of this LWorkspaceCreateRequest.


        :param emr_config_id: The emr_config_id of this LWorkspaceCreateRequest.  # noqa: E501
        :type: int
        """

        self._emr_config_id = emr_config_id

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
        if issubclass(LWorkspaceCreateRequest, dict):
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
        if not isinstance(other, LWorkspaceCreateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
