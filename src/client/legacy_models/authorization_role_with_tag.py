# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

import pprint
import re  # noqa: F401

import six

class LAuthorizationRoleWithTag(object):
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
        'policy_id': 'LAnyOfauthorizationRoleWithTagPolicyId',
        'workspace_id': 'LAnyOfauthorizationRoleWithTagWorkspaceId',
        'product_policy_id': 'str',
        'resource_operations': 'list[LResourceOperation]',
        'updated_at': 'datetime',
        'created_at': 'datetime',
        'user_count': 'int',
        'name_locked': 'bool',
        'privilege_locked': 'bool',
        'capabilities': 'list[LCapability]',
        'tag': 'str'
    }

    attribute_map = {
        'policy_id': 'policyId',
        'workspace_id': 'workspaceId',
        'product_policy_id': 'productPolicyId',
        'resource_operations': 'resourceOperations',
        'updated_at': 'updatedAt',
        'created_at': 'createdAt',
        'user_count': 'userCount',
        'name_locked': 'nameLocked',
        'privilege_locked': 'privilegeLocked',
        'capabilities': 'capabilities',
        'tag': 'tag'
    }

    def __init__(self, policy_id=None, workspace_id=None, product_policy_id=None, resource_operations=None, updated_at=None, created_at=None, user_count=None, name_locked=None, privilege_locked=None, capabilities=None, tag=None):  # noqa: E501
        """LAuthorizationRoleWithTag - a model defined in Swagger"""  # noqa: E501
        self._policy_id = None
        self._workspace_id = None
        self._product_policy_id = None
        self._resource_operations = None
        self._updated_at = None
        self._created_at = None
        self._user_count = None
        self._name_locked = None
        self._privilege_locked = None
        self._capabilities = None
        self._tag = None
        self.discriminator = None
        self.policy_id = policy_id
        self.workspace_id = workspace_id
        if product_policy_id is not None:
            self.product_policy_id = product_policy_id
        self.resource_operations = resource_operations
        self.updated_at = updated_at
        self.created_at = created_at
        if user_count is not None:
            self.user_count = user_count
        self.name_locked = name_locked
        self.privilege_locked = privilege_locked
        if capabilities is not None:
            self.capabilities = capabilities
        self.tag = tag

    @property
    def policy_id(self):
        """Gets the policy_id of this LAuthorizationRoleWithTag.  # noqa: E501


        :return: The policy_id of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: LAnyOfauthorizationRoleWithTagPolicyId
        """
        return self._policy_id

    @policy_id.setter
    def policy_id(self, policy_id):
        """Sets the policy_id of this LAuthorizationRoleWithTag.


        :param policy_id: The policy_id of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: LAnyOfauthorizationRoleWithTagPolicyId
        """
        if policy_id is None:
            raise ValueError("Invalid value for `policy_id`, must not be `None`")  # noqa: E501

        self._policy_id = policy_id

    @property
    def workspace_id(self):
        """Gets the workspace_id of this LAuthorizationRoleWithTag.  # noqa: E501


        :return: The workspace_id of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: LAnyOfauthorizationRoleWithTagWorkspaceId
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this LAuthorizationRoleWithTag.


        :param workspace_id: The workspace_id of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: LAnyOfauthorizationRoleWithTagWorkspaceId
        """
        if workspace_id is None:
            raise ValueError("Invalid value for `workspace_id`, must not be `None`")  # noqa: E501

        self._workspace_id = workspace_id

    @property
    def product_policy_id(self):
        """Gets the product_policy_id of this LAuthorizationRoleWithTag.  # noqa: E501


        :return: The product_policy_id of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: str
        """
        return self._product_policy_id

    @product_policy_id.setter
    def product_policy_id(self, product_policy_id):
        """Sets the product_policy_id of this LAuthorizationRoleWithTag.


        :param product_policy_id: The product_policy_id of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: str
        """

        self._product_policy_id = product_policy_id

    @property
    def resource_operations(self):
        """Gets the resource_operations of this LAuthorizationRoleWithTag.  # noqa: E501


        :return: The resource_operations of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: list[LResourceOperation]
        """
        return self._resource_operations

    @resource_operations.setter
    def resource_operations(self, resource_operations):
        """Sets the resource_operations of this LAuthorizationRoleWithTag.


        :param resource_operations: The resource_operations of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: list[LResourceOperation]
        """
        if resource_operations is None:
            raise ValueError("Invalid value for `resource_operations`, must not be `None`")  # noqa: E501

        self._resource_operations = resource_operations

    @property
    def updated_at(self):
        """Gets the updated_at of this LAuthorizationRoleWithTag.  # noqa: E501

        The time this object was last updated.  # noqa: E501

        :return: The updated_at of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this LAuthorizationRoleWithTag.

        The time this object was last updated.  # noqa: E501

        :param updated_at: The updated_at of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: datetime
        """
        if updated_at is None:
            raise ValueError("Invalid value for `updated_at`, must not be `None`")  # noqa: E501

        self._updated_at = updated_at

    @property
    def created_at(self):
        """Gets the created_at of this LAuthorizationRoleWithTag.  # noqa: E501

        The time this object was first created.  # noqa: E501

        :return: The created_at of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this LAuthorizationRoleWithTag.

        The time this object was first created.  # noqa: E501

        :param created_at: The created_at of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def user_count(self):
        """Gets the user_count of this LAuthorizationRoleWithTag.  # noqa: E501


        :return: The user_count of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: int
        """
        return self._user_count

    @user_count.setter
    def user_count(self, user_count):
        """Sets the user_count of this LAuthorizationRoleWithTag.


        :param user_count: The user_count of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: int
        """

        self._user_count = user_count

    @property
    def name_locked(self):
        """Gets the name_locked of this LAuthorizationRoleWithTag.  # noqa: E501


        :return: The name_locked of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: bool
        """
        return self._name_locked

    @name_locked.setter
    def name_locked(self, name_locked):
        """Sets the name_locked of this LAuthorizationRoleWithTag.


        :param name_locked: The name_locked of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: bool
        """
        if name_locked is None:
            raise ValueError("Invalid value for `name_locked`, must not be `None`")  # noqa: E501

        self._name_locked = name_locked

    @property
    def privilege_locked(self):
        """Gets the privilege_locked of this LAuthorizationRoleWithTag.  # noqa: E501


        :return: The privilege_locked of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: bool
        """
        return self._privilege_locked

    @privilege_locked.setter
    def privilege_locked(self, privilege_locked):
        """Sets the privilege_locked of this LAuthorizationRoleWithTag.


        :param privilege_locked: The privilege_locked of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: bool
        """
        if privilege_locked is None:
            raise ValueError("Invalid value for `privilege_locked`, must not be `None`")  # noqa: E501

        self._privilege_locked = privilege_locked

    @property
    def capabilities(self):
        """Gets the capabilities of this LAuthorizationRoleWithTag.  # noqa: E501


        :return: The capabilities of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: list[LCapability]
        """
        return self._capabilities

    @capabilities.setter
    def capabilities(self, capabilities):
        """Sets the capabilities of this LAuthorizationRoleWithTag.


        :param capabilities: The capabilities of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: list[LCapability]
        """

        self._capabilities = capabilities

    @property
    def tag(self):
        """Gets the tag of this LAuthorizationRoleWithTag.  # noqa: E501


        :return: The tag of this LAuthorizationRoleWithTag.  # noqa: E501
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this LAuthorizationRoleWithTag.


        :param tag: The tag of this LAuthorizationRoleWithTag.  # noqa: E501
        :type: str
        """
        if tag is None:
            raise ValueError("Invalid value for `tag`, must not be `None`")  # noqa: E501

        self._tag = tag

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
        if issubclass(LAuthorizationRoleWithTag, dict):
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
        if not isinstance(other, LAuthorizationRoleWithTag):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
