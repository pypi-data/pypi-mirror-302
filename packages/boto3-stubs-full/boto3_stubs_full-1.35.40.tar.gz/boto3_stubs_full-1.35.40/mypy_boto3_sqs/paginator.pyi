"""
Type annotations for sqs service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sqs/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sqs.client import SQSClient
    from mypy_boto3_sqs.paginator import (
        ListDeadLetterSourceQueuesPaginator,
        ListQueuesPaginator,
    )

    session = Session()
    client: SQSClient = session.client("sqs")

    list_dead_letter_source_queues_paginator: ListDeadLetterSourceQueuesPaginator = client.get_paginator("list_dead_letter_source_queues")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef,
    ListDeadLetterSourceQueuesResultTypeDef,
    ListQueuesRequestListQueuesPaginateTypeDef,
    ListQueuesResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDeadLetterSourceQueuesPaginator", "ListQueuesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDeadLetterSourceQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Paginator.ListDeadLetterSourceQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sqs/paginators/#listdeadlettersourcequeuespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef
        ],
    ) -> _PageIterator[ListDeadLetterSourceQueuesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Paginator.ListDeadLetterSourceQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sqs/paginators/#listdeadlettersourcequeuespaginator)
        """

class ListQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Paginator.ListQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sqs/paginators/#listqueuespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueuesRequestListQueuesPaginateTypeDef]
    ) -> _PageIterator[ListQueuesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Paginator.ListQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sqs/paginators/#listqueuespaginator)
        """
