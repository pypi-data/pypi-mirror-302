"""
Type annotations for networkmanager service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_networkmanager.client import NetworkManagerClient

    session = Session()
    client: NetworkManagerClient = session.client("networkmanager")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeGlobalNetworksPaginator,
    GetConnectionsPaginator,
    GetConnectPeerAssociationsPaginator,
    GetCoreNetworkChangeEventsPaginator,
    GetCoreNetworkChangeSetPaginator,
    GetCustomerGatewayAssociationsPaginator,
    GetDevicesPaginator,
    GetLinkAssociationsPaginator,
    GetLinksPaginator,
    GetNetworkResourceCountsPaginator,
    GetNetworkResourceRelationshipsPaginator,
    GetNetworkResourcesPaginator,
    GetNetworkTelemetryPaginator,
    GetSitesPaginator,
    GetTransitGatewayConnectPeerAssociationsPaginator,
    GetTransitGatewayRegistrationsPaginator,
    ListAttachmentsPaginator,
    ListConnectPeersPaginator,
    ListCoreNetworkPolicyVersionsPaginator,
    ListCoreNetworksPaginator,
    ListPeeringsPaginator,
)
from .type_defs import (
    AcceptAttachmentRequestRequestTypeDef,
    AcceptAttachmentResponseTypeDef,
    AssociateConnectPeerRequestRequestTypeDef,
    AssociateConnectPeerResponseTypeDef,
    AssociateCustomerGatewayRequestRequestTypeDef,
    AssociateCustomerGatewayResponseTypeDef,
    AssociateLinkRequestRequestTypeDef,
    AssociateLinkResponseTypeDef,
    AssociateTransitGatewayConnectPeerRequestRequestTypeDef,
    AssociateTransitGatewayConnectPeerResponseTypeDef,
    CreateConnectAttachmentRequestRequestTypeDef,
    CreateConnectAttachmentResponseTypeDef,
    CreateConnectionRequestRequestTypeDef,
    CreateConnectionResponseTypeDef,
    CreateConnectPeerRequestRequestTypeDef,
    CreateConnectPeerResponseTypeDef,
    CreateCoreNetworkRequestRequestTypeDef,
    CreateCoreNetworkResponseTypeDef,
    CreateDeviceRequestRequestTypeDef,
    CreateDeviceResponseTypeDef,
    CreateGlobalNetworkRequestRequestTypeDef,
    CreateGlobalNetworkResponseTypeDef,
    CreateLinkRequestRequestTypeDef,
    CreateLinkResponseTypeDef,
    CreateSiteRequestRequestTypeDef,
    CreateSiteResponseTypeDef,
    CreateSiteToSiteVpnAttachmentRequestRequestTypeDef,
    CreateSiteToSiteVpnAttachmentResponseTypeDef,
    CreateTransitGatewayPeeringRequestRequestTypeDef,
    CreateTransitGatewayPeeringResponseTypeDef,
    CreateTransitGatewayRouteTableAttachmentRequestRequestTypeDef,
    CreateTransitGatewayRouteTableAttachmentResponseTypeDef,
    CreateVpcAttachmentRequestRequestTypeDef,
    CreateVpcAttachmentResponseTypeDef,
    DeleteAttachmentRequestRequestTypeDef,
    DeleteAttachmentResponseTypeDef,
    DeleteConnectionRequestRequestTypeDef,
    DeleteConnectionResponseTypeDef,
    DeleteConnectPeerRequestRequestTypeDef,
    DeleteConnectPeerResponseTypeDef,
    DeleteCoreNetworkPolicyVersionRequestRequestTypeDef,
    DeleteCoreNetworkPolicyVersionResponseTypeDef,
    DeleteCoreNetworkRequestRequestTypeDef,
    DeleteCoreNetworkResponseTypeDef,
    DeleteDeviceRequestRequestTypeDef,
    DeleteDeviceResponseTypeDef,
    DeleteGlobalNetworkRequestRequestTypeDef,
    DeleteGlobalNetworkResponseTypeDef,
    DeleteLinkRequestRequestTypeDef,
    DeleteLinkResponseTypeDef,
    DeletePeeringRequestRequestTypeDef,
    DeletePeeringResponseTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteSiteRequestRequestTypeDef,
    DeleteSiteResponseTypeDef,
    DeregisterTransitGatewayRequestRequestTypeDef,
    DeregisterTransitGatewayResponseTypeDef,
    DescribeGlobalNetworksRequestRequestTypeDef,
    DescribeGlobalNetworksResponseTypeDef,
    DisassociateConnectPeerRequestRequestTypeDef,
    DisassociateConnectPeerResponseTypeDef,
    DisassociateCustomerGatewayRequestRequestTypeDef,
    DisassociateCustomerGatewayResponseTypeDef,
    DisassociateLinkRequestRequestTypeDef,
    DisassociateLinkResponseTypeDef,
    DisassociateTransitGatewayConnectPeerRequestRequestTypeDef,
    DisassociateTransitGatewayConnectPeerResponseTypeDef,
    ExecuteCoreNetworkChangeSetRequestRequestTypeDef,
    GetConnectAttachmentRequestRequestTypeDef,
    GetConnectAttachmentResponseTypeDef,
    GetConnectionsRequestRequestTypeDef,
    GetConnectionsResponseTypeDef,
    GetConnectPeerAssociationsRequestRequestTypeDef,
    GetConnectPeerAssociationsResponseTypeDef,
    GetConnectPeerRequestRequestTypeDef,
    GetConnectPeerResponseTypeDef,
    GetCoreNetworkChangeEventsRequestRequestTypeDef,
    GetCoreNetworkChangeEventsResponseTypeDef,
    GetCoreNetworkChangeSetRequestRequestTypeDef,
    GetCoreNetworkChangeSetResponseTypeDef,
    GetCoreNetworkPolicyRequestRequestTypeDef,
    GetCoreNetworkPolicyResponseTypeDef,
    GetCoreNetworkRequestRequestTypeDef,
    GetCoreNetworkResponseTypeDef,
    GetCustomerGatewayAssociationsRequestRequestTypeDef,
    GetCustomerGatewayAssociationsResponseTypeDef,
    GetDevicesRequestRequestTypeDef,
    GetDevicesResponseTypeDef,
    GetLinkAssociationsRequestRequestTypeDef,
    GetLinkAssociationsResponseTypeDef,
    GetLinksRequestRequestTypeDef,
    GetLinksResponseTypeDef,
    GetNetworkResourceCountsRequestRequestTypeDef,
    GetNetworkResourceCountsResponseTypeDef,
    GetNetworkResourceRelationshipsRequestRequestTypeDef,
    GetNetworkResourceRelationshipsResponseTypeDef,
    GetNetworkResourcesRequestRequestTypeDef,
    GetNetworkResourcesResponseTypeDef,
    GetNetworkRoutesRequestRequestTypeDef,
    GetNetworkRoutesResponseTypeDef,
    GetNetworkTelemetryRequestRequestTypeDef,
    GetNetworkTelemetryResponseTypeDef,
    GetResourcePolicyRequestRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetRouteAnalysisRequestRequestTypeDef,
    GetRouteAnalysisResponseTypeDef,
    GetSitesRequestRequestTypeDef,
    GetSitesResponseTypeDef,
    GetSiteToSiteVpnAttachmentRequestRequestTypeDef,
    GetSiteToSiteVpnAttachmentResponseTypeDef,
    GetTransitGatewayConnectPeerAssociationsRequestRequestTypeDef,
    GetTransitGatewayConnectPeerAssociationsResponseTypeDef,
    GetTransitGatewayPeeringRequestRequestTypeDef,
    GetTransitGatewayPeeringResponseTypeDef,
    GetTransitGatewayRegistrationsRequestRequestTypeDef,
    GetTransitGatewayRegistrationsResponseTypeDef,
    GetTransitGatewayRouteTableAttachmentRequestRequestTypeDef,
    GetTransitGatewayRouteTableAttachmentResponseTypeDef,
    GetVpcAttachmentRequestRequestTypeDef,
    GetVpcAttachmentResponseTypeDef,
    ListAttachmentsRequestRequestTypeDef,
    ListAttachmentsResponseTypeDef,
    ListConnectPeersRequestRequestTypeDef,
    ListConnectPeersResponseTypeDef,
    ListCoreNetworkPolicyVersionsRequestRequestTypeDef,
    ListCoreNetworkPolicyVersionsResponseTypeDef,
    ListCoreNetworksRequestRequestTypeDef,
    ListCoreNetworksResponseTypeDef,
    ListOrganizationServiceAccessStatusRequestRequestTypeDef,
    ListOrganizationServiceAccessStatusResponseTypeDef,
    ListPeeringsRequestRequestTypeDef,
    ListPeeringsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutCoreNetworkPolicyRequestRequestTypeDef,
    PutCoreNetworkPolicyResponseTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    RegisterTransitGatewayRequestRequestTypeDef,
    RegisterTransitGatewayResponseTypeDef,
    RejectAttachmentRequestRequestTypeDef,
    RejectAttachmentResponseTypeDef,
    RestoreCoreNetworkPolicyVersionRequestRequestTypeDef,
    RestoreCoreNetworkPolicyVersionResponseTypeDef,
    StartOrganizationServiceAccessUpdateRequestRequestTypeDef,
    StartOrganizationServiceAccessUpdateResponseTypeDef,
    StartRouteAnalysisRequestRequestTypeDef,
    StartRouteAnalysisResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateConnectionRequestRequestTypeDef,
    UpdateConnectionResponseTypeDef,
    UpdateCoreNetworkRequestRequestTypeDef,
    UpdateCoreNetworkResponseTypeDef,
    UpdateDeviceRequestRequestTypeDef,
    UpdateDeviceResponseTypeDef,
    UpdateGlobalNetworkRequestRequestTypeDef,
    UpdateGlobalNetworkResponseTypeDef,
    UpdateLinkRequestRequestTypeDef,
    UpdateLinkResponseTypeDef,
    UpdateNetworkResourceMetadataRequestRequestTypeDef,
    UpdateNetworkResourceMetadataResponseTypeDef,
    UpdateSiteRequestRequestTypeDef,
    UpdateSiteResponseTypeDef,
    UpdateVpcAttachmentRequestRequestTypeDef,
    UpdateVpcAttachmentResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("NetworkManagerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CoreNetworkPolicyException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class NetworkManagerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NetworkManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#exceptions)
        """

    def accept_attachment(
        self, **kwargs: Unpack[AcceptAttachmentRequestRequestTypeDef]
    ) -> AcceptAttachmentResponseTypeDef:
        """
        Accepts a core network attachment request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.accept_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#accept_attachment)
        """

    def associate_connect_peer(
        self, **kwargs: Unpack[AssociateConnectPeerRequestRequestTypeDef]
    ) -> AssociateConnectPeerResponseTypeDef:
        """
        Associates a core network Connect peer with a device and optionally, with a
        link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.associate_connect_peer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#associate_connect_peer)
        """

    def associate_customer_gateway(
        self, **kwargs: Unpack[AssociateCustomerGatewayRequestRequestTypeDef]
    ) -> AssociateCustomerGatewayResponseTypeDef:
        """
        Associates a customer gateway with a device and optionally, with a link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.associate_customer_gateway)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#associate_customer_gateway)
        """

    def associate_link(
        self, **kwargs: Unpack[AssociateLinkRequestRequestTypeDef]
    ) -> AssociateLinkResponseTypeDef:
        """
        Associates a link to a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.associate_link)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#associate_link)
        """

    def associate_transit_gateway_connect_peer(
        self, **kwargs: Unpack[AssociateTransitGatewayConnectPeerRequestRequestTypeDef]
    ) -> AssociateTransitGatewayConnectPeerResponseTypeDef:
        """
        Associates a transit gateway Connect peer with a device, and optionally, with a
        link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.associate_transit_gateway_connect_peer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#associate_transit_gateway_connect_peer)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#close)
        """

    def create_connect_attachment(
        self, **kwargs: Unpack[CreateConnectAttachmentRequestRequestTypeDef]
    ) -> CreateConnectAttachmentResponseTypeDef:
        """
        Creates a core network Connect attachment from a specified core network
        attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_connect_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_connect_attachment)
        """

    def create_connect_peer(
        self, **kwargs: Unpack[CreateConnectPeerRequestRequestTypeDef]
    ) -> CreateConnectPeerResponseTypeDef:
        """
        Creates a core network Connect peer for a specified core network connect
        attachment between a core network and an
        appliance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_connect_peer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_connect_peer)
        """

    def create_connection(
        self, **kwargs: Unpack[CreateConnectionRequestRequestTypeDef]
    ) -> CreateConnectionResponseTypeDef:
        """
        Creates a connection between two devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_connection)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_connection)
        """

    def create_core_network(
        self, **kwargs: Unpack[CreateCoreNetworkRequestRequestTypeDef]
    ) -> CreateCoreNetworkResponseTypeDef:
        """
        Creates a core network as part of your global network, and optionally, with a
        core network
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_core_network)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_core_network)
        """

    def create_device(
        self, **kwargs: Unpack[CreateDeviceRequestRequestTypeDef]
    ) -> CreateDeviceResponseTypeDef:
        """
        Creates a new device in a global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_device)
        """

    def create_global_network(
        self, **kwargs: Unpack[CreateGlobalNetworkRequestRequestTypeDef]
    ) -> CreateGlobalNetworkResponseTypeDef:
        """
        Creates a new, empty global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_global_network)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_global_network)
        """

    def create_link(
        self, **kwargs: Unpack[CreateLinkRequestRequestTypeDef]
    ) -> CreateLinkResponseTypeDef:
        """
        Creates a new link for a specified site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_link)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_link)
        """

    def create_site(
        self, **kwargs: Unpack[CreateSiteRequestRequestTypeDef]
    ) -> CreateSiteResponseTypeDef:
        """
        Creates a new site in a global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_site)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_site)
        """

    def create_site_to_site_vpn_attachment(
        self, **kwargs: Unpack[CreateSiteToSiteVpnAttachmentRequestRequestTypeDef]
    ) -> CreateSiteToSiteVpnAttachmentResponseTypeDef:
        """
        Creates an Amazon Web Services site-to-site VPN attachment on an edge location
        of a core
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_site_to_site_vpn_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_site_to_site_vpn_attachment)
        """

    def create_transit_gateway_peering(
        self, **kwargs: Unpack[CreateTransitGatewayPeeringRequestRequestTypeDef]
    ) -> CreateTransitGatewayPeeringResponseTypeDef:
        """
        Creates a transit gateway peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_transit_gateway_peering)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_transit_gateway_peering)
        """

    def create_transit_gateway_route_table_attachment(
        self, **kwargs: Unpack[CreateTransitGatewayRouteTableAttachmentRequestRequestTypeDef]
    ) -> CreateTransitGatewayRouteTableAttachmentResponseTypeDef:
        """
        Creates a transit gateway route table attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_transit_gateway_route_table_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_transit_gateway_route_table_attachment)
        """

    def create_vpc_attachment(
        self, **kwargs: Unpack[CreateVpcAttachmentRequestRequestTypeDef]
    ) -> CreateVpcAttachmentResponseTypeDef:
        """
        Creates a VPC attachment on an edge location of a core network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.create_vpc_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#create_vpc_attachment)
        """

    def delete_attachment(
        self, **kwargs: Unpack[DeleteAttachmentRequestRequestTypeDef]
    ) -> DeleteAttachmentResponseTypeDef:
        """
        Deletes an attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_attachment)
        """

    def delete_connect_peer(
        self, **kwargs: Unpack[DeleteConnectPeerRequestRequestTypeDef]
    ) -> DeleteConnectPeerResponseTypeDef:
        """
        Deletes a Connect peer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_connect_peer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_connect_peer)
        """

    def delete_connection(
        self, **kwargs: Unpack[DeleteConnectionRequestRequestTypeDef]
    ) -> DeleteConnectionResponseTypeDef:
        """
        Deletes the specified connection in your global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_connection)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_connection)
        """

    def delete_core_network(
        self, **kwargs: Unpack[DeleteCoreNetworkRequestRequestTypeDef]
    ) -> DeleteCoreNetworkResponseTypeDef:
        """
        Deletes a core network along with all core network policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_core_network)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_core_network)
        """

    def delete_core_network_policy_version(
        self, **kwargs: Unpack[DeleteCoreNetworkPolicyVersionRequestRequestTypeDef]
    ) -> DeleteCoreNetworkPolicyVersionResponseTypeDef:
        """
        Deletes a policy version from a core network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_core_network_policy_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_core_network_policy_version)
        """

    def delete_device(
        self, **kwargs: Unpack[DeleteDeviceRequestRequestTypeDef]
    ) -> DeleteDeviceResponseTypeDef:
        """
        Deletes an existing device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_device)
        """

    def delete_global_network(
        self, **kwargs: Unpack[DeleteGlobalNetworkRequestRequestTypeDef]
    ) -> DeleteGlobalNetworkResponseTypeDef:
        """
        Deletes an existing global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_global_network)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_global_network)
        """

    def delete_link(
        self, **kwargs: Unpack[DeleteLinkRequestRequestTypeDef]
    ) -> DeleteLinkResponseTypeDef:
        """
        Deletes an existing link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_link)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_link)
        """

    def delete_peering(
        self, **kwargs: Unpack[DeletePeeringRequestRequestTypeDef]
    ) -> DeletePeeringResponseTypeDef:
        """
        Deletes an existing peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_peering)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_peering)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a resource policy for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_resource_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_resource_policy)
        """

    def delete_site(
        self, **kwargs: Unpack[DeleteSiteRequestRequestTypeDef]
    ) -> DeleteSiteResponseTypeDef:
        """
        Deletes an existing site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.delete_site)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#delete_site)
        """

    def deregister_transit_gateway(
        self, **kwargs: Unpack[DeregisterTransitGatewayRequestRequestTypeDef]
    ) -> DeregisterTransitGatewayResponseTypeDef:
        """
        Deregisters a transit gateway from your global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.deregister_transit_gateway)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#deregister_transit_gateway)
        """

    def describe_global_networks(
        self, **kwargs: Unpack[DescribeGlobalNetworksRequestRequestTypeDef]
    ) -> DescribeGlobalNetworksResponseTypeDef:
        """
        Describes one or more global networks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.describe_global_networks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#describe_global_networks)
        """

    def disassociate_connect_peer(
        self, **kwargs: Unpack[DisassociateConnectPeerRequestRequestTypeDef]
    ) -> DisassociateConnectPeerResponseTypeDef:
        """
        Disassociates a core network Connect peer from a device and a link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.disassociate_connect_peer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#disassociate_connect_peer)
        """

    def disassociate_customer_gateway(
        self, **kwargs: Unpack[DisassociateCustomerGatewayRequestRequestTypeDef]
    ) -> DisassociateCustomerGatewayResponseTypeDef:
        """
        Disassociates a customer gateway from a device and a link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.disassociate_customer_gateway)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#disassociate_customer_gateway)
        """

    def disassociate_link(
        self, **kwargs: Unpack[DisassociateLinkRequestRequestTypeDef]
    ) -> DisassociateLinkResponseTypeDef:
        """
        Disassociates an existing device from a link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.disassociate_link)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#disassociate_link)
        """

    def disassociate_transit_gateway_connect_peer(
        self, **kwargs: Unpack[DisassociateTransitGatewayConnectPeerRequestRequestTypeDef]
    ) -> DisassociateTransitGatewayConnectPeerResponseTypeDef:
        """
        Disassociates a transit gateway Connect peer from a device and link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.disassociate_transit_gateway_connect_peer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#disassociate_transit_gateway_connect_peer)
        """

    def execute_core_network_change_set(
        self, **kwargs: Unpack[ExecuteCoreNetworkChangeSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Executes a change set on your core network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.execute_core_network_change_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#execute_core_network_change_set)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#generate_presigned_url)
        """

    def get_connect_attachment(
        self, **kwargs: Unpack[GetConnectAttachmentRequestRequestTypeDef]
    ) -> GetConnectAttachmentResponseTypeDef:
        """
        Returns information about a core network Connect attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_connect_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_connect_attachment)
        """

    def get_connect_peer(
        self, **kwargs: Unpack[GetConnectPeerRequestRequestTypeDef]
    ) -> GetConnectPeerResponseTypeDef:
        """
        Returns information about a core network Connect peer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_connect_peer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_connect_peer)
        """

    def get_connect_peer_associations(
        self, **kwargs: Unpack[GetConnectPeerAssociationsRequestRequestTypeDef]
    ) -> GetConnectPeerAssociationsResponseTypeDef:
        """
        Returns information about a core network Connect peer associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_connect_peer_associations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_connect_peer_associations)
        """

    def get_connections(
        self, **kwargs: Unpack[GetConnectionsRequestRequestTypeDef]
    ) -> GetConnectionsResponseTypeDef:
        """
        Gets information about one or more of your connections in a global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_connections)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_connections)
        """

    def get_core_network(
        self, **kwargs: Unpack[GetCoreNetworkRequestRequestTypeDef]
    ) -> GetCoreNetworkResponseTypeDef:
        """
        Returns information about the LIVE policy for a core network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_core_network)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_core_network)
        """

    def get_core_network_change_events(
        self, **kwargs: Unpack[GetCoreNetworkChangeEventsRequestRequestTypeDef]
    ) -> GetCoreNetworkChangeEventsResponseTypeDef:
        """
        Returns information about a core network change event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_core_network_change_events)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_core_network_change_events)
        """

    def get_core_network_change_set(
        self, **kwargs: Unpack[GetCoreNetworkChangeSetRequestRequestTypeDef]
    ) -> GetCoreNetworkChangeSetResponseTypeDef:
        """
        Returns a change set between the LIVE core network policy and a submitted
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_core_network_change_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_core_network_change_set)
        """

    def get_core_network_policy(
        self, **kwargs: Unpack[GetCoreNetworkPolicyRequestRequestTypeDef]
    ) -> GetCoreNetworkPolicyResponseTypeDef:
        """
        Returns details about a core network policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_core_network_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_core_network_policy)
        """

    def get_customer_gateway_associations(
        self, **kwargs: Unpack[GetCustomerGatewayAssociationsRequestRequestTypeDef]
    ) -> GetCustomerGatewayAssociationsResponseTypeDef:
        """
        Gets the association information for customer gateways that are associated with
        devices and links in your global
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_customer_gateway_associations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_customer_gateway_associations)
        """

    def get_devices(
        self, **kwargs: Unpack[GetDevicesRequestRequestTypeDef]
    ) -> GetDevicesResponseTypeDef:
        """
        Gets information about one or more of your devices in a global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_devices)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_devices)
        """

    def get_link_associations(
        self, **kwargs: Unpack[GetLinkAssociationsRequestRequestTypeDef]
    ) -> GetLinkAssociationsResponseTypeDef:
        """
        Gets the link associations for a device or a link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_link_associations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_link_associations)
        """

    def get_links(self, **kwargs: Unpack[GetLinksRequestRequestTypeDef]) -> GetLinksResponseTypeDef:
        """
        Gets information about one or more links in a specified global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_links)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_links)
        """

    def get_network_resource_counts(
        self, **kwargs: Unpack[GetNetworkResourceCountsRequestRequestTypeDef]
    ) -> GetNetworkResourceCountsResponseTypeDef:
        """
        Gets the count of network resources, by resource type, for the specified global
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_network_resource_counts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_network_resource_counts)
        """

    def get_network_resource_relationships(
        self, **kwargs: Unpack[GetNetworkResourceRelationshipsRequestRequestTypeDef]
    ) -> GetNetworkResourceRelationshipsResponseTypeDef:
        """
        Gets the network resource relationships for the specified global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_network_resource_relationships)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_network_resource_relationships)
        """

    def get_network_resources(
        self, **kwargs: Unpack[GetNetworkResourcesRequestRequestTypeDef]
    ) -> GetNetworkResourcesResponseTypeDef:
        """
        Describes the network resources for the specified global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_network_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_network_resources)
        """

    def get_network_routes(
        self, **kwargs: Unpack[GetNetworkRoutesRequestRequestTypeDef]
    ) -> GetNetworkRoutesResponseTypeDef:
        """
        Gets the network routes of the specified global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_network_routes)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_network_routes)
        """

    def get_network_telemetry(
        self, **kwargs: Unpack[GetNetworkTelemetryRequestRequestTypeDef]
    ) -> GetNetworkTelemetryResponseTypeDef:
        """
        Gets the network telemetry of the specified global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_network_telemetry)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_network_telemetry)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Returns information about a resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_resource_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_resource_policy)
        """

    def get_route_analysis(
        self, **kwargs: Unpack[GetRouteAnalysisRequestRequestTypeDef]
    ) -> GetRouteAnalysisResponseTypeDef:
        """
        Gets information about the specified route analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_route_analysis)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_route_analysis)
        """

    def get_site_to_site_vpn_attachment(
        self, **kwargs: Unpack[GetSiteToSiteVpnAttachmentRequestRequestTypeDef]
    ) -> GetSiteToSiteVpnAttachmentResponseTypeDef:
        """
        Returns information about a site-to-site VPN attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_site_to_site_vpn_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_site_to_site_vpn_attachment)
        """

    def get_sites(self, **kwargs: Unpack[GetSitesRequestRequestTypeDef]) -> GetSitesResponseTypeDef:
        """
        Gets information about one or more of your sites in a global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_sites)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_sites)
        """

    def get_transit_gateway_connect_peer_associations(
        self, **kwargs: Unpack[GetTransitGatewayConnectPeerAssociationsRequestRequestTypeDef]
    ) -> GetTransitGatewayConnectPeerAssociationsResponseTypeDef:
        """
        Gets information about one or more of your transit gateway Connect peer
        associations in a global
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_transit_gateway_connect_peer_associations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_transit_gateway_connect_peer_associations)
        """

    def get_transit_gateway_peering(
        self, **kwargs: Unpack[GetTransitGatewayPeeringRequestRequestTypeDef]
    ) -> GetTransitGatewayPeeringResponseTypeDef:
        """
        Returns information about a transit gateway peer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_transit_gateway_peering)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_transit_gateway_peering)
        """

    def get_transit_gateway_registrations(
        self, **kwargs: Unpack[GetTransitGatewayRegistrationsRequestRequestTypeDef]
    ) -> GetTransitGatewayRegistrationsResponseTypeDef:
        """
        Gets information about the transit gateway registrations in a specified global
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_transit_gateway_registrations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_transit_gateway_registrations)
        """

    def get_transit_gateway_route_table_attachment(
        self, **kwargs: Unpack[GetTransitGatewayRouteTableAttachmentRequestRequestTypeDef]
    ) -> GetTransitGatewayRouteTableAttachmentResponseTypeDef:
        """
        Returns information about a transit gateway route table attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_transit_gateway_route_table_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_transit_gateway_route_table_attachment)
        """

    def get_vpc_attachment(
        self, **kwargs: Unpack[GetVpcAttachmentRequestRequestTypeDef]
    ) -> GetVpcAttachmentResponseTypeDef:
        """
        Returns information about a VPC attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_vpc_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_vpc_attachment)
        """

    def list_attachments(
        self, **kwargs: Unpack[ListAttachmentsRequestRequestTypeDef]
    ) -> ListAttachmentsResponseTypeDef:
        """
        Returns a list of core network attachments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.list_attachments)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#list_attachments)
        """

    def list_connect_peers(
        self, **kwargs: Unpack[ListConnectPeersRequestRequestTypeDef]
    ) -> ListConnectPeersResponseTypeDef:
        """
        Returns a list of core network Connect peers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.list_connect_peers)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#list_connect_peers)
        """

    def list_core_network_policy_versions(
        self, **kwargs: Unpack[ListCoreNetworkPolicyVersionsRequestRequestTypeDef]
    ) -> ListCoreNetworkPolicyVersionsResponseTypeDef:
        """
        Returns a list of core network policy versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.list_core_network_policy_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#list_core_network_policy_versions)
        """

    def list_core_networks(
        self, **kwargs: Unpack[ListCoreNetworksRequestRequestTypeDef]
    ) -> ListCoreNetworksResponseTypeDef:
        """
        Returns a list of owned and shared core networks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.list_core_networks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#list_core_networks)
        """

    def list_organization_service_access_status(
        self, **kwargs: Unpack[ListOrganizationServiceAccessStatusRequestRequestTypeDef]
    ) -> ListOrganizationServiceAccessStatusResponseTypeDef:
        """
        Gets the status of the Service Linked Role (SLR) deployment for the accounts in
        a given Amazon Web Services
        Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.list_organization_service_access_status)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#list_organization_service_access_status)
        """

    def list_peerings(
        self, **kwargs: Unpack[ListPeeringsRequestRequestTypeDef]
    ) -> ListPeeringsResponseTypeDef:
        """
        Lists the peerings for a core network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.list_peerings)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#list_peerings)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#list_tags_for_resource)
        """

    def put_core_network_policy(
        self, **kwargs: Unpack[PutCoreNetworkPolicyRequestRequestTypeDef]
    ) -> PutCoreNetworkPolicyResponseTypeDef:
        """
        Creates a new, immutable version of a core network policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.put_core_network_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#put_core_network_policy)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates a resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.put_resource_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#put_resource_policy)
        """

    def register_transit_gateway(
        self, **kwargs: Unpack[RegisterTransitGatewayRequestRequestTypeDef]
    ) -> RegisterTransitGatewayResponseTypeDef:
        """
        Registers a transit gateway in your global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.register_transit_gateway)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#register_transit_gateway)
        """

    def reject_attachment(
        self, **kwargs: Unpack[RejectAttachmentRequestRequestTypeDef]
    ) -> RejectAttachmentResponseTypeDef:
        """
        Rejects a core network attachment request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.reject_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#reject_attachment)
        """

    def restore_core_network_policy_version(
        self, **kwargs: Unpack[RestoreCoreNetworkPolicyVersionRequestRequestTypeDef]
    ) -> RestoreCoreNetworkPolicyVersionResponseTypeDef:
        """
        Restores a previous policy version as a new, immutable version of a core
        network
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.restore_core_network_policy_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#restore_core_network_policy_version)
        """

    def start_organization_service_access_update(
        self, **kwargs: Unpack[StartOrganizationServiceAccessUpdateRequestRequestTypeDef]
    ) -> StartOrganizationServiceAccessUpdateResponseTypeDef:
        """
        Enables the Network Manager service for an Amazon Web Services Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.start_organization_service_access_update)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#start_organization_service_access_update)
        """

    def start_route_analysis(
        self, **kwargs: Unpack[StartRouteAnalysisRequestRequestTypeDef]
    ) -> StartRouteAnalysisResponseTypeDef:
        """
        Starts analyzing the routing path between the specified source and destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.start_route_analysis)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#start_route_analysis)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#untag_resource)
        """

    def update_connection(
        self, **kwargs: Unpack[UpdateConnectionRequestRequestTypeDef]
    ) -> UpdateConnectionResponseTypeDef:
        """
        Updates the information for an existing connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.update_connection)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#update_connection)
        """

    def update_core_network(
        self, **kwargs: Unpack[UpdateCoreNetworkRequestRequestTypeDef]
    ) -> UpdateCoreNetworkResponseTypeDef:
        """
        Updates the description of a core network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.update_core_network)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#update_core_network)
        """

    def update_device(
        self, **kwargs: Unpack[UpdateDeviceRequestRequestTypeDef]
    ) -> UpdateDeviceResponseTypeDef:
        """
        Updates the details for an existing device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.update_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#update_device)
        """

    def update_global_network(
        self, **kwargs: Unpack[UpdateGlobalNetworkRequestRequestTypeDef]
    ) -> UpdateGlobalNetworkResponseTypeDef:
        """
        Updates an existing global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.update_global_network)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#update_global_network)
        """

    def update_link(
        self, **kwargs: Unpack[UpdateLinkRequestRequestTypeDef]
    ) -> UpdateLinkResponseTypeDef:
        """
        Updates the details for an existing link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.update_link)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#update_link)
        """

    def update_network_resource_metadata(
        self, **kwargs: Unpack[UpdateNetworkResourceMetadataRequestRequestTypeDef]
    ) -> UpdateNetworkResourceMetadataResponseTypeDef:
        """
        Updates the resource metadata for the specified global network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.update_network_resource_metadata)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#update_network_resource_metadata)
        """

    def update_site(
        self, **kwargs: Unpack[UpdateSiteRequestRequestTypeDef]
    ) -> UpdateSiteResponseTypeDef:
        """
        Updates the information for an existing site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.update_site)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#update_site)
        """

    def update_vpc_attachment(
        self, **kwargs: Unpack[UpdateVpcAttachmentRequestRequestTypeDef]
    ) -> UpdateVpcAttachmentResponseTypeDef:
        """
        Updates a VPC attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.update_vpc_attachment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#update_vpc_attachment)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_global_networks"]
    ) -> DescribeGlobalNetworksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_connect_peer_associations"]
    ) -> GetConnectPeerAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_connections"]) -> GetConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_core_network_change_events"]
    ) -> GetCoreNetworkChangeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_core_network_change_set"]
    ) -> GetCoreNetworkChangeSetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_customer_gateway_associations"]
    ) -> GetCustomerGatewayAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_devices"]) -> GetDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_link_associations"]
    ) -> GetLinkAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_links"]) -> GetLinksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_network_resource_counts"]
    ) -> GetNetworkResourceCountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_network_resource_relationships"]
    ) -> GetNetworkResourceRelationshipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_network_resources"]
    ) -> GetNetworkResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_network_telemetry"]
    ) -> GetNetworkTelemetryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_sites"]) -> GetSitesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_transit_gateway_connect_peer_associations"]
    ) -> GetTransitGatewayConnectPeerAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_transit_gateway_registrations"]
    ) -> GetTransitGatewayRegistrationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attachments"]
    ) -> ListAttachmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_connect_peers"]
    ) -> ListConnectPeersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_core_network_policy_versions"]
    ) -> ListCoreNetworkPolicyVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_core_networks"]
    ) -> ListCoreNetworksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_peerings"]) -> ListPeeringsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/client/#get_paginator)
        """
