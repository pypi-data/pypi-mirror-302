"""
Type annotations for outposts service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_outposts.client import OutpostsClient

    session = Session()
    client: OutpostsClient = session.client("outposts")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetOutpostInstanceTypesPaginator,
    GetOutpostSupportedInstanceTypesPaginator,
    ListAssetsPaginator,
    ListCapacityTasksPaginator,
    ListCatalogItemsPaginator,
    ListOrdersPaginator,
    ListOutpostsPaginator,
    ListSitesPaginator,
)
from .type_defs import (
    CancelCapacityTaskInputRequestTypeDef,
    CancelOrderInputRequestTypeDef,
    CreateOrderInputRequestTypeDef,
    CreateOrderOutputTypeDef,
    CreateOutpostInputRequestTypeDef,
    CreateOutpostOutputTypeDef,
    CreateSiteInputRequestTypeDef,
    CreateSiteOutputTypeDef,
    DeleteOutpostInputRequestTypeDef,
    DeleteSiteInputRequestTypeDef,
    GetCapacityTaskInputRequestTypeDef,
    GetCapacityTaskOutputTypeDef,
    GetCatalogItemInputRequestTypeDef,
    GetCatalogItemOutputTypeDef,
    GetConnectionRequestRequestTypeDef,
    GetConnectionResponseTypeDef,
    GetOrderInputRequestTypeDef,
    GetOrderOutputTypeDef,
    GetOutpostInputRequestTypeDef,
    GetOutpostInstanceTypesInputRequestTypeDef,
    GetOutpostInstanceTypesOutputTypeDef,
    GetOutpostOutputTypeDef,
    GetOutpostSupportedInstanceTypesInputRequestTypeDef,
    GetOutpostSupportedInstanceTypesOutputTypeDef,
    GetSiteAddressInputRequestTypeDef,
    GetSiteAddressOutputTypeDef,
    GetSiteInputRequestTypeDef,
    GetSiteOutputTypeDef,
    ListAssetsInputRequestTypeDef,
    ListAssetsOutputTypeDef,
    ListCapacityTasksInputRequestTypeDef,
    ListCapacityTasksOutputTypeDef,
    ListCatalogItemsInputRequestTypeDef,
    ListCatalogItemsOutputTypeDef,
    ListOrdersInputRequestTypeDef,
    ListOrdersOutputTypeDef,
    ListOutpostsInputRequestTypeDef,
    ListOutpostsOutputTypeDef,
    ListSitesInputRequestTypeDef,
    ListSitesOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartCapacityTaskInputRequestTypeDef,
    StartCapacityTaskOutputTypeDef,
    StartConnectionRequestRequestTypeDef,
    StartConnectionResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateOutpostInputRequestTypeDef,
    UpdateOutpostOutputTypeDef,
    UpdateSiteAddressInputRequestTypeDef,
    UpdateSiteAddressOutputTypeDef,
    UpdateSiteInputRequestTypeDef,
    UpdateSiteOutputTypeDef,
    UpdateSiteRackPhysicalPropertiesInputRequestTypeDef,
    UpdateSiteRackPhysicalPropertiesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("OutpostsClient",)

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
    NotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class OutpostsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OutpostsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#can_paginate)
        """

    def cancel_capacity_task(
        self, **kwargs: Unpack[CancelCapacityTaskInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the capacity task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.cancel_capacity_task)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#cancel_capacity_task)
        """

    def cancel_order(self, **kwargs: Unpack[CancelOrderInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Cancels the specified order for an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.cancel_order)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#cancel_order)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#close)
        """

    def create_order(
        self, **kwargs: Unpack[CreateOrderInputRequestTypeDef]
    ) -> CreateOrderOutputTypeDef:
        """
        Creates an order for an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.create_order)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#create_order)
        """

    def create_outpost(
        self, **kwargs: Unpack[CreateOutpostInputRequestTypeDef]
    ) -> CreateOutpostOutputTypeDef:
        """
        Creates an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.create_outpost)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#create_outpost)
        """

    def create_site(
        self, **kwargs: Unpack[CreateSiteInputRequestTypeDef]
    ) -> CreateSiteOutputTypeDef:
        """
        Creates a site for an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.create_site)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#create_site)
        """

    def delete_outpost(self, **kwargs: Unpack[DeleteOutpostInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.delete_outpost)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#delete_outpost)
        """

    def delete_site(self, **kwargs: Unpack[DeleteSiteInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.delete_site)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#delete_site)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#generate_presigned_url)
        """

    def get_capacity_task(
        self, **kwargs: Unpack[GetCapacityTaskInputRequestTypeDef]
    ) -> GetCapacityTaskOutputTypeDef:
        """
        Gets details of the specified capacity task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_capacity_task)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_capacity_task)
        """

    def get_catalog_item(
        self, **kwargs: Unpack[GetCatalogItemInputRequestTypeDef]
    ) -> GetCatalogItemOutputTypeDef:
        """
        Gets information about the specified catalog item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_catalog_item)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_catalog_item)
        """

    def get_connection(
        self, **kwargs: Unpack[GetConnectionRequestRequestTypeDef]
    ) -> GetConnectionResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_connection)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_connection)
        """

    def get_order(self, **kwargs: Unpack[GetOrderInputRequestTypeDef]) -> GetOrderOutputTypeDef:
        """
        Gets information about the specified order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_order)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_order)
        """

    def get_outpost(
        self, **kwargs: Unpack[GetOutpostInputRequestTypeDef]
    ) -> GetOutpostOutputTypeDef:
        """
        Gets information about the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_outpost)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_outpost)
        """

    def get_outpost_instance_types(
        self, **kwargs: Unpack[GetOutpostInstanceTypesInputRequestTypeDef]
    ) -> GetOutpostInstanceTypesOutputTypeDef:
        """
        Gets the instance types for the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_outpost_instance_types)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_outpost_instance_types)
        """

    def get_outpost_supported_instance_types(
        self, **kwargs: Unpack[GetOutpostSupportedInstanceTypesInputRequestTypeDef]
    ) -> GetOutpostSupportedInstanceTypesOutputTypeDef:
        """
        Gets the instance types that an Outpost can support in `InstanceTypeCapacity`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_outpost_supported_instance_types)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_outpost_supported_instance_types)
        """

    def get_site(self, **kwargs: Unpack[GetSiteInputRequestTypeDef]) -> GetSiteOutputTypeDef:
        """
        Gets information about the specified Outpost site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_site)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_site)
        """

    def get_site_address(
        self, **kwargs: Unpack[GetSiteAddressInputRequestTypeDef]
    ) -> GetSiteAddressOutputTypeDef:
        """
        Gets the site address of the specified site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_site_address)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_site_address)
        """

    def list_assets(
        self, **kwargs: Unpack[ListAssetsInputRequestTypeDef]
    ) -> ListAssetsOutputTypeDef:
        """
        Lists the hardware assets for the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_assets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_assets)
        """

    def list_capacity_tasks(
        self, **kwargs: Unpack[ListCapacityTasksInputRequestTypeDef]
    ) -> ListCapacityTasksOutputTypeDef:
        """
        Lists the capacity tasks for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_capacity_tasks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_capacity_tasks)
        """

    def list_catalog_items(
        self, **kwargs: Unpack[ListCatalogItemsInputRequestTypeDef]
    ) -> ListCatalogItemsOutputTypeDef:
        """
        Lists the items in the catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_catalog_items)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_catalog_items)
        """

    def list_orders(
        self, **kwargs: Unpack[ListOrdersInputRequestTypeDef]
    ) -> ListOrdersOutputTypeDef:
        """
        Lists the Outpost orders for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_orders)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_orders)
        """

    def list_outposts(
        self, **kwargs: Unpack[ListOutpostsInputRequestTypeDef]
    ) -> ListOutpostsOutputTypeDef:
        """
        Lists the Outposts for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_outposts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_outposts)
        """

    def list_sites(self, **kwargs: Unpack[ListSitesInputRequestTypeDef]) -> ListSitesOutputTypeDef:
        """
        Lists the Outpost sites for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_sites)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_sites)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_tags_for_resource)
        """

    def start_capacity_task(
        self, **kwargs: Unpack[StartCapacityTaskInputRequestTypeDef]
    ) -> StartCapacityTaskOutputTypeDef:
        """
        Starts the specified capacity task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.start_capacity_task)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#start_capacity_task)
        """

    def start_connection(
        self, **kwargs: Unpack[StartConnectionRequestRequestTypeDef]
    ) -> StartConnectionResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.start_connection)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#start_connection)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#untag_resource)
        """

    def update_outpost(
        self, **kwargs: Unpack[UpdateOutpostInputRequestTypeDef]
    ) -> UpdateOutpostOutputTypeDef:
        """
        Updates an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_outpost)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#update_outpost)
        """

    def update_site(
        self, **kwargs: Unpack[UpdateSiteInputRequestTypeDef]
    ) -> UpdateSiteOutputTypeDef:
        """
        Updates the specified site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_site)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#update_site)
        """

    def update_site_address(
        self, **kwargs: Unpack[UpdateSiteAddressInputRequestTypeDef]
    ) -> UpdateSiteAddressOutputTypeDef:
        """
        Updates the address of the specified site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_site_address)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#update_site_address)
        """

    def update_site_rack_physical_properties(
        self, **kwargs: Unpack[UpdateSiteRackPhysicalPropertiesInputRequestTypeDef]
    ) -> UpdateSiteRackPhysicalPropertiesOutputTypeDef:
        """
        Update the physical and logistical details for a rack at a site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_site_rack_physical_properties)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#update_site_rack_physical_properties)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_outpost_instance_types"]
    ) -> GetOutpostInstanceTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_outpost_supported_instance_types"]
    ) -> GetOutpostSupportedInstanceTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_assets"]) -> ListAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_capacity_tasks"]
    ) -> ListCapacityTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_catalog_items"]
    ) -> ListCatalogItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_orders"]) -> ListOrdersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_outposts"]) -> ListOutpostsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_sites"]) -> ListSitesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """
