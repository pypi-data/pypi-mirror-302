"""
Type annotations for ebs service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ebs.client import EBSClient

    session = Session()
    client: EBSClient = session.client("ebs")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CompleteSnapshotRequestRequestTypeDef,
    CompleteSnapshotResponseTypeDef,
    GetSnapshotBlockRequestRequestTypeDef,
    GetSnapshotBlockResponseTypeDef,
    ListChangedBlocksRequestRequestTypeDef,
    ListChangedBlocksResponseTypeDef,
    ListSnapshotBlocksRequestRequestTypeDef,
    ListSnapshotBlocksResponseTypeDef,
    PutSnapshotBlockRequestRequestTypeDef,
    PutSnapshotBlockResponseTypeDef,
    StartSnapshotRequestRequestTypeDef,
    StartSnapshotResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("EBSClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentLimitExceededException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    RequestThrottledException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class EBSClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EBSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#close)
        """

    def complete_snapshot(
        self, **kwargs: Unpack[CompleteSnapshotRequestRequestTypeDef]
    ) -> CompleteSnapshotResponseTypeDef:
        """
        Seals and completes the snapshot after all of the required blocks of data have
        been written to
        it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.complete_snapshot)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#complete_snapshot)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#generate_presigned_url)
        """

    def get_snapshot_block(
        self, **kwargs: Unpack[GetSnapshotBlockRequestRequestTypeDef]
    ) -> GetSnapshotBlockResponseTypeDef:
        """
        Returns the data in a block in an Amazon Elastic Block Store snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.get_snapshot_block)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#get_snapshot_block)
        """

    def list_changed_blocks(
        self, **kwargs: Unpack[ListChangedBlocksRequestRequestTypeDef]
    ) -> ListChangedBlocksResponseTypeDef:
        """
        Returns information about the blocks that are different between two Amazon
        Elastic Block Store snapshots of the same volume/snapshot
        lineage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.list_changed_blocks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#list_changed_blocks)
        """

    def list_snapshot_blocks(
        self, **kwargs: Unpack[ListSnapshotBlocksRequestRequestTypeDef]
    ) -> ListSnapshotBlocksResponseTypeDef:
        """
        Returns information about the blocks in an Amazon Elastic Block Store snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.list_snapshot_blocks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#list_snapshot_blocks)
        """

    def put_snapshot_block(
        self, **kwargs: Unpack[PutSnapshotBlockRequestRequestTypeDef]
    ) -> PutSnapshotBlockResponseTypeDef:
        """
        Writes a block of data to a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.put_snapshot_block)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#put_snapshot_block)
        """

    def start_snapshot(
        self, **kwargs: Unpack[StartSnapshotRequestRequestTypeDef]
    ) -> StartSnapshotResponseTypeDef:
        """
        Creates a new Amazon EBS snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.start_snapshot)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ebs/client/#start_snapshot)
        """
