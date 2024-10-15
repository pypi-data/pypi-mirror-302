"""
Type annotations for timestream-query service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_timestream_query.client import TimestreamQueryClient

    session = Session()
    client: TimestreamQueryClient = session.client("timestream-query")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListScheduledQueriesPaginator, ListTagsForResourcePaginator, QueryPaginator
from .type_defs import (
    CancelQueryRequestRequestTypeDef,
    CancelQueryResponseTypeDef,
    CreateScheduledQueryRequestRequestTypeDef,
    CreateScheduledQueryResponseTypeDef,
    DeleteScheduledQueryRequestRequestTypeDef,
    DescribeAccountSettingsResponseTypeDef,
    DescribeEndpointsResponseTypeDef,
    DescribeScheduledQueryRequestRequestTypeDef,
    DescribeScheduledQueryResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExecuteScheduledQueryRequestRequestTypeDef,
    ListScheduledQueriesRequestRequestTypeDef,
    ListScheduledQueriesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PrepareQueryRequestRequestTypeDef,
    PrepareQueryResponseTypeDef,
    QueryRequestRequestTypeDef,
    QueryResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccountSettingsRequestRequestTypeDef,
    UpdateAccountSettingsResponseTypeDef,
    UpdateScheduledQueryRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("TimestreamQueryClient",)

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
    InvalidEndpointException: Type[BotocoreClientError]
    QueryExecutionException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class TimestreamQueryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TimestreamQueryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#can_paginate)
        """

    def cancel_query(
        self, **kwargs: Unpack[CancelQueryRequestRequestTypeDef]
    ) -> CancelQueryResponseTypeDef:
        """
        Cancels a query that has been issued.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.cancel_query)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#cancel_query)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#close)
        """

    def create_scheduled_query(
        self, **kwargs: Unpack[CreateScheduledQueryRequestRequestTypeDef]
    ) -> CreateScheduledQueryResponseTypeDef:
        """
        Create a scheduled query that will be run on your behalf at the configured
        schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.create_scheduled_query)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#create_scheduled_query)
        """

    def delete_scheduled_query(
        self, **kwargs: Unpack[DeleteScheduledQueryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a given scheduled query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.delete_scheduled_query)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#delete_scheduled_query)
        """

    def describe_account_settings(self) -> DescribeAccountSettingsResponseTypeDef:
        """
        Describes the settings for your account that include the query pricing model
        and the configured maximum TCUs the service can use for your query
        workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.describe_account_settings)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#describe_account_settings)
        """

    def describe_endpoints(self) -> DescribeEndpointsResponseTypeDef:
        """
        DescribeEndpoints returns a list of available endpoints to make Timestream API
        calls
        against.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.describe_endpoints)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#describe_endpoints)
        """

    def describe_scheduled_query(
        self, **kwargs: Unpack[DescribeScheduledQueryRequestRequestTypeDef]
    ) -> DescribeScheduledQueryResponseTypeDef:
        """
        Provides detailed information about a scheduled query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.describe_scheduled_query)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#describe_scheduled_query)
        """

    def execute_scheduled_query(
        self, **kwargs: Unpack[ExecuteScheduledQueryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        You can use this API to run a scheduled query manually.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.execute_scheduled_query)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#execute_scheduled_query)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#generate_presigned_url)
        """

    def list_scheduled_queries(
        self, **kwargs: Unpack[ListScheduledQueriesRequestRequestTypeDef]
    ) -> ListScheduledQueriesResponseTypeDef:
        """
        Gets a list of all scheduled queries in the caller's Amazon account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.list_scheduled_queries)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#list_scheduled_queries)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags on a Timestream query resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#list_tags_for_resource)
        """

    def prepare_query(
        self, **kwargs: Unpack[PrepareQueryRequestRequestTypeDef]
    ) -> PrepareQueryResponseTypeDef:
        """
        A synchronous operation that allows you to submit a query with parameters to be
        stored by Timestream for later
        running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.prepare_query)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#prepare_query)
        """

    def query(self, **kwargs: Unpack[QueryRequestRequestTypeDef]) -> QueryResponseTypeDef:
        """
        `Query` is a synchronous operation that enables you to run a query against your
        Amazon Timestream
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.query)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#query)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associate a set of tags with a Timestream resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the association of tags from a Timestream query resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#untag_resource)
        """

    def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsRequestRequestTypeDef]
    ) -> UpdateAccountSettingsResponseTypeDef:
        """
        Transitions your account to use TCUs for query pricing and modifies the maximum
        query compute units that you've
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.update_account_settings)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#update_account_settings)
        """

    def update_scheduled_query(
        self, **kwargs: Unpack[UpdateScheduledQueryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update a scheduled query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.update_scheduled_query)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#update_scheduled_query)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_scheduled_queries"]
    ) -> ListScheduledQueriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query"]) -> QueryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#get_paginator)
        """
