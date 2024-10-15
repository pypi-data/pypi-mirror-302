"""
Type annotations for greengrassv2 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_greengrassv2.client import GreengrassV2Client

    session = Session()
    client: GreengrassV2Client = session.client("greengrassv2")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListClientDevicesAssociatedWithCoreDevicePaginator,
    ListComponentsPaginator,
    ListComponentVersionsPaginator,
    ListCoreDevicesPaginator,
    ListDeploymentsPaginator,
    ListEffectiveDeploymentsPaginator,
    ListInstalledComponentsPaginator,
)
from .type_defs import (
    AssociateServiceRoleToAccountRequestRequestTypeDef,
    AssociateServiceRoleToAccountResponseTypeDef,
    BatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef,
    BatchAssociateClientDeviceWithCoreDeviceResponseTypeDef,
    BatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef,
    BatchDisassociateClientDeviceFromCoreDeviceResponseTypeDef,
    CancelDeploymentRequestRequestTypeDef,
    CancelDeploymentResponseTypeDef,
    CreateComponentVersionRequestRequestTypeDef,
    CreateComponentVersionResponseTypeDef,
    CreateDeploymentRequestRequestTypeDef,
    CreateDeploymentResponseTypeDef,
    DeleteComponentRequestRequestTypeDef,
    DeleteCoreDeviceRequestRequestTypeDef,
    DeleteDeploymentRequestRequestTypeDef,
    DescribeComponentRequestRequestTypeDef,
    DescribeComponentResponseTypeDef,
    DisassociateServiceRoleFromAccountResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetComponentRequestRequestTypeDef,
    GetComponentResponseTypeDef,
    GetComponentVersionArtifactRequestRequestTypeDef,
    GetComponentVersionArtifactResponseTypeDef,
    GetConnectivityInfoRequestRequestTypeDef,
    GetConnectivityInfoResponseTypeDef,
    GetCoreDeviceRequestRequestTypeDef,
    GetCoreDeviceResponseTypeDef,
    GetDeploymentRequestRequestTypeDef,
    GetDeploymentResponseTypeDef,
    GetServiceRoleForAccountResponseTypeDef,
    ListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef,
    ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef,
    ListComponentsRequestRequestTypeDef,
    ListComponentsResponseTypeDef,
    ListComponentVersionsRequestRequestTypeDef,
    ListComponentVersionsResponseTypeDef,
    ListCoreDevicesRequestRequestTypeDef,
    ListCoreDevicesResponseTypeDef,
    ListDeploymentsRequestRequestTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEffectiveDeploymentsRequestRequestTypeDef,
    ListEffectiveDeploymentsResponseTypeDef,
    ListInstalledComponentsRequestRequestTypeDef,
    ListInstalledComponentsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ResolveComponentCandidatesRequestRequestTypeDef,
    ResolveComponentCandidatesResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateConnectivityInfoRequestRequestTypeDef,
    UpdateConnectivityInfoResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("GreengrassV2Client",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    RequestAlreadyInProgressException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class GreengrassV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GreengrassV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#exceptions)
        """

    def associate_service_role_to_account(
        self, **kwargs: Unpack[AssociateServiceRoleToAccountRequestRequestTypeDef]
    ) -> AssociateServiceRoleToAccountResponseTypeDef:
        """
        Associates a Greengrass service role with IoT Greengrass for your Amazon Web
        Services account in this Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.associate_service_role_to_account)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#associate_service_role_to_account)
        """

    def batch_associate_client_device_with_core_device(
        self, **kwargs: Unpack[BatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef]
    ) -> BatchAssociateClientDeviceWithCoreDeviceResponseTypeDef:
        """
        Associates a list of client devices with a core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.batch_associate_client_device_with_core_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#batch_associate_client_device_with_core_device)
        """

    def batch_disassociate_client_device_from_core_device(
        self, **kwargs: Unpack[BatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef]
    ) -> BatchDisassociateClientDeviceFromCoreDeviceResponseTypeDef:
        """
        Disassociates a list of client devices from a core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.batch_disassociate_client_device_from_core_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#batch_disassociate_client_device_from_core_device)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#can_paginate)
        """

    def cancel_deployment(
        self, **kwargs: Unpack[CancelDeploymentRequestRequestTypeDef]
    ) -> CancelDeploymentResponseTypeDef:
        """
        Cancels a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.cancel_deployment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#cancel_deployment)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#close)
        """

    def create_component_version(
        self, **kwargs: Unpack[CreateComponentVersionRequestRequestTypeDef]
    ) -> CreateComponentVersionResponseTypeDef:
        """
        Creates a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.create_component_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#create_component_version)
        """

    def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentRequestRequestTypeDef]
    ) -> CreateDeploymentResponseTypeDef:
        """
        Creates a continuous deployment for a target, which is a Greengrass core device
        or group of core
        devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.create_deployment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#create_deployment)
        """

    def delete_component(
        self, **kwargs: Unpack[DeleteComponentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a version of a component from IoT Greengrass.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.delete_component)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#delete_component)
        """

    def delete_core_device(
        self, **kwargs: Unpack[DeleteCoreDeviceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Greengrass core device, which is an IoT thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.delete_core_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#delete_core_device)
        """

    def delete_deployment(
        self, **kwargs: Unpack[DeleteDeploymentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.delete_deployment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#delete_deployment)
        """

    def describe_component(
        self, **kwargs: Unpack[DescribeComponentRequestRequestTypeDef]
    ) -> DescribeComponentResponseTypeDef:
        """
        Retrieves metadata for a version of a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.describe_component)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#describe_component)
        """

    def disassociate_service_role_from_account(
        self,
    ) -> DisassociateServiceRoleFromAccountResponseTypeDef:
        """
        Disassociates the Greengrass service role from IoT Greengrass for your Amazon
        Web Services account in this Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.disassociate_service_role_from_account)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#disassociate_service_role_from_account)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#generate_presigned_url)
        """

    def get_component(
        self, **kwargs: Unpack[GetComponentRequestRequestTypeDef]
    ) -> GetComponentResponseTypeDef:
        """
        Gets the recipe for a version of a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_component)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_component)
        """

    def get_component_version_artifact(
        self, **kwargs: Unpack[GetComponentVersionArtifactRequestRequestTypeDef]
    ) -> GetComponentVersionArtifactResponseTypeDef:
        """
        Gets the pre-signed URL to download a public or a Lambda component artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_component_version_artifact)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_component_version_artifact)
        """

    def get_connectivity_info(
        self, **kwargs: Unpack[GetConnectivityInfoRequestRequestTypeDef]
    ) -> GetConnectivityInfoResponseTypeDef:
        """
        Retrieves connectivity information for a Greengrass core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_connectivity_info)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_connectivity_info)
        """

    def get_core_device(
        self, **kwargs: Unpack[GetCoreDeviceRequestRequestTypeDef]
    ) -> GetCoreDeviceResponseTypeDef:
        """
        Retrieves metadata for a Greengrass core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_core_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_core_device)
        """

    def get_deployment(
        self, **kwargs: Unpack[GetDeploymentRequestRequestTypeDef]
    ) -> GetDeploymentResponseTypeDef:
        """
        Gets a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_deployment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_deployment)
        """

    def get_service_role_for_account(self) -> GetServiceRoleForAccountResponseTypeDef:
        """
        Gets the service role associated with IoT Greengrass for your Amazon Web
        Services account in this Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_service_role_for_account)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_service_role_for_account)
        """

    def list_client_devices_associated_with_core_device(
        self, **kwargs: Unpack[ListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef]
    ) -> ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef:
        """
        Retrieves a paginated list of client devices that are associated with a core
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_client_devices_associated_with_core_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#list_client_devices_associated_with_core_device)
        """

    def list_component_versions(
        self, **kwargs: Unpack[ListComponentVersionsRequestRequestTypeDef]
    ) -> ListComponentVersionsResponseTypeDef:
        """
        Retrieves a paginated list of all versions for a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_component_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#list_component_versions)
        """

    def list_components(
        self, **kwargs: Unpack[ListComponentsRequestRequestTypeDef]
    ) -> ListComponentsResponseTypeDef:
        """
        Retrieves a paginated list of component summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_components)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#list_components)
        """

    def list_core_devices(
        self, **kwargs: Unpack[ListCoreDevicesRequestRequestTypeDef]
    ) -> ListCoreDevicesResponseTypeDef:
        """
        Retrieves a paginated list of Greengrass core devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_core_devices)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#list_core_devices)
        """

    def list_deployments(
        self, **kwargs: Unpack[ListDeploymentsRequestRequestTypeDef]
    ) -> ListDeploymentsResponseTypeDef:
        """
        Retrieves a paginated list of deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_deployments)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#list_deployments)
        """

    def list_effective_deployments(
        self, **kwargs: Unpack[ListEffectiveDeploymentsRequestRequestTypeDef]
    ) -> ListEffectiveDeploymentsResponseTypeDef:
        """
        Retrieves a paginated list of deployment jobs that IoT Greengrass sends to
        Greengrass core
        devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_effective_deployments)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#list_effective_deployments)
        """

    def list_installed_components(
        self, **kwargs: Unpack[ListInstalledComponentsRequestRequestTypeDef]
    ) -> ListInstalledComponentsResponseTypeDef:
        """
        Retrieves a paginated list of the components that a Greengrass core device runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_installed_components)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#list_installed_components)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags for an IoT Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#list_tags_for_resource)
        """

    def resolve_component_candidates(
        self, **kwargs: Unpack[ResolveComponentCandidatesRequestRequestTypeDef]
    ) -> ResolveComponentCandidatesResponseTypeDef:
        """
        Retrieves a list of components that meet the component, version, and platform
        requirements of a
        deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.resolve_component_candidates)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#resolve_component_candidates)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to an IoT Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from an IoT Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#untag_resource)
        """

    def update_connectivity_info(
        self, **kwargs: Unpack[UpdateConnectivityInfoRequestRequestTypeDef]
    ) -> UpdateConnectivityInfoResponseTypeDef:
        """
        Updates connectivity information for a Greengrass core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.update_connectivity_info)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#update_connectivity_info)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_client_devices_associated_with_core_device"]
    ) -> ListClientDevicesAssociatedWithCoreDevicePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_component_versions"]
    ) -> ListComponentVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_components"]) -> ListComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_core_devices"]
    ) -> ListCoreDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_effective_deployments"]
    ) -> ListEffectiveDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_installed_components"]
    ) -> ListInstalledComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/client/#get_paginator)
        """
