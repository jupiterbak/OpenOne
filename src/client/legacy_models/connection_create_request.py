# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

import pprint
import re  # noqa: F401

import six

class LConnectionCreateRequest(object):
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
        'vendor': 'str',
        'vendor_name': 'str',
        'type': 'str',
        'credential_type': 'str',
        'advanced_credential_type': 'str',
        'ssh_tunneling': 'bool',
        'ssl': 'bool',
        'name': 'str',
        'description': 'str',
        'disable_type_inference': 'bool',
        'is_global': 'bool',
        'credentials_shared': 'bool',
        'has_credentials': 'bool',
        'host': 'str',
        'port': 'int',
        'bucket': 'str',
        'params': 'object',
        'oauth2_state_id': 'str',
        'credentials': 'LAcceptedCredentials',
        'advanced_credentials': 'LAdvancedCredentialsInfo',
        'endpoints': 'LJdbcRestEndpointsInfo'
    }

    attribute_map = {
        'vendor': 'vendor',
        'vendor_name': 'vendorName',
        'type': 'type',
        'credential_type': 'credentialType',
        'advanced_credential_type': 'advancedCredentialType',
        'ssh_tunneling': 'sshTunneling',
        'ssl': 'ssl',
        'name': 'name',
        'description': 'description',
        'disable_type_inference': 'disableTypeInference',
        'is_global': 'isGlobal',
        'credentials_shared': 'credentialsShared',
        'has_credentials': 'hasCredentials',
        'host': 'host',
        'port': 'port',
        'bucket': 'bucket',
        'params': 'params',
        'oauth2_state_id': 'oauth2StateId',
        'credentials': 'credentials',
        'advanced_credentials': 'advancedCredentials',
        'endpoints': 'endpoints'
    }

    def __init__(self, vendor=None, vendor_name=None, type=None, credential_type=None, advanced_credential_type=None, ssh_tunneling=None, ssl=None, name=None, description=None, disable_type_inference=None, is_global=None, credentials_shared=None, has_credentials=None, host=None, port=None, bucket=None, params=None, oauth2_state_id=None, credentials=None, advanced_credentials=None, endpoints=None):  # noqa: E501
        """LConnectionCreateRequest - a model defined in Swagger"""  # noqa: E501
        self._vendor = None
        self._vendor_name = None
        self._type = None
        self._credential_type = None
        self._advanced_credential_type = None
        self._ssh_tunneling = None
        self._ssl = None
        self._name = None
        self._description = None
        self._disable_type_inference = None
        self._is_global = None
        self._credentials_shared = None
        self._has_credentials = None
        self._host = None
        self._port = None
        self._bucket = None
        self._params = None
        self._oauth2_state_id = None
        self._credentials = None
        self._advanced_credentials = None
        self._endpoints = None
        self.discriminator = None
        self.vendor = vendor
        self.vendor_name = vendor_name
        self.type = type
        self.credential_type = credential_type
        if advanced_credential_type is not None:
            self.advanced_credential_type = advanced_credential_type
        if ssh_tunneling is not None:
            self.ssh_tunneling = ssh_tunneling
        if ssl is not None:
            self.ssl = ssl
        self.name = name
        if description is not None:
            self.description = description
        if disable_type_inference is not None:
            self.disable_type_inference = disable_type_inference
        if is_global is not None:
            self.is_global = is_global
        if credentials_shared is not None:
            self.credentials_shared = credentials_shared
        if has_credentials is not None:
            self.has_credentials = has_credentials
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if bucket is not None:
            self.bucket = bucket
        self.params = params
        if oauth2_state_id is not None:
            self.oauth2_state_id = oauth2_state_id
        if credentials is not None:
            self.credentials = credentials
        if advanced_credentials is not None:
            self.advanced_credentials = advanced_credentials
        if endpoints is not None:
            self.endpoints = endpoints

    @property
    def vendor(self):
        """Gets the vendor of this LConnectionCreateRequest.  # noqa: E501

        String identifying the connection`s vendor  # noqa: E501

        :return: The vendor of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._vendor

    @vendor.setter
    def vendor(self, vendor):
        """Sets the vendor of this LConnectionCreateRequest.

        String identifying the connection`s vendor  # noqa: E501

        :param vendor: The vendor of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """
        if vendor is None:
            raise ValueError("Invalid value for `vendor`, must not be `None`")  # noqa: E501

        self._vendor = vendor

    @property
    def vendor_name(self):
        """Gets the vendor_name of this LConnectionCreateRequest.  # noqa: E501

        Name of the vendor of the connection  # noqa: E501

        :return: The vendor_name of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._vendor_name

    @vendor_name.setter
    def vendor_name(self, vendor_name):
        """Sets the vendor_name of this LConnectionCreateRequest.

        Name of the vendor of the connection  # noqa: E501

        :param vendor_name: The vendor_name of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """
        if vendor_name is None:
            raise ValueError("Invalid value for `vendor_name`, must not be `None`")  # noqa: E501

        self._vendor_name = vendor_name

    @property
    def type(self):
        """Gets the type of this LConnectionCreateRequest.  # noqa: E501

        Type of connection  # noqa: E501

        :return: The type of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this LConnectionCreateRequest.

        Type of connection  # noqa: E501

        :param type: The type of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["jdbc", "rest", "remotefile"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def credential_type(self):
        """Gets the credential_type of this LConnectionCreateRequest.  # noqa: E501

         * `basic` - Simple username/password to be provided in the credentials property      * `securityToken` - Connection uses username, password and security token to authenticate. * `iamRoleArn` - Connection uses username, password and optiona IAM Role ARN to authenticate. * `iamDbUser` - Connection uses IAM and DbUser to connect to the database. * `oauth2` - Connection uses OAuth 2.0 to authenticate. * `keySecret` - connection uses key and secret to authenticate. * `apiKey` - Connection uses API Key for authentication. * `awsKeySecret` - Connection uses AWS Access Key and Secret Key for authentication. * `basicWithAppToken` - Connection uses Username, Password and Application Token for authentication. * `userWithApiToken` - Connection uses User and Api Token for authentication. * `basicApp` - Connection uses App Id and Password for authentication. * `transactionKey` - Connection uses Login ID and Transaction key for authentication. * `password` - Connection uses Password for authentication. * `apiKeyWithToken` - Connection uses API Key and Token for authentication. * `noAuth` - No authentication required for the connection. * `httpHeaderBasedAuth` - Connection uses http header based credentials for authentication. * `privateApp` - Connection uses privateApp token for authentication. * `httpQueryBasedAuth` - Connection uses http query based credentials for authentication. * `accessToken` - Connection uses access token for authentication. * `personalAccessToken` - Connection uses personal access token for authentication. * `tokenAuth` - Connection uses token based authentication. * `personalAccessTokenNameSecret` - Connection uses personal access token name and secret pair for authentication. * `convergedConnectorAuth` - Authentication Type implemented by the converged connector.  # noqa: E501

        :return: The credential_type of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._credential_type

    @credential_type.setter
    def credential_type(self, credential_type):
        """Sets the credential_type of this LConnectionCreateRequest.

         * `basic` - Simple username/password to be provided in the credentials property      * `securityToken` - Connection uses username, password and security token to authenticate. * `iamRoleArn` - Connection uses username, password and optiona IAM Role ARN to authenticate. * `iamDbUser` - Connection uses IAM and DbUser to connect to the database. * `oauth2` - Connection uses OAuth 2.0 to authenticate. * `keySecret` - connection uses key and secret to authenticate. * `apiKey` - Connection uses API Key for authentication. * `awsKeySecret` - Connection uses AWS Access Key and Secret Key for authentication. * `basicWithAppToken` - Connection uses Username, Password and Application Token for authentication. * `userWithApiToken` - Connection uses User and Api Token for authentication. * `basicApp` - Connection uses App Id and Password for authentication. * `transactionKey` - Connection uses Login ID and Transaction key for authentication. * `password` - Connection uses Password for authentication. * `apiKeyWithToken` - Connection uses API Key and Token for authentication. * `noAuth` - No authentication required for the connection. * `httpHeaderBasedAuth` - Connection uses http header based credentials for authentication. * `privateApp` - Connection uses privateApp token for authentication. * `httpQueryBasedAuth` - Connection uses http query based credentials for authentication. * `accessToken` - Connection uses access token for authentication. * `personalAccessToken` - Connection uses personal access token for authentication. * `tokenAuth` - Connection uses token based authentication. * `personalAccessTokenNameSecret` - Connection uses personal access token name and secret pair for authentication. * `convergedConnectorAuth` - Authentication Type implemented by the converged connector.  # noqa: E501

        :param credential_type: The credential_type of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """
        if credential_type is None:
            raise ValueError("Invalid value for `credential_type`, must not be `None`")  # noqa: E501
        allowed_values = ["basic", "securityToken", "iamRoleArn", "iamDbUser", "oauth2", "keySecret", "apiKey", "awsKeySecret", "basicWithAppToken", "userWithApiToken", "basicApp", "transactionKey", "password", "apiKeyWithToken", "noAuth", "httpHeaderBasedAuth", "privateApp", "httpQueryBasedAuth", "accessToken", "personalAccessToken", "tokenAuth", "personalAccessTokenNameSecret", "convergedConnectorAuth"]  # noqa: E501
        if credential_type not in allowed_values:
            raise ValueError(
                "Invalid value for `credential_type` ({0}), must be one of {1}"  # noqa: E501
                .format(credential_type, allowed_values)
            )

        self._credential_type = credential_type

    @property
    def advanced_credential_type(self):
        """Gets the advanced_credential_type of this LConnectionCreateRequest.  # noqa: E501

            # noqa: E501

        :return: The advanced_credential_type of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._advanced_credential_type

    @advanced_credential_type.setter
    def advanced_credential_type(self, advanced_credential_type):
        """Sets the advanced_credential_type of this LConnectionCreateRequest.

            # noqa: E501

        :param advanced_credential_type: The advanced_credential_type of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """

        self._advanced_credential_type = advanced_credential_type

    @property
    def ssh_tunneling(self):
        """Gets the ssh_tunneling of this LConnectionCreateRequest.  # noqa: E501

        When `true`, the Alteryx Analytics Cloud Platform uses SSH Tunneling to connect to the source  # noqa: E501

        :return: The ssh_tunneling of this LConnectionCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._ssh_tunneling

    @ssh_tunneling.setter
    def ssh_tunneling(self, ssh_tunneling):
        """Sets the ssh_tunneling of this LConnectionCreateRequest.

        When `true`, the Alteryx Analytics Cloud Platform uses SSH Tunneling to connect to the source  # noqa: E501

        :param ssh_tunneling: The ssh_tunneling of this LConnectionCreateRequest.  # noqa: E501
        :type: bool
        """

        self._ssh_tunneling = ssh_tunneling

    @property
    def ssl(self):
        """Gets the ssl of this LConnectionCreateRequest.  # noqa: E501

        When `true`, the Alteryx Analytics Cloud Platform uses SSL to connect to the source  # noqa: E501

        :return: The ssl of this LConnectionCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._ssl

    @ssl.setter
    def ssl(self, ssl):
        """Sets the ssl of this LConnectionCreateRequest.

        When `true`, the Alteryx Analytics Cloud Platform uses SSL to connect to the source  # noqa: E501

        :param ssl: The ssl of this LConnectionCreateRequest.  # noqa: E501
        :type: bool
        """

        self._ssl = ssl

    @property
    def name(self):
        """Gets the name of this LConnectionCreateRequest.  # noqa: E501

        Display name of the connection.  # noqa: E501

        :return: The name of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LConnectionCreateRequest.

        Display name of the connection.  # noqa: E501

        :param name: The name of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this LConnectionCreateRequest.  # noqa: E501

        User-friendly description for the connection.  # noqa: E501

        :return: The description of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this LConnectionCreateRequest.

        User-friendly description for the connection.  # noqa: E501

        :param description: The description of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def disable_type_inference(self):
        """Gets the disable_type_inference of this LConnectionCreateRequest.  # noqa: E501

        If set to false, type inference has been disabled for this connection. The default is true. When type inference has been disabled, the Alteryx Analytics Cloud Platform does not apply Alteryx Analytics Cloud types to data when it is imported.  # noqa: E501

        :return: The disable_type_inference of this LConnectionCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._disable_type_inference

    @disable_type_inference.setter
    def disable_type_inference(self, disable_type_inference):
        """Sets the disable_type_inference of this LConnectionCreateRequest.

        If set to false, type inference has been disabled for this connection. The default is true. When type inference has been disabled, the Alteryx Analytics Cloud Platform does not apply Alteryx Analytics Cloud types to data when it is imported.  # noqa: E501

        :param disable_type_inference: The disable_type_inference of this LConnectionCreateRequest.  # noqa: E501
        :type: bool
        """

        self._disable_type_inference = disable_type_inference

    @property
    def is_global(self):
        """Gets the is_global of this LConnectionCreateRequest.  # noqa: E501

        If `true`, the connection is public and available to all users. Default is false.  **NOTE**: After a connection has been made public, it cannot be made private again. It must be deleted and recreated.  # noqa: E501

        :return: The is_global of this LConnectionCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_global

    @is_global.setter
    def is_global(self, is_global):
        """Sets the is_global of this LConnectionCreateRequest.

        If `true`, the connection is public and available to all users. Default is false.  **NOTE**: After a connection has been made public, it cannot be made private again. It must be deleted and recreated.  # noqa: E501

        :param is_global: The is_global of this LConnectionCreateRequest.  # noqa: E501
        :type: bool
        """

        self._is_global = is_global

    @property
    def credentials_shared(self):
        """Gets the credentials_shared of this LConnectionCreateRequest.  # noqa: E501

        If `true`, the credentials used for the connection are available for use byusers who have been shared the connection.  # noqa: E501

        :return: The credentials_shared of this LConnectionCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._credentials_shared

    @credentials_shared.setter
    def credentials_shared(self, credentials_shared):
        """Sets the credentials_shared of this LConnectionCreateRequest.

        If `true`, the credentials used for the connection are available for use byusers who have been shared the connection.  # noqa: E501

        :param credentials_shared: The credentials_shared of this LConnectionCreateRequest.  # noqa: E501
        :type: bool
        """

        self._credentials_shared = credentials_shared

    @property
    def has_credentials(self):
        """Gets the has_credentials of this LConnectionCreateRequest.  # noqa: E501

        When `true`, the connection has credentials associated with it to connect to the source.  # noqa: E501

        :return: The has_credentials of this LConnectionCreateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._has_credentials

    @has_credentials.setter
    def has_credentials(self, has_credentials):
        """Sets the has_credentials of this LConnectionCreateRequest.

        When `true`, the connection has credentials associated with it to connect to the source.  # noqa: E501

        :param has_credentials: The has_credentials of this LConnectionCreateRequest.  # noqa: E501
        :type: bool
        """

        self._has_credentials = has_credentials

    @property
    def host(self):
        """Gets the host of this LConnectionCreateRequest.  # noqa: E501

        Host of the source  # noqa: E501

        :return: The host of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this LConnectionCreateRequest.

        Host of the source  # noqa: E501

        :param host: The host of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """

        self._host = host

    @property
    def port(self):
        """Gets the port of this LConnectionCreateRequest.  # noqa: E501

        Port number for the source  # noqa: E501

        :return: The port of this LConnectionCreateRequest.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this LConnectionCreateRequest.

        Port number for the source  # noqa: E501

        :param port: The port of this LConnectionCreateRequest.  # noqa: E501
        :type: int
        """

        self._port = port

    @property
    def bucket(self):
        """Gets the bucket of this LConnectionCreateRequest.  # noqa: E501

        bucket name for the source  # noqa: E501

        :return: The bucket of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """Sets the bucket of this LConnectionCreateRequest.

        bucket name for the source  # noqa: E501

        :param bucket: The bucket of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """

        self._bucket = bucket

    @property
    def params(self):
        """Gets the params of this LConnectionCreateRequest.  # noqa: E501

        This setting is populated with any parameters that are passed to the source duringconnection and operations. For relational sources, this setting may include thedefault database and extra load parameters.  # noqa: E501

        :return: The params of this LConnectionCreateRequest.  # noqa: E501
        :rtype: object
        """
        return self._params

    @params.setter
    def params(self, params):
        """Sets the params of this LConnectionCreateRequest.

        This setting is populated with any parameters that are passed to the source duringconnection and operations. For relational sources, this setting may include thedefault database and extra load parameters.  # noqa: E501

        :param params: The params of this LConnectionCreateRequest.  # noqa: E501
        :type: object
        """
        if params is None:
            raise ValueError("Invalid value for `params`, must not be `None`")  # noqa: E501

        self._params = params

    @property
    def oauth2_state_id(self):
        """Gets the oauth2_state_id of this LConnectionCreateRequest.  # noqa: E501


        :return: The oauth2_state_id of this LConnectionCreateRequest.  # noqa: E501
        :rtype: str
        """
        return self._oauth2_state_id

    @oauth2_state_id.setter
    def oauth2_state_id(self, oauth2_state_id):
        """Sets the oauth2_state_id of this LConnectionCreateRequest.


        :param oauth2_state_id: The oauth2_state_id of this LConnectionCreateRequest.  # noqa: E501
        :type: str
        """

        self._oauth2_state_id = oauth2_state_id

    @property
    def credentials(self):
        """Gets the credentials of this LConnectionCreateRequest.  # noqa: E501


        :return: The credentials of this LConnectionCreateRequest.  # noqa: E501
        :rtype: LAcceptedCredentials
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """Sets the credentials of this LConnectionCreateRequest.


        :param credentials: The credentials of this LConnectionCreateRequest.  # noqa: E501
        :type: LAcceptedCredentials
        """

        self._credentials = credentials

    @property
    def advanced_credentials(self):
        """Gets the advanced_credentials of this LConnectionCreateRequest.  # noqa: E501


        :return: The advanced_credentials of this LConnectionCreateRequest.  # noqa: E501
        :rtype: LAdvancedCredentialsInfo
        """
        return self._advanced_credentials

    @advanced_credentials.setter
    def advanced_credentials(self, advanced_credentials):
        """Sets the advanced_credentials of this LConnectionCreateRequest.


        :param advanced_credentials: The advanced_credentials of this LConnectionCreateRequest.  # noqa: E501
        :type: LAdvancedCredentialsInfo
        """

        self._advanced_credentials = advanced_credentials

    @property
    def endpoints(self):
        """Gets the endpoints of this LConnectionCreateRequest.  # noqa: E501


        :return: The endpoints of this LConnectionCreateRequest.  # noqa: E501
        :rtype: LJdbcRestEndpointsInfo
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints):
        """Sets the endpoints of this LConnectionCreateRequest.


        :param endpoints: The endpoints of this LConnectionCreateRequest.  # noqa: E501
        :type: LJdbcRestEndpointsInfo
        """

        self._endpoints = endpoints

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
        if issubclass(LConnectionCreateRequest, dict):
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
        if not isinstance(other, LConnectionCreateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
