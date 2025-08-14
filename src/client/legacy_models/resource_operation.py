# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

import pprint
import re  # noqa: F401

import six

class LResourceOperation(object):
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
        'operations': 'list[str]',
        'resource_type': 'str',
        'policy_tag': 'str'
    }

    attribute_map = {
        'operations': 'operations',
        'resource_type': 'resourceType',
        'policy_tag': 'policyTag'
    }

    def __init__(self, operations=None, resource_type=None, policy_tag=None):  # noqa: E501
        """LResourceOperation - a model defined in Swagger"""  # noqa: E501
        self._operations = None
        self._resource_type = None
        self._policy_tag = None
        self.discriminator = None
        self.operations = operations
        self.resource_type = resource_type
        if policy_tag is not None:
            self.policy_tag = policy_tag

    @property
    def operations(self):
        """Gets the operations of this LResourceOperation.  # noqa: E501


        :return: The operations of this LResourceOperation.  # noqa: E501
        :rtype: list[str]
        """
        return self._operations

    @operations.setter
    def operations(self, operations):
        """Sets the operations of this LResourceOperation.


        :param operations: The operations of this LResourceOperation.  # noqa: E501
        :type: list[str]
        """
        if operations is None:
            raise ValueError("Invalid value for `operations`, must not be `None`")  # noqa: E501
        allowed_values = ["read", "update", "delete", "create", "share", "execute", "export"]  # noqa: E501
        if not set(operations).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `operations` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(operations) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._operations = operations

    @property
    def resource_type(self):
        """Gets the resource_type of this LResourceOperation.  # noqa: E501


        :return: The resource_type of this LResourceOperation.  # noqa: E501
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this LResourceOperation.


        :param resource_type: The resource_type of this LResourceOperation.  # noqa: E501
        :type: str
        """
        if resource_type is None:
            raise ValueError("Invalid value for `resource_type`, must not be `None`")  # noqa: E501
        allowed_values = ["flow", "connection", "plan", "datasource", "reference", "userdefinedfunction", "folder", "workflow", "workload", "mlproject", "aiproject", "vectorproject", "locationintelligenceproject", "abapplication", "aidatalayer", "aimission", "desktopworkflow", "desktopapp", "report", "globaljobhistory", "folder", "desktopmacro", "aireport", "desktopconnection", "desktopcredential", "desktopdatasource", "desktopenvironmentrule", "schedule", "package", "packagespec", "credential"]  # noqa: E501
        if resource_type not in allowed_values:
            raise ValueError(
                "Invalid value for `resource_type` ({0}), must be one of {1}"  # noqa: E501
                .format(resource_type, allowed_values)
            )

        self._resource_type = resource_type

    @property
    def policy_tag(self):
        """Gets the policy_tag of this LResourceOperation.  # noqa: E501


        :return: The policy_tag of this LResourceOperation.  # noqa: E501
        :rtype: str
        """
        return self._policy_tag

    @policy_tag.setter
    def policy_tag(self, policy_tag):
        """Sets the policy_tag of this LResourceOperation.


        :param policy_tag: The policy_tag of this LResourceOperation.  # noqa: E501
        :type: str
        """
        allowed_values = ["flow_author", "flow_editor", "flow_viewer", "flow_vieweradmin", "flow_owner", "flow_none", "flow_admin", "workspace_admin", "connection_author", "connection_editor", "connection_viewer", "connection_vieweradmin", "connection_owner", "connection_none", "plan_author", "plan_admin", "plan_vieweradmin", "plan_owner", "plan_editor", "plan_viewer", "plan_vieweradmin", "plan_none", "datasource_author", "datasource_owner", "datasource_editor", "datasource_viewer", "datasource_vieweradmin", "datasource_none", "reference_author", "reference_owner", "reference_editor", "reference_viewer", "reference_admin", "reference_none", "userdefinedfunction_author", "userdefinedfunction_owner", "userdefinedfunction_editor", "userdefinedfunction_viewer", "userdefinedfunction_vieweradmin", "userdefinedfunction_none", "workflow_author", "workflow_owner", "workflow_editor", "workflow_viewer", "workflow_vieweradmin", "workflow_none", "workflow_admin", "workload_viewer", "workload_none", "mlproject_author", "mlproject_owner", "mlproject_editor", "mlproject_viewer", "mlproject_vieweradmin", "mlproject_none", "mlproject_admin", "aiproject_author", "aiproject_owner", "aiproject_editor", "aiproject_viewer", "aiproject_vieweradmin", "aiproject_none", "aiproject_admin", "vectorproject_author", "vectorproject_owner", "vectorproject_editor", "vectorproject_viewer", "vectorproject_vieweradmin", "vectorproject_none", "vectorproject_admin", "locationintelligenceproject_author", "locationintelligenceproject_viewer", "locationintelligenceproject_vieweradmin", "locationintelligenceproject_owner", "locationintelligenceproject_none", "locationintelligenceproject_admin", "abapplication_author", "abapplication_owner", "abapplication_editor", "abapplication_viewer", "abapplication_vieweradmin", "abapplication_admin", "abapplication_none", "aidatalayer_author", "aidatalayer_owner", "aidatalayer_editor", "aidatalayer_viewer", "aidatalayer_vieweradmin", "aidatalayer_admin", "aidatalayer_none", "aimission_author", "aimission_owner", "aimission_editor", "aimission_viewer", "aimission_vieweradmin", "aimission_admin", "aimission_none", "desktopworkflow_author", "desktopworkflow_owner", "desktopworkflow_editor", "desktopworkflow_viewer", "desktopworkflow_vieweradmin", "desktopworkflow_admin", "desktopworkflow_none", "desktopapp_author", "desktopapp_owner", "desktopapp_editor", "desktopapp_viewer", "desktopapp_vieweradmin", "desktopapp_admin", "desktopapp_none", "report_author", "report_owner", "report_editor", "report_viewer", "report_vieweradmin", "report_admin", "report_none", "globaljobhistory_viewer", "globaljobhistory_none", "folder_owner", "folder_editor", "folder_viewer", "folder_none", "desktopmacro_author", "desktopmacro_owner", "desktopmacro_editor", "desktopmacro_viewer", "desktopmacro_vieweradmin", "desktopmacro_admin", "desktopmacro_none", "aireport_author", "aireport_owner", "aireport_editor", "aireport_viewer", "aireport_vieweradmin", "aireport_admin", "aireport_none", "desktopconnection_author", "desktopconnection_owner", "desktopconnection_editor", "desktopconnection_viewer", "desktopconnection_vieweradmin", "desktopconnection_collabsharee", "desktopconnection_admin", "desktopconnection_execsharee", "desktopconnection_none", "desktopdatasource_author", "desktopdatasource_owner", "desktopdatasource_admin", "desktopdatasource_none", "desktopcredential_author", "desktopcredential_owner", "desktopcredential_viewer", "desktopcredential_vieweradmin", "desktopcredential_admin", "desktopcredential_none", "desktopenvironmentrule_author", "desktopenvironmentrule_owner", "desktopenvironmentrule_none", "schedule_author", "schedule_owner", "schedule_editor", "schedule_viewer", "schedule_admin", "schedule_vieweradmin", "schedule_none", "package_author", "package_owner", "package_editor", "package_viewer", "package_admin", "package_vieweradmin", "package_none", "packagespec_author", "packagespec_owner", "packagespec_editor", "packagespec_viewer", "packagespec_admin", "packagespec_vieweradmin", "packagespec_none", "credential_author", "credential_owner", "credential_viewer", "credential_none", "custom_policy"]  # noqa: E501
        if policy_tag not in allowed_values:
            raise ValueError(
                "Invalid value for `policy_tag` ({0}), must be one of {1}"  # noqa: E501
                .format(policy_tag, allowed_values)
            )

        self._policy_tag = policy_tag

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
        if issubclass(LResourceOperation, dict):
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
        if not isinstance(other, LResourceOperation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
