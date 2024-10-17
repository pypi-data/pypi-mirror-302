"""
Type annotations for dataexchange service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_dataexchange.client import DataExchangeClient
    from mypy_boto3_dataexchange.paginator import (
        ListDataSetRevisionsPaginator,
        ListDataSetsPaginator,
        ListEventActionsPaginator,
        ListJobsPaginator,
        ListRevisionAssetsPaginator,
    )

    session = Session()
    client: DataExchangeClient = session.client("dataexchange")

    list_data_set_revisions_paginator: ListDataSetRevisionsPaginator = client.get_paginator("list_data_set_revisions")
    list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
    list_event_actions_paginator: ListEventActionsPaginator = client.get_paginator("list_event_actions")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_revision_assets_paginator: ListRevisionAssetsPaginator = client.get_paginator("list_revision_assets")
    ```
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef,
    ListDataSetRevisionsResponseTypeDef,
    ListDataSetsRequestListDataSetsPaginateTypeDef,
    ListDataSetsResponseTypeDef,
    ListEventActionsRequestListEventActionsPaginateTypeDef,
    ListEventActionsResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef,
    ListRevisionAssetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDataSetRevisionsPaginator",
    "ListDataSetsPaginator",
    "ListEventActionsPaginator",
    "ListJobsPaginator",
    "ListRevisionAssetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDataSetRevisionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSetRevisions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listdatasetrevisionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef]
    ) -> _PageIterator[ListDataSetRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSetRevisions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listdatasetrevisionspaginator)
        """


class ListDataSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listdatasetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSetsRequestListDataSetsPaginateTypeDef]
    ) -> _PageIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listdatasetspaginator)
        """


class ListEventActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListEventActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listeventactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEventActionsRequestListEventActionsPaginateTypeDef]
    ) -> _PageIterator[ListEventActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListEventActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listeventactionspaginator)
        """


class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listjobspaginator)
        """


class ListRevisionAssetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListRevisionAssets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listrevisionassetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef]
    ) -> _PageIterator[ListRevisionAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Paginator.ListRevisionAssets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators/#listrevisionassetspaginator)
        """
