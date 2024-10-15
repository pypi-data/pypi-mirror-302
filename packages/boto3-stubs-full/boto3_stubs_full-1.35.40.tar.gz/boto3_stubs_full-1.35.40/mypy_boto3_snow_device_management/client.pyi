"""
Type annotations for snow-device-management service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_snow_device_management.client import SnowDeviceManagementClient

    session = Session()
    client: SnowDeviceManagementClient = session.client("snow-device-management")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListDeviceResourcesPaginator,
    ListDevicesPaginator,
    ListExecutionsPaginator,
    ListTasksPaginator,
)
from .type_defs import (
    CancelTaskInputRequestTypeDef,
    CancelTaskOutputTypeDef,
    CreateTaskInputRequestTypeDef,
    CreateTaskOutputTypeDef,
    DescribeDeviceEc2InputRequestTypeDef,
    DescribeDeviceEc2OutputTypeDef,
    DescribeDeviceInputRequestTypeDef,
    DescribeDeviceOutputTypeDef,
    DescribeExecutionInputRequestTypeDef,
    DescribeExecutionOutputTypeDef,
    DescribeTaskInputRequestTypeDef,
    DescribeTaskOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    ListDeviceResourcesInputRequestTypeDef,
    ListDeviceResourcesOutputTypeDef,
    ListDevicesInputRequestTypeDef,
    ListDevicesOutputTypeDef,
    ListExecutionsInputRequestTypeDef,
    ListExecutionsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTasksInputRequestTypeDef,
    ListTasksOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SnowDeviceManagementClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SnowDeviceManagementClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SnowDeviceManagementClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#can_paginate)
        """

    def cancel_task(
        self, **kwargs: Unpack[CancelTaskInputRequestTypeDef]
    ) -> CancelTaskOutputTypeDef:
        """
        Sends a cancel request for a specified task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.cancel_task)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#cancel_task)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#close)
        """

    def create_task(
        self, **kwargs: Unpack[CreateTaskInputRequestTypeDef]
    ) -> CreateTaskOutputTypeDef:
        """
        Instructs one or more devices to start a task, such as unlocking or rebooting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.create_task)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#create_task)
        """

    def describe_device(
        self, **kwargs: Unpack[DescribeDeviceInputRequestTypeDef]
    ) -> DescribeDeviceOutputTypeDef:
        """
        Checks device-specific information, such as the device type, software version,
        IP addresses, and lock
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.describe_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#describe_device)
        """

    def describe_device_ec2_instances(
        self, **kwargs: Unpack[DescribeDeviceEc2InputRequestTypeDef]
    ) -> DescribeDeviceEc2OutputTypeDef:
        """
        Checks the current state of the Amazon EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.describe_device_ec2_instances)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#describe_device_ec2_instances)
        """

    def describe_execution(
        self, **kwargs: Unpack[DescribeExecutionInputRequestTypeDef]
    ) -> DescribeExecutionOutputTypeDef:
        """
        Checks the status of a remote task running on one or more target devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.describe_execution)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#describe_execution)
        """

    def describe_task(
        self, **kwargs: Unpack[DescribeTaskInputRequestTypeDef]
    ) -> DescribeTaskOutputTypeDef:
        """
        Checks the metadata for a given task on a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.describe_task)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#describe_task)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#generate_presigned_url)
        """

    def list_device_resources(
        self, **kwargs: Unpack[ListDeviceResourcesInputRequestTypeDef]
    ) -> ListDeviceResourcesOutputTypeDef:
        """
        Returns a list of the Amazon Web Services resources available for a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_device_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#list_device_resources)
        """

    def list_devices(
        self, **kwargs: Unpack[ListDevicesInputRequestTypeDef]
    ) -> ListDevicesOutputTypeDef:
        """
        Returns a list of all devices on your Amazon Web Services account that have
        Amazon Web Services Snow Device Management enabled in the Amazon Web Services
        Region where the command is
        run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_devices)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#list_devices)
        """

    def list_executions(
        self, **kwargs: Unpack[ListExecutionsInputRequestTypeDef]
    ) -> ListExecutionsOutputTypeDef:
        """
        Returns the status of tasks for one or more target devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_executions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#list_executions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns a list of tags for a managed device or task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#list_tags_for_resource)
        """

    def list_tasks(self, **kwargs: Unpack[ListTasksInputRequestTypeDef]) -> ListTasksOutputTypeDef:
        """
        Returns a list of tasks that can be filtered by state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_tasks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#list_tasks)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or replaces tags on a device or task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a tag from a device or task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_resources"]
    ) -> ListDeviceResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_devices"]) -> ListDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_executions"]) -> ListExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tasks"]) -> ListTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/client/#get_paginator)
        """
