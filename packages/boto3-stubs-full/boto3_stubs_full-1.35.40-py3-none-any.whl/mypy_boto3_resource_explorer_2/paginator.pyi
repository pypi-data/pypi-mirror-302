"""
Type annotations for resource-explorer-2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_resource_explorer_2.client import ResourceExplorerClient
    from mypy_boto3_resource_explorer_2.paginator import (
        ListIndexesPaginator,
        ListIndexesForMembersPaginator,
        ListResourcesPaginator,
        ListSupportedResourceTypesPaginator,
        ListViewsPaginator,
        SearchPaginator,
    )

    session = Session()
    client: ResourceExplorerClient = session.client("resource-explorer-2")

    list_indexes_paginator: ListIndexesPaginator = client.get_paginator("list_indexes")
    list_indexes_for_members_paginator: ListIndexesForMembersPaginator = client.get_paginator("list_indexes_for_members")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    list_supported_resource_types_paginator: ListSupportedResourceTypesPaginator = client.get_paginator("list_supported_resource_types")
    list_views_paginator: ListViewsPaginator = client.get_paginator("list_views")
    search_paginator: SearchPaginator = client.get_paginator("search")
    ```
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListIndexesForMembersInputListIndexesForMembersPaginateTypeDef,
    ListIndexesForMembersOutputTypeDef,
    ListIndexesInputListIndexesPaginateTypeDef,
    ListIndexesOutputTypeDef,
    ListResourcesInputListResourcesPaginateTypeDef,
    ListResourcesOutputTypeDef,
    ListSupportedResourceTypesInputListSupportedResourceTypesPaginateTypeDef,
    ListSupportedResourceTypesOutputTypeDef,
    ListViewsInputListViewsPaginateTypeDef,
    ListViewsOutputTypeDef,
    SearchInputSearchPaginateTypeDef,
    SearchOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListIndexesPaginator",
    "ListIndexesForMembersPaginator",
    "ListResourcesPaginator",
    "ListSupportedResourceTypesPaginator",
    "ListViewsPaginator",
    "SearchPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListIndexesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListIndexes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listindexespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIndexesInputListIndexesPaginateTypeDef]
    ) -> _PageIterator[ListIndexesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListIndexes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listindexespaginator)
        """

class ListIndexesForMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListIndexesForMembers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listindexesformemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIndexesForMembersInputListIndexesForMembersPaginateTypeDef]
    ) -> _PageIterator[ListIndexesForMembersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListIndexesForMembers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listindexesformemberspaginator)
        """

class ListResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourcesInputListResourcesPaginateTypeDef]
    ) -> _PageIterator[ListResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listresourcespaginator)
        """

class ListSupportedResourceTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListSupportedResourceTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listsupportedresourcetypespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSupportedResourceTypesInputListSupportedResourceTypesPaginateTypeDef],
    ) -> _PageIterator[ListSupportedResourceTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListSupportedResourceTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listsupportedresourcetypespaginator)
        """

class ListViewsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListViews)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listviewspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListViewsInputListViewsPaginateTypeDef]
    ) -> _PageIterator[ListViewsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListViews.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#listviewspaginator)
        """

class SearchPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.Search)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#searchpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchInputSearchPaginateTypeDef]
    ) -> _PageIterator[SearchOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.Search.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/paginators/#searchpaginator)
        """
