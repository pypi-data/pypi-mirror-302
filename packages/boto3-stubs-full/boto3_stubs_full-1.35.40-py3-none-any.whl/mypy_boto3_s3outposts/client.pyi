"""
Type annotations for s3outposts service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_s3outposts.client import S3OutpostsClient

    session = Session()
    client: S3OutpostsClient = session.client("s3outposts")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListEndpointsPaginator,
    ListOutpostsWithS3Paginator,
    ListSharedEndpointsPaginator,
)
from .type_defs import (
    CreateEndpointRequestRequestTypeDef,
    CreateEndpointResultTypeDef,
    DeleteEndpointRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    ListEndpointsRequestRequestTypeDef,
    ListEndpointsResultTypeDef,
    ListOutpostsWithS3RequestRequestTypeDef,
    ListOutpostsWithS3ResultTypeDef,
    ListSharedEndpointsRequestRequestTypeDef,
    ListSharedEndpointsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("S3OutpostsClient",)

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
    OutpostOfflineException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class S3OutpostsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3OutpostsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#close)
        """

    def create_endpoint(
        self, **kwargs: Unpack[CreateEndpointRequestRequestTypeDef]
    ) -> CreateEndpointResultTypeDef:
        """
        Creates an endpoint and associates it with the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.create_endpoint)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#create_endpoint)
        """

    def delete_endpoint(
        self, **kwargs: Unpack[DeleteEndpointRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.delete_endpoint)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#delete_endpoint)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#generate_presigned_url)
        """

    def list_endpoints(
        self, **kwargs: Unpack[ListEndpointsRequestRequestTypeDef]
    ) -> ListEndpointsResultTypeDef:
        """
        Lists endpoints associated with the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.list_endpoints)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#list_endpoints)
        """

    def list_outposts_with_s3(
        self, **kwargs: Unpack[ListOutpostsWithS3RequestRequestTypeDef]
    ) -> ListOutpostsWithS3ResultTypeDef:
        """
        Lists the Outposts with S3 on Outposts capacity for your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.list_outposts_with_s3)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#list_outposts_with_s3)
        """

    def list_shared_endpoints(
        self, **kwargs: Unpack[ListSharedEndpointsRequestRequestTypeDef]
    ) -> ListSharedEndpointsResultTypeDef:
        """
        Lists all endpoints associated with an Outpost that has been shared by Amazon
        Web Services Resource Access Manager
        (RAM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.list_shared_endpoints)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#list_shared_endpoints)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_endpoints"]) -> ListEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_outposts_with_s3"]
    ) -> ListOutpostsWithS3Paginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_shared_endpoints"]
    ) -> ListSharedEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/client/#get_paginator)
        """
