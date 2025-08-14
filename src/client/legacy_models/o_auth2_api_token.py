# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

import pprint
import re  # noqa: F401

import six

class LOAuth2ApiToken(object):
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
        'sid': 'str',
        'env_id': 'str',
        'client_id': 'str',
        'user_id': 'str',
        'issuer': 'str',
        'token_type': 'str',
        'status': 'str',
        'access_scope': 'str',
        'scopes': 'str',
        'expired_at': 'datetime',
        'created_at': 'datetime',
        'active_at': 'datetime'
    }

    attribute_map = {
        'name': 'name',
        'sid': 'sid',
        'env_id': 'envId',
        'client_id': 'clientId',
        'user_id': 'userId',
        'issuer': 'issuer',
        'token_type': 'tokenType',
        'status': 'status',
        'access_scope': 'accessScope',
        'scopes': 'scopes',
        'expired_at': 'expiredAt',
        'created_at': 'createdAt',
        'active_at': 'activeAt'
    }

    def __init__(self, name=None, sid=None, env_id=None, client_id=None, user_id=None, issuer=None, token_type=None, status=None, access_scope=None, scopes=None, expired_at=None, created_at=None, active_at=None):  # noqa: E501
        """LOAuth2ApiToken - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._sid = None
        self._env_id = None
        self._client_id = None
        self._user_id = None
        self._issuer = None
        self._token_type = None
        self._status = None
        self._access_scope = None
        self._scopes = None
        self._expired_at = None
        self._created_at = None
        self._active_at = None
        self.discriminator = None
        self.name = name
        self.sid = sid
        self.env_id = env_id
        self.client_id = client_id
        self.user_id = user_id
        self.issuer = issuer
        self.token_type = token_type
        self.status = status
        self.access_scope = access_scope
        self.scopes = scopes
        self.expired_at = expired_at
        self.created_at = created_at
        if active_at is not None:
            self.active_at = active_at

    @property
    def name(self):
        """Gets the name of this LOAuth2ApiToken.  # noqa: E501

        User-friendly description for the access token  # noqa: E501

        :return: The name of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LOAuth2ApiToken.

        User-friendly description for the access token  # noqa: E501

        :param name: The name of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def sid(self):
        """Gets the sid of this LOAuth2ApiToken.  # noqa: E501

        Token Session ID  # noqa: E501

        :return: The sid of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._sid

    @sid.setter
    def sid(self, sid):
        """Sets the sid of this LOAuth2ApiToken.

        Token Session ID  # noqa: E501

        :param sid: The sid of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if sid is None:
            raise ValueError("Invalid value for `sid`, must not be `None`")  # noqa: E501

        self._sid = sid

    @property
    def env_id(self):
        """Gets the env_id of this LOAuth2ApiToken.  # noqa: E501

        Token Auth Server environment ID  # noqa: E501

        :return: The env_id of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._env_id

    @env_id.setter
    def env_id(self, env_id):
        """Sets the env_id of this LOAuth2ApiToken.

        Token Auth Server environment ID  # noqa: E501

        :param env_id: The env_id of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if env_id is None:
            raise ValueError("Invalid value for `env_id`, must not be `None`")  # noqa: E501

        self._env_id = env_id

    @property
    def client_id(self):
        """Gets the client_id of this LOAuth2ApiToken.  # noqa: E501

        Token Authentication Application ID  # noqa: E501

        :return: The client_id of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this LOAuth2ApiToken.

        Token Authentication Application ID  # noqa: E501

        :param client_id: The client_id of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if client_id is None:
            raise ValueError("Invalid value for `client_id`, must not be `None`")  # noqa: E501

        self._client_id = client_id

    @property
    def user_id(self):
        """Gets the user_id of this LOAuth2ApiToken.  # noqa: E501

        Token User ID  # noqa: E501

        :return: The user_id of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this LOAuth2ApiToken.

        Token User ID  # noqa: E501

        :param user_id: The user_id of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

    @property
    def issuer(self):
        """Gets the issuer of this LOAuth2ApiToken.  # noqa: E501

        Token Issuer URL  # noqa: E501

        :return: The issuer of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._issuer

    @issuer.setter
    def issuer(self, issuer):
        """Sets the issuer of this LOAuth2ApiToken.

        Token Issuer URL  # noqa: E501

        :param issuer: The issuer of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if issuer is None:
            raise ValueError("Invalid value for `issuer`, must not be `None`")  # noqa: E501

        self._issuer = issuer

    @property
    def token_type(self):
        """Gets the token_type of this LOAuth2ApiToken.  # noqa: E501

        Type of the token * `Workspace` - Workspace token * `Billing Account` - Billing account token  # noqa: E501

        :return: The token_type of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._token_type

    @token_type.setter
    def token_type(self, token_type):
        """Sets the token_type of this LOAuth2ApiToken.

        Type of the token * `Workspace` - Workspace token * `Billing Account` - Billing account token  # noqa: E501

        :param token_type: The token_type of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if token_type is None:
            raise ValueError("Invalid value for `token_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Workspace", "Billing Account"]  # noqa: E501
        if token_type not in allowed_values:
            raise ValueError(
                "Invalid value for `token_type` ({0}), must be one of {1}"  # noqa: E501
                .format(token_type, allowed_values)
            )

        self._token_type = token_type

    @property
    def status(self):
        """Gets the status of this LOAuth2ApiToken.  # noqa: E501

        Status of the token * `Enabled` - Token is active * `Disabled by User` - Token was disabled by user * `Disabled by Admin` - Token was disabled by admin * `Expired` - Token expired  # noqa: E501

        :return: The status of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this LOAuth2ApiToken.

        Status of the token * `Enabled` - Token is active * `Disabled by User` - Token was disabled by user * `Disabled by Admin` - Token was disabled by admin * `Expired` - Token expired  # noqa: E501

        :param status: The status of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501
        allowed_values = ["Enabled", "Disabled by User", "Disabled by Admin", "Expired"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def access_scope(self):
        """Gets the access_scope of this LOAuth2ApiToken.  # noqa: E501

        Scope category of the token * `Full Access` - Token has full access scope * `Custom Access` - Token has custom access scope  # noqa: E501

        :return: The access_scope of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._access_scope

    @access_scope.setter
    def access_scope(self, access_scope):
        """Sets the access_scope of this LOAuth2ApiToken.

        Scope category of the token * `Full Access` - Token has full access scope * `Custom Access` - Token has custom access scope  # noqa: E501

        :param access_scope: The access_scope of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if access_scope is None:
            raise ValueError("Invalid value for `access_scope`, must not be `None`")  # noqa: E501
        allowed_values = ["Full Access", "Custom Access"]  # noqa: E501
        if access_scope not in allowed_values:
            raise ValueError(
                "Invalid value for `access_scope` ({0}), must be one of {1}"  # noqa: E501
                .format(access_scope, allowed_values)
            )

        self._access_scope = access_scope

    @property
    def scopes(self):
        """Gets the scopes of this LOAuth2ApiToken.  # noqa: E501

        Scope of the token  # noqa: E501

        :return: The scopes of this LOAuth2ApiToken.  # noqa: E501
        :rtype: str
        """
        return self._scopes

    @scopes.setter
    def scopes(self, scopes):
        """Sets the scopes of this LOAuth2ApiToken.

        Scope of the token  # noqa: E501

        :param scopes: The scopes of this LOAuth2ApiToken.  # noqa: E501
        :type: str
        """
        if scopes is None:
            raise ValueError("Invalid value for `scopes`, must not be `None`")  # noqa: E501

        self._scopes = scopes

    @property
    def expired_at(self):
        """Gets the expired_at of this LOAuth2ApiToken.  # noqa: E501

        Timestamp for when the access token expires. A `null` value indicates that the access token never expires.  # noqa: E501

        :return: The expired_at of this LOAuth2ApiToken.  # noqa: E501
        :rtype: datetime
        """
        return self._expired_at

    @expired_at.setter
    def expired_at(self, expired_at):
        """Sets the expired_at of this LOAuth2ApiToken.

        Timestamp for when the access token expires. A `null` value indicates that the access token never expires.  # noqa: E501

        :param expired_at: The expired_at of this LOAuth2ApiToken.  # noqa: E501
        :type: datetime
        """
        if expired_at is None:
            raise ValueError("Invalid value for `expired_at`, must not be `None`")  # noqa: E501

        self._expired_at = expired_at

    @property
    def created_at(self):
        """Gets the created_at of this LOAuth2ApiToken.  # noqa: E501

        The time this object was first created.  # noqa: E501

        :return: The created_at of this LOAuth2ApiToken.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this LOAuth2ApiToken.

        The time this object was first created.  # noqa: E501

        :param created_at: The created_at of this LOAuth2ApiToken.  # noqa: E501
        :type: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def active_at(self):
        """Gets the active_at of this LOAuth2ApiToken.  # noqa: E501

        Timestamp for when the access token was last used. A `null` value indicates that the access token has never been used.  # noqa: E501

        :return: The active_at of this LOAuth2ApiToken.  # noqa: E501
        :rtype: datetime
        """
        return self._active_at

    @active_at.setter
    def active_at(self, active_at):
        """Sets the active_at of this LOAuth2ApiToken.

        Timestamp for when the access token was last used. A `null` value indicates that the access token has never been used.  # noqa: E501

        :param active_at: The active_at of this LOAuth2ApiToken.  # noqa: E501
        :type: datetime
        """

        self._active_at = active_at

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
        if issubclass(LOAuth2ApiToken, dict):
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
        if not isinstance(other, LOAuth2ApiToken):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
