"""
Type annotations for kendra-ranking service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kendra_ranking.client import KendraRankingClient

    session = Session()
    client: KendraRankingClient = session.client("kendra-ranking")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateRescoreExecutionPlanRequestRequestTypeDef,
    CreateRescoreExecutionPlanResponseTypeDef,
    DeleteRescoreExecutionPlanRequestRequestTypeDef,
    DescribeRescoreExecutionPlanRequestRequestTypeDef,
    DescribeRescoreExecutionPlanResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ListRescoreExecutionPlansRequestRequestTypeDef,
    ListRescoreExecutionPlansResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RescoreRequestRequestTypeDef,
    RescoreResultTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateRescoreExecutionPlanRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("KendraRankingClient",)

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
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class KendraRankingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KendraRankingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#close)
        """

    def create_rescore_execution_plan(
        self, **kwargs: Unpack[CreateRescoreExecutionPlanRequestRequestTypeDef]
    ) -> CreateRescoreExecutionPlanResponseTypeDef:
        """
        Creates a rescore execution plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.create_rescore_execution_plan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#create_rescore_execution_plan)
        """

    def delete_rescore_execution_plan(
        self, **kwargs: Unpack[DeleteRescoreExecutionPlanRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a rescore execution plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.delete_rescore_execution_plan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#delete_rescore_execution_plan)
        """

    def describe_rescore_execution_plan(
        self, **kwargs: Unpack[DescribeRescoreExecutionPlanRequestRequestTypeDef]
    ) -> DescribeRescoreExecutionPlanResponseTypeDef:
        """
        Gets information about a rescore execution plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.describe_rescore_execution_plan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#describe_rescore_execution_plan)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#generate_presigned_url)
        """

    def list_rescore_execution_plans(
        self, **kwargs: Unpack[ListRescoreExecutionPlansRequestRequestTypeDef]
    ) -> ListRescoreExecutionPlansResponseTypeDef:
        """
        Lists your rescore execution plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.list_rescore_execution_plans)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#list_rescore_execution_plans)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#list_tags_for_resource)
        """

    def rescore(self, **kwargs: Unpack[RescoreRequestRequestTypeDef]) -> RescoreResultTypeDef:
        """
        Rescores or re-ranks search results from a search service such as OpenSearch
        (self
        managed).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.rescore)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#rescore)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds a specified tag to a specified rescore execution plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from a rescore execution plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#untag_resource)
        """

    def update_rescore_execution_plan(
        self, **kwargs: Unpack[UpdateRescoreExecutionPlanRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a rescore execution plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra-ranking.html#KendraRanking.Client.update_rescore_execution_plan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/client/#update_rescore_execution_plan)
        """
