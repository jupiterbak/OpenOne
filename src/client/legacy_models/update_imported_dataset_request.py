# coding: utf-8

"""
    Alteryx Analytics Cloud API

      # Overview  To enable programmatic control over its objects, the Alteryx Analytics Cloud Platform supports a range of REST API endpoints across its objects. This section provides an overview of the API design, methods, and supported use cases.  Most of the endpoints accept `JSON` as input and return `JSON` responses. This means that you must usually add the following headers to your request: ``` Content-type: application/json Accept: application/json ```    <small><!--__VERSION__--></small>  ## Resources  The term `resource` refers to a single type of object in the Alteryx Analytics Cloud Platform metadata. An API is broken up by its endpoint's corresponding resource. The name of a resource is typically plural, and expressed in camelCase. Example: `jobGroups`.  Resource names are used as part of endpoint URLs, as well as in API parameters and responses.  ## CRUD Operations  The platform supports **C**reate, **R**ead, **U**pdate, and **D**elete operations on most resources.  You can review the standards for these operations and their standard parameters below.  Some endpoints have special behavior as exceptions.  ### Create  To create a resource, you typically submit an HTTP `POST` request with the resource's required metadata in the request body. The response returns a `201 Created` response code upon success with the resource's metadata, including its internal `id`, in the response body.  ### Read  An HTTP `GET` request can be used to read a resource or to list a number of resources.  A resource's `id` can be submitted in the request parameters to read a specific resource. The response usually returns a `200 OK` response code upon success, with the resource's metadata in the response body.  If a `GET` request does not include a specific resource `id`, it is treated as a list request. The response usually returns a `200 OK` response code upon success, with an object containing a list of resources' metadata in the response body.   When reading resources, some common query parameters are usually available. e.g.: ``` /v4/jobGroups?limit=100&includeDeleted=true&embed=jobs ```  |Query Parameter|Type|Description| |---------------|----|-----------| |embed|string|Comma-separated list of objects to include part of the response. See [Embedding resources](#section/Overview/Embedding-Resources).| |includeDeleted|string|If set to `true`, response includes deleted objects.| |limit|integer|Maximum number of objects to fetch. Usually 25 by default| |offset|integer|Offset after which to start returning objects. For use with limit query parameter.|  ### Update  Updating a resource requires the resource `id`, and is typically done using an HTTP `PUT` or `PATCH` request, with the fields to modify in the request body. The response usually returns a `200 OK` response code upon success, with minimal information about the modified resource in the response body.  ### Delete  Deleting a resource requires the resource `id` and is typically executing via an HTTP `DELETE` request. The response usually returns a `204 No Content` response code upon success.  ## Conventions - Resource names are plural and expressed in camelCase. - Resource names are consistent between main URL and URL parameter.  - Parameter lists are consistently enveloped in the following manner: ``` { \"data\": [{ ... }] } ```  - Field names are in camelCase and are consistent with the resource name in the URL or with the embed URL parameter. ``` \"creator\": { \"id\": 1 }, \"updater\": { \"id\": 2 }, ```  ## Embedding Resources  When reading a resource, the platform supports an `embed` query parameter for most resources, which allows the caller to ask for associated resources in the response. Use of this parameter requires knowledge of how different resources are related to each other and is suggested for advanced users only.  In the following example, the sub-jobs of a [jobGroup](#tag/JobGroup) are embedded in the response for jobGroup=1:  ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=jobs ```  If you provide an invalid embedding, you will get an error message. The response will contain the list of possible resources that can be embedded. e.g. ``` https://us1.alteryxcloud.com/v4/jobGroups/1?embed=* ```  Example error: ``` {   \"exception\": {     \"name\": \"ValidationFailed\",     \"message\": \"Input validation failed\",     \"details\": \"No association * in flows! Valid associations are creator, updater, snapshots...\"   } } ```  ### Fields  It is possible to let the application know that you need fewer data to improve the performance of the endpoints using the `fields` query parameter. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name ```  The list of fields need to be separated by semi-colons `;`. Note that the application might sometimes return more fields than requested.  You can also use it while embedding resources. ``` https://us1.alteryxcloud.com/v4/flows?fields=id;name&embed=flownodes(fields=id) ```  ### Limit and sorting You can limit and sort the number of embedded resources for some associations. e.g. ``` https://us1.alteryxcloud.com/v4/flows?fields=id&embed=flownodes(limit=1,fields=id,sort=-id) ```  Note that not all association support this. An error is returned when it is not possible to limit the number of embedded results.  ## Errors The Alteryx Analytics Cloud Platform uses HTTP response codes to indicate the success or failure of an API request.  - Codes in the 2xx range indicate success.  - Codes in the 4xx range indicate that the information provided is invalid (invalid parameters, missing permissions, etc.) - Codes in the 5xx range indicate an error on the servers. These are rare and should usually go away when retrying. If you experience a lot of 5xx errors, contact support.   |HTTP Status Code (client errors)|Notes| |--------------------------------|-----| |400 Bad Request |Potential reasons: <ul><li>Resource doesn't exist</li><li>Request is incorrectly formatted</li><li>Request contains invalid values</li></ul> | |403 Forbidden   |Incorrect permissions to access the Resource.| |404 Not Found   |Resource cannot be found.| |410 Gone        |Resource has been previously deleted.| |415 Unsupported Media Type|Incorrect `Accept` or `Content-type` header|   ## Request Ids  Each request has a request identifier, which can be found in the response headers, in the following form: ``` x-trifacta-request-id: <myRequestId> ```  > ℹ️ **NOTE**: If you have an issue with a specific request, please include the `x-trifacta-request-id` value when you contact support    ## Versioning and Endpoint Lifecycle  - API versioning is not synchronized to specific releases of the platform.  - APIs are designed to be backward compatible. - Any changes to the API will first go through a deprecation phase.  ## Rate limiting  The Alteryx Analytics Cloud Platform applies a per-minute limit to the number of request received by the API for some endpoints. Users who send too many requests receive a HTTP status code `429` error response. For applicable endpoints, the quota is documented under the endpoint description.  Treat these limits as maximums and don't try to generate unnecessary load.  Notes: * Limits may be changed or reduced at any time to prevent abuse. * Some endpoints may queue requests if the rate-limit is reached. * If you have special rate requirements, please contact Support.  ### Handling rate limiting In case you need to trigger many requests on short interval, you can watch for the `429` status code and build a retry mechanism. The retry mechanism should follow an exponential backoff schedule to reduce request volume. Adding some randomness to the backoff schedule is recommended.  ### Response headers For endpoints which are subject to low rate-limits, response headers will be included in the request and indicate how many requests are left for the current interval. You can use these to avoid blindly retrying.   Example response headers for an endpoint limited to 30 requests/user/min and 60 requests/workspace/min  |Header name|Description| |-----------|-----------| |`x-rate-limit-user-limit`|The maximum number of requests you're permitted to make per user per minute (e.g. `30`)| |`x-rate-limit-user-remaining`|The number of requests remaining in the current rate limit window. (e.g. `28`)| |`x-rate-limit-user-reset`|The time at which the current rate limit window resets in UTC epoch seconds (e.g. `1631095033096`)| |`x-rate-limit-workspace-limit`|The maximum number of requests you're permitted to make per workspace per minute (e.g. `60`)| |`x-rate-limit-workspace-remaining`|The number of requests remaining in the current rate limit window. (e.g. `38`)| |`x-rate-limit-workspace-reset`|The time at which the current rate limit window resets in UTC epoch milliseconds (e.g. `1631095033096`)| |`x-retry-after`|Number of seconds until the current rate limit window resets (e.g. `42`)|  #### Example error If you exceed the rate limit, an error response is returned:  ``` curl -i -X POST 'https://api.clouddataprep.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }'  HTTP/1.1 429 Too Many Requests x-rate-limit-user-limit: 30 x-rate-limit-user-remaining: 0 x-rate-limit-user-reset: 1631096271696 x-retry-after: 57  {   \"exception\": {     \"name\": \"TooManyRequestsException\",     \"message\": \"Too Many Requests\",     \"details\": \"API quota reached for \\\"runJobGroup\\\". Wait 57 seconds before making a new request. (Max. 30 requests allowed per minute per user.)\"   } } ```  # Trying the API You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or the [Insomnia rest client](https://insomnia.rest/) to test the Alteryx Analytics Cloud API.  > ⚠️ **When testing the API, bear in mind that you are working with your live production data, not sample data or test data.**  Note that you will need to pass an API token with each request.   For e.g., here is how to run a job with [curl](https://curl.haxx.se/): ``` curl -X POST 'https://us1.alteryxcloud.com/v4/jobGroups' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer <token>' \\ -d '{ \"wrangledDataset\": { \"id\": \"<recipe-id>\" } }' ```  Using a graphical tool such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), it is possible to import the API specifications directly: 1. Download the API specification by clicking the **Download** button at top of this document 2. Import the JSON specification in the graphical tool of your choice.    - In *Postman*, you can click the **import** button at the top   - With *Insomnia*, you can just drag-and-drop the file on the UI  Note that with *Postman*, you can also generate code snippets by selecting a request and clicking on the **Code** button.   # noqa: E501

    OpenAPI spec version: v2025.23.2
     
"""

import pprint
import re  # noqa: F401

import six

class LUpdateImportedDatasetRequest(object):
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
        'id': 'int',
        'job_status': 'str',
        'jobgroup_id': 'str',
        'visible': 'bool',
        'is_pending': 'bool',
        'num_flows': 'int',
        'bucket_name': 'str',
        'dynamic_bucket': 'str',
        'dynamic_host': 'str',
        'dynamic_user_info': 'str',
        'name': 'str',
        'description': 'str',
        'disable_type_inference': 'bool',
        'type': 'str',
        'is_converted': 'bool',
        'is_dynamic': 'bool',
        'host': 'str',
        'userinfo': 'str',
        'bucket': 'str',
        'raw': 'str',
        'path': 'str',
        'dynamic_path': 'str',
        'run_parameters': 'list[LRunParameterInfo]',
        'is_hidden': 'bool',
        'table_name': 'str',
        'relational_path': 'list[str]',
        'columns': 'list[str]'
    }

    attribute_map = {
        'id': 'id',
        'job_status': 'jobStatus',
        'jobgroup_id': 'jobgroupId',
        'visible': 'visible',
        'is_pending': 'isPending',
        'num_flows': 'numFlows',
        'bucket_name': 'bucketName',
        'dynamic_bucket': 'dynamicBucket',
        'dynamic_host': 'dynamicHost',
        'dynamic_user_info': 'dynamicUserInfo',
        'name': 'name',
        'description': 'description',
        'disable_type_inference': 'disableTypeInference',
        'type': 'type',
        'is_converted': 'isConverted',
        'is_dynamic': 'isDynamic',
        'host': 'host',
        'userinfo': 'userinfo',
        'bucket': 'bucket',
        'raw': 'raw',
        'path': 'path',
        'dynamic_path': 'dynamicPath',
        'run_parameters': 'runParameters',
        'is_hidden': 'isHidden',
        'table_name': 'tableName',
        'relational_path': 'relationalPath',
        'columns': 'columns'
    }

    def __init__(self, id=None, job_status=None, jobgroup_id=None, visible=None, is_pending=None, num_flows=None, bucket_name=None, dynamic_bucket=None, dynamic_host=None, dynamic_user_info=None, name=None, description=None, disable_type_inference=None, type=None, is_converted=None, is_dynamic=False, host=None, userinfo=None, bucket=None, raw=None, path=None, dynamic_path=None, run_parameters=None, is_hidden=None, table_name=None, relational_path=None, columns=None):  # noqa: E501
        """LUpdateImportedDatasetRequest - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._job_status = None
        self._jobgroup_id = None
        self._visible = None
        self._is_pending = None
        self._num_flows = None
        self._bucket_name = None
        self._dynamic_bucket = None
        self._dynamic_host = None
        self._dynamic_user_info = None
        self._name = None
        self._description = None
        self._disable_type_inference = None
        self._type = None
        self._is_converted = None
        self._is_dynamic = None
        self._host = None
        self._userinfo = None
        self._bucket = None
        self._raw = None
        self._path = None
        self._dynamic_path = None
        self._run_parameters = None
        self._is_hidden = None
        self._table_name = None
        self._relational_path = None
        self._columns = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if job_status is not None:
            self.job_status = job_status
        if jobgroup_id is not None:
            self.jobgroup_id = jobgroup_id
        if visible is not None:
            self.visible = visible
        if is_pending is not None:
            self.is_pending = is_pending
        if num_flows is not None:
            self.num_flows = num_flows
        if bucket_name is not None:
            self.bucket_name = bucket_name
        if dynamic_bucket is not None:
            self.dynamic_bucket = dynamic_bucket
        if dynamic_host is not None:
            self.dynamic_host = dynamic_host
        if dynamic_user_info is not None:
            self.dynamic_user_info = dynamic_user_info
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if disable_type_inference is not None:
            self.disable_type_inference = disable_type_inference
        if type is not None:
            self.type = type
        if is_converted is not None:
            self.is_converted = is_converted
        if is_dynamic is not None:
            self.is_dynamic = is_dynamic
        if host is not None:
            self.host = host
        if userinfo is not None:
            self.userinfo = userinfo
        if bucket is not None:
            self.bucket = bucket
        if raw is not None:
            self.raw = raw
        if path is not None:
            self.path = path
        if dynamic_path is not None:
            self.dynamic_path = dynamic_path
        if run_parameters is not None:
            self.run_parameters = run_parameters
        if is_hidden is not None:
            self.is_hidden = is_hidden
        if table_name is not None:
            self.table_name = table_name
        if relational_path is not None:
            self.relational_path = relational_path
        if columns is not None:
            self.columns = columns

    @property
    def id(self):
        """Gets the id of this LUpdateImportedDatasetRequest.  # noqa: E501

        unique identifier for this object.  # noqa: E501

        :return: The id of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this LUpdateImportedDatasetRequest.

        unique identifier for this object.  # noqa: E501

        :param id: The id of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def job_status(self):
        """Gets the job_status of this LUpdateImportedDatasetRequest.  # noqa: E501


        :return: The job_status of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._job_status

    @job_status.setter
    def job_status(self, job_status):
        """Sets the job_status of this LUpdateImportedDatasetRequest.


        :param job_status: The job_status of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._job_status = job_status

    @property
    def jobgroup_id(self):
        """Gets the jobgroup_id of this LUpdateImportedDatasetRequest.  # noqa: E501


        :return: The jobgroup_id of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._jobgroup_id

    @jobgroup_id.setter
    def jobgroup_id(self, jobgroup_id):
        """Sets the jobgroup_id of this LUpdateImportedDatasetRequest.


        :param jobgroup_id: The jobgroup_id of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._jobgroup_id = jobgroup_id

    @property
    def visible(self):
        """Gets the visible of this LUpdateImportedDatasetRequest.  # noqa: E501


        :return: The visible of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: bool
        """
        return self._visible

    @visible.setter
    def visible(self, visible):
        """Sets the visible of this LUpdateImportedDatasetRequest.


        :param visible: The visible of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: bool
        """

        self._visible = visible

    @property
    def is_pending(self):
        """Gets the is_pending of this LUpdateImportedDatasetRequest.  # noqa: E501


        :return: The is_pending of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_pending

    @is_pending.setter
    def is_pending(self, is_pending):
        """Sets the is_pending of this LUpdateImportedDatasetRequest.


        :param is_pending: The is_pending of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: bool
        """

        self._is_pending = is_pending

    @property
    def num_flows(self):
        """Gets the num_flows of this LUpdateImportedDatasetRequest.  # noqa: E501


        :return: The num_flows of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: int
        """
        return self._num_flows

    @num_flows.setter
    def num_flows(self, num_flows):
        """Sets the num_flows of this LUpdateImportedDatasetRequest.


        :param num_flows: The num_flows of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: int
        """

        self._num_flows = num_flows

    @property
    def bucket_name(self):
        """Gets the bucket_name of this LUpdateImportedDatasetRequest.  # noqa: E501


        :return: The bucket_name of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """Sets the bucket_name of this LUpdateImportedDatasetRequest.


        :param bucket_name: The bucket_name of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._bucket_name = bucket_name

    @property
    def dynamic_bucket(self):
        """Gets the dynamic_bucket of this LUpdateImportedDatasetRequest.  # noqa: E501

        Bucket used when resolving the parameters. It is used when running a job or collecting a sample. It is different from the one used as a storage location which corresponds to the first match. The latter is used when doing a fast preview in the UI.  # noqa: E501

        :return: The dynamic_bucket of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._dynamic_bucket

    @dynamic_bucket.setter
    def dynamic_bucket(self, dynamic_bucket):
        """Sets the dynamic_bucket of this LUpdateImportedDatasetRequest.

        Bucket used when resolving the parameters. It is used when running a job or collecting a sample. It is different from the one used as a storage location which corresponds to the first match. The latter is used when doing a fast preview in the UI.  # noqa: E501

        :param dynamic_bucket: The dynamic_bucket of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._dynamic_bucket = dynamic_bucket

    @property
    def dynamic_host(self):
        """Gets the dynamic_host of this LUpdateImportedDatasetRequest.  # noqa: E501

        Host used when resolving the parameters. It is used when running a job or collecting a sample. It is different from the one used as a storage location which corresponds to the first match. The latter is used when doing a fast preview in the UI.  # noqa: E501

        :return: The dynamic_host of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._dynamic_host

    @dynamic_host.setter
    def dynamic_host(self, dynamic_host):
        """Sets the dynamic_host of this LUpdateImportedDatasetRequest.

        Host used when resolving the parameters. It is used when running a job or collecting a sample. It is different from the one used as a storage location which corresponds to the first match. The latter is used when doing a fast preview in the UI.  # noqa: E501

        :param dynamic_host: The dynamic_host of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._dynamic_host = dynamic_host

    @property
    def dynamic_user_info(self):
        """Gets the dynamic_user_info of this LUpdateImportedDatasetRequest.  # noqa: E501

        User used when resolving the parameters. It is used when running a job or collecting a sample. It is different from the one used as a storage location which corresponds to the first match. The latter is used when doing a fast preview in the UI.  # noqa: E501

        :return: The dynamic_user_info of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._dynamic_user_info

    @dynamic_user_info.setter
    def dynamic_user_info(self, dynamic_user_info):
        """Sets the dynamic_user_info of this LUpdateImportedDatasetRequest.

        User used when resolving the parameters. It is used when running a job or collecting a sample. It is different from the one used as a storage location which corresponds to the first match. The latter is used when doing a fast preview in the UI.  # noqa: E501

        :param dynamic_user_info: The dynamic_user_info of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._dynamic_user_info = dynamic_user_info

    @property
    def name(self):
        """Gets the name of this LUpdateImportedDatasetRequest.  # noqa: E501

        Display name of the imported dataset.  # noqa: E501

        :return: The name of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LUpdateImportedDatasetRequest.

        Display name of the imported dataset.  # noqa: E501

        :param name: The name of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this LUpdateImportedDatasetRequest.  # noqa: E501

        User-friendly description for the imported dataset.  # noqa: E501

        :return: The description of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this LUpdateImportedDatasetRequest.

        User-friendly description for the imported dataset.  # noqa: E501

        :param description: The description of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def disable_type_inference(self):
        """Gets the disable_type_inference of this LUpdateImportedDatasetRequest.  # noqa: E501

        Only applicable to relational sources (database tables/views for e.g.). Prevent Alteryx Analytics Cloud type inference from running and inferring types by looking at the first rows of the dataset.  # noqa: E501

        :return: The disable_type_inference of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: bool
        """
        return self._disable_type_inference

    @disable_type_inference.setter
    def disable_type_inference(self, disable_type_inference):
        """Sets the disable_type_inference of this LUpdateImportedDatasetRequest.

        Only applicable to relational sources (database tables/views for e.g.). Prevent Alteryx Analytics Cloud type inference from running and inferring types by looking at the first rows of the dataset.  # noqa: E501

        :param disable_type_inference: The disable_type_inference of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: bool
        """

        self._disable_type_inference = disable_type_inference

    @property
    def type(self):
        """Gets the type of this LUpdateImportedDatasetRequest.  # noqa: E501

        Indicate the type of dataset. If not specified, the default storage protocol is used.  # noqa: E501

        :return: The type of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this LUpdateImportedDatasetRequest.

        Indicate the type of dataset. If not specified, the default storage protocol is used.  # noqa: E501

        :param type: The type of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def is_converted(self):
        """Gets the is_converted of this LUpdateImportedDatasetRequest.  # noqa: E501

        Indicate if the imported dataset is converted. This is the case for Microsoft Excel Dataset for e.g.  # noqa: E501

        :return: The is_converted of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_converted

    @is_converted.setter
    def is_converted(self, is_converted):
        """Sets the is_converted of this LUpdateImportedDatasetRequest.

        Indicate if the imported dataset is converted. This is the case for Microsoft Excel Dataset for e.g.  # noqa: E501

        :param is_converted: The is_converted of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: bool
        """

        self._is_converted = is_converted

    @property
    def is_dynamic(self):
        """Gets the is_dynamic of this LUpdateImportedDatasetRequest.  # noqa: E501

        indicate if the datasource is parameterized. In that case, a `dynamicPath` should be passed.  # noqa: E501

        :return: The is_dynamic of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_dynamic

    @is_dynamic.setter
    def is_dynamic(self, is_dynamic):
        """Sets the is_dynamic of this LUpdateImportedDatasetRequest.

        indicate if the datasource is parameterized. In that case, a `dynamicPath` should be passed.  # noqa: E501

        :param is_dynamic: The is_dynamic of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: bool
        """

        self._is_dynamic = is_dynamic

    @property
    def host(self):
        """Gets the host of this LUpdateImportedDatasetRequest.  # noqa: E501

        Host for the dataset  # noqa: E501

        :return: The host of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this LUpdateImportedDatasetRequest.

        Host for the dataset  # noqa: E501

        :param host: The host of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._host = host

    @property
    def userinfo(self):
        """Gets the userinfo of this LUpdateImportedDatasetRequest.  # noqa: E501

        User info for the dataset  # noqa: E501

        :return: The userinfo of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._userinfo

    @userinfo.setter
    def userinfo(self, userinfo):
        """Sets the userinfo of this LUpdateImportedDatasetRequest.

        User info for the dataset  # noqa: E501

        :param userinfo: The userinfo of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._userinfo = userinfo

    @property
    def bucket(self):
        """Gets the bucket of this LUpdateImportedDatasetRequest.  # noqa: E501

        The bucket is required if the datasource is stored in a bucket file system.  # noqa: E501

        :return: The bucket of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """Sets the bucket of this LUpdateImportedDatasetRequest.

        The bucket is required if the datasource is stored in a bucket file system.  # noqa: E501

        :param bucket: The bucket of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._bucket = bucket

    @property
    def raw(self):
        """Gets the raw of this LUpdateImportedDatasetRequest.  # noqa: E501

        Raw SQL query  # noqa: E501

        :return: The raw of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._raw

    @raw.setter
    def raw(self, raw):
        """Sets the raw of this LUpdateImportedDatasetRequest.

        Raw SQL query  # noqa: E501

        :param raw: The raw of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._raw = raw

    @property
    def path(self):
        """Gets the path of this LUpdateImportedDatasetRequest.  # noqa: E501


        :return: The path of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this LUpdateImportedDatasetRequest.


        :param path: The path of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def dynamic_path(self):
        """Gets the dynamic_path of this LUpdateImportedDatasetRequest.  # noqa: E501

        Path used when resolving the parameters. It is used when running a job or collecting a sample. It is different from the one used as a storage location which corresponds to the first match. The latter is used when doing a fast preview in the UI.  # noqa: E501

        :return: The dynamic_path of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._dynamic_path

    @dynamic_path.setter
    def dynamic_path(self, dynamic_path):
        """Sets the dynamic_path of this LUpdateImportedDatasetRequest.

        Path used when resolving the parameters. It is used when running a job or collecting a sample. It is different from the one used as a storage location which corresponds to the first match. The latter is used when doing a fast preview in the UI.  # noqa: E501

        :param dynamic_path: The dynamic_path of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._dynamic_path = dynamic_path

    @property
    def run_parameters(self):
        """Gets the run_parameters of this LUpdateImportedDatasetRequest.  # noqa: E501


        :return: The run_parameters of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: list[LRunParameterInfo]
        """
        return self._run_parameters

    @run_parameters.setter
    def run_parameters(self, run_parameters):
        """Sets the run_parameters of this LUpdateImportedDatasetRequest.


        :param run_parameters: The run_parameters of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: list[LRunParameterInfo]
        """

        self._run_parameters = run_parameters

    @property
    def is_hidden(self):
        """Gets the is_hidden of this LUpdateImportedDatasetRequest.  # noqa: E501


        :return: The is_hidden of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, is_hidden):
        """Sets the is_hidden of this LUpdateImportedDatasetRequest.


        :param is_hidden: The is_hidden of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: bool
        """

        self._is_hidden = is_hidden

    @property
    def table_name(self):
        """Gets the table_name of this LUpdateImportedDatasetRequest.  # noqa: E501

        The name of the database table for this datasource. Used when updating a relational source.  # noqa: E501

        :return: The table_name of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: str
        """
        return self._table_name

    @table_name.setter
    def table_name(self, table_name):
        """Sets the table_name of this LUpdateImportedDatasetRequest.

        The name of the database table for this datasource. Used when updating a relational source.  # noqa: E501

        :param table_name: The table_name of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: str
        """

        self._table_name = table_name

    @property
    def relational_path(self):
        """Gets the relational_path of this LUpdateImportedDatasetRequest.  # noqa: E501

        The path to the table. Used when updating a relational source.  # noqa: E501

        :return: The relational_path of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._relational_path

    @relational_path.setter
    def relational_path(self, relational_path):
        """Sets the relational_path of this LUpdateImportedDatasetRequest.

        The path to the table. Used when updating a relational source.  # noqa: E501

        :param relational_path: The relational_path of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: list[str]
        """

        self._relational_path = relational_path

    @property
    def columns(self):
        """Gets the columns of this LUpdateImportedDatasetRequest.  # noqa: E501

        List of column names to use for the datasource. Used when updating a relational source.  # noqa: E501

        :return: The columns of this LUpdateImportedDatasetRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._columns

    @columns.setter
    def columns(self, columns):
        """Sets the columns of this LUpdateImportedDatasetRequest.

        List of column names to use for the datasource. Used when updating a relational source.  # noqa: E501

        :param columns: The columns of this LUpdateImportedDatasetRequest.  # noqa: E501
        :type: list[str]
        """

        self._columns = columns

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
        if issubclass(LUpdateImportedDatasetRequest, dict):
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
        if not isinstance(other, LUpdateImportedDatasetRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
