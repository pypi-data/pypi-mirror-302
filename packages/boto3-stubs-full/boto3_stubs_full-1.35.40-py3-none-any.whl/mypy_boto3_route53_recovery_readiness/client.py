"""
Type annotations for route53-recovery-readiness service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_route53_recovery_readiness.client import Route53RecoveryReadinessClient

    session = Session()
    client: Route53RecoveryReadinessClient = session.client("route53-recovery-readiness")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetCellReadinessSummaryPaginator,
    GetReadinessCheckResourceStatusPaginator,
    GetReadinessCheckStatusPaginator,
    GetRecoveryGroupReadinessSummaryPaginator,
    ListCellsPaginator,
    ListCrossAccountAuthorizationsPaginator,
    ListReadinessChecksPaginator,
    ListRecoveryGroupsPaginator,
    ListResourceSetsPaginator,
    ListRulesPaginator,
)
from .type_defs import (
    CreateCellRequestRequestTypeDef,
    CreateCellResponseTypeDef,
    CreateCrossAccountAuthorizationRequestRequestTypeDef,
    CreateCrossAccountAuthorizationResponseTypeDef,
    CreateReadinessCheckRequestRequestTypeDef,
    CreateReadinessCheckResponseTypeDef,
    CreateRecoveryGroupRequestRequestTypeDef,
    CreateRecoveryGroupResponseTypeDef,
    CreateResourceSetRequestRequestTypeDef,
    CreateResourceSetResponseTypeDef,
    DeleteCellRequestRequestTypeDef,
    DeleteCrossAccountAuthorizationRequestRequestTypeDef,
    DeleteReadinessCheckRequestRequestTypeDef,
    DeleteRecoveryGroupRequestRequestTypeDef,
    DeleteResourceSetRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetArchitectureRecommendationsRequestRequestTypeDef,
    GetArchitectureRecommendationsResponseTypeDef,
    GetCellReadinessSummaryRequestRequestTypeDef,
    GetCellReadinessSummaryResponseTypeDef,
    GetCellRequestRequestTypeDef,
    GetCellResponseTypeDef,
    GetReadinessCheckRequestRequestTypeDef,
    GetReadinessCheckResourceStatusRequestRequestTypeDef,
    GetReadinessCheckResourceStatusResponseTypeDef,
    GetReadinessCheckResponseTypeDef,
    GetReadinessCheckStatusRequestRequestTypeDef,
    GetReadinessCheckStatusResponseTypeDef,
    GetRecoveryGroupReadinessSummaryRequestRequestTypeDef,
    GetRecoveryGroupReadinessSummaryResponseTypeDef,
    GetRecoveryGroupRequestRequestTypeDef,
    GetRecoveryGroupResponseTypeDef,
    GetResourceSetRequestRequestTypeDef,
    GetResourceSetResponseTypeDef,
    ListCellsRequestRequestTypeDef,
    ListCellsResponseTypeDef,
    ListCrossAccountAuthorizationsRequestRequestTypeDef,
    ListCrossAccountAuthorizationsResponseTypeDef,
    ListReadinessChecksRequestRequestTypeDef,
    ListReadinessChecksResponseTypeDef,
    ListRecoveryGroupsRequestRequestTypeDef,
    ListRecoveryGroupsResponseTypeDef,
    ListResourceSetsRequestRequestTypeDef,
    ListResourceSetsResponseTypeDef,
    ListRulesRequestRequestTypeDef,
    ListRulesResponseTypeDef,
    ListTagsForResourcesRequestRequestTypeDef,
    ListTagsForResourcesResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCellRequestRequestTypeDef,
    UpdateCellResponseTypeDef,
    UpdateReadinessCheckRequestRequestTypeDef,
    UpdateReadinessCheckResponseTypeDef,
    UpdateRecoveryGroupRequestRequestTypeDef,
    UpdateRecoveryGroupResponseTypeDef,
    UpdateResourceSetRequestRequestTypeDef,
    UpdateResourceSetResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("Route53RecoveryReadinessClient",)


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
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Route53RecoveryReadinessClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53RecoveryReadinessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#close)
        """

    def create_cell(
        self, **kwargs: Unpack[CreateCellRequestRequestTypeDef]
    ) -> CreateCellResponseTypeDef:
        """
        Creates a cell in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.create_cell)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#create_cell)
        """

    def create_cross_account_authorization(
        self, **kwargs: Unpack[CreateCrossAccountAuthorizationRequestRequestTypeDef]
    ) -> CreateCrossAccountAuthorizationResponseTypeDef:
        """
        Creates a cross-account readiness authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.create_cross_account_authorization)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#create_cross_account_authorization)
        """

    def create_readiness_check(
        self, **kwargs: Unpack[CreateReadinessCheckRequestRequestTypeDef]
    ) -> CreateReadinessCheckResponseTypeDef:
        """
        Creates a readiness check in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.create_readiness_check)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#create_readiness_check)
        """

    def create_recovery_group(
        self, **kwargs: Unpack[CreateRecoveryGroupRequestRequestTypeDef]
    ) -> CreateRecoveryGroupResponseTypeDef:
        """
        Creates a recovery group in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.create_recovery_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#create_recovery_group)
        """

    def create_resource_set(
        self, **kwargs: Unpack[CreateResourceSetRequestRequestTypeDef]
    ) -> CreateResourceSetResponseTypeDef:
        """
        Creates a resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.create_resource_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#create_resource_set)
        """

    def delete_cell(
        self, **kwargs: Unpack[DeleteCellRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a cell.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.delete_cell)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#delete_cell)
        """

    def delete_cross_account_authorization(
        self, **kwargs: Unpack[DeleteCrossAccountAuthorizationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes cross account readiness authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.delete_cross_account_authorization)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#delete_cross_account_authorization)
        """

    def delete_readiness_check(
        self, **kwargs: Unpack[DeleteReadinessCheckRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a readiness check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.delete_readiness_check)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#delete_readiness_check)
        """

    def delete_recovery_group(
        self, **kwargs: Unpack[DeleteRecoveryGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a recovery group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.delete_recovery_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#delete_recovery_group)
        """

    def delete_resource_set(
        self, **kwargs: Unpack[DeleteResourceSetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.delete_resource_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#delete_resource_set)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#generate_presigned_url)
        """

    def get_architecture_recommendations(
        self, **kwargs: Unpack[GetArchitectureRecommendationsRequestRequestTypeDef]
    ) -> GetArchitectureRecommendationsResponseTypeDef:
        """
        Gets recommendations about architecture designs for improving resiliency for an
        application, based on a recovery
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_architecture_recommendations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_architecture_recommendations)
        """

    def get_cell(self, **kwargs: Unpack[GetCellRequestRequestTypeDef]) -> GetCellResponseTypeDef:
        """
        Gets information about a cell including cell name, cell Amazon Resource Name
        (ARN), ARNs of nested cells for this cell, and a list of those cell ARNs with
        their associated recovery group
        ARNs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_cell)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_cell)
        """

    def get_cell_readiness_summary(
        self, **kwargs: Unpack[GetCellReadinessSummaryRequestRequestTypeDef]
    ) -> GetCellReadinessSummaryResponseTypeDef:
        """
        Gets readiness for a cell.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_cell_readiness_summary)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_cell_readiness_summary)
        """

    def get_readiness_check(
        self, **kwargs: Unpack[GetReadinessCheckRequestRequestTypeDef]
    ) -> GetReadinessCheckResponseTypeDef:
        """
        Gets details about a readiness check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_readiness_check)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_readiness_check)
        """

    def get_readiness_check_resource_status(
        self, **kwargs: Unpack[GetReadinessCheckResourceStatusRequestRequestTypeDef]
    ) -> GetReadinessCheckResourceStatusResponseTypeDef:
        """
        Gets individual readiness status for a readiness check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_readiness_check_resource_status)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_readiness_check_resource_status)
        """

    def get_readiness_check_status(
        self, **kwargs: Unpack[GetReadinessCheckStatusRequestRequestTypeDef]
    ) -> GetReadinessCheckStatusResponseTypeDef:
        """
        Gets the readiness status for an individual readiness check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_readiness_check_status)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_readiness_check_status)
        """

    def get_recovery_group(
        self, **kwargs: Unpack[GetRecoveryGroupRequestRequestTypeDef]
    ) -> GetRecoveryGroupResponseTypeDef:
        """
        Gets details about a recovery group, including a list of the cells that are
        included in
        it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_recovery_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_recovery_group)
        """

    def get_recovery_group_readiness_summary(
        self, **kwargs: Unpack[GetRecoveryGroupReadinessSummaryRequestRequestTypeDef]
    ) -> GetRecoveryGroupReadinessSummaryResponseTypeDef:
        """
        Displays a summary of information about a recovery group's readiness status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_recovery_group_readiness_summary)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_recovery_group_readiness_summary)
        """

    def get_resource_set(
        self, **kwargs: Unpack[GetResourceSetRequestRequestTypeDef]
    ) -> GetResourceSetResponseTypeDef:
        """
        Displays the details about a resource set, including a list of the resources in
        the
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_resource_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_resource_set)
        """

    def list_cells(
        self, **kwargs: Unpack[ListCellsRequestRequestTypeDef]
    ) -> ListCellsResponseTypeDef:
        """
        Lists the cells for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.list_cells)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#list_cells)
        """

    def list_cross_account_authorizations(
        self, **kwargs: Unpack[ListCrossAccountAuthorizationsRequestRequestTypeDef]
    ) -> ListCrossAccountAuthorizationsResponseTypeDef:
        """
        Lists the cross-account readiness authorizations that are in place for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.list_cross_account_authorizations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#list_cross_account_authorizations)
        """

    def list_readiness_checks(
        self, **kwargs: Unpack[ListReadinessChecksRequestRequestTypeDef]
    ) -> ListReadinessChecksResponseTypeDef:
        """
        Lists the readiness checks for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.list_readiness_checks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#list_readiness_checks)
        """

    def list_recovery_groups(
        self, **kwargs: Unpack[ListRecoveryGroupsRequestRequestTypeDef]
    ) -> ListRecoveryGroupsResponseTypeDef:
        """
        Lists the recovery groups in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.list_recovery_groups)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#list_recovery_groups)
        """

    def list_resource_sets(
        self, **kwargs: Unpack[ListResourceSetsRequestRequestTypeDef]
    ) -> ListResourceSetsResponseTypeDef:
        """
        Lists the resource sets in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.list_resource_sets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#list_resource_sets)
        """

    def list_rules(
        self, **kwargs: Unpack[ListRulesRequestRequestTypeDef]
    ) -> ListRulesResponseTypeDef:
        """
        Lists all readiness rules, or lists the readiness rules for a specific resource
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.list_rules)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#list_rules)
        """

    def list_tags_for_resources(
        self, **kwargs: Unpack[ListTagsForResourcesRequestRequestTypeDef]
    ) -> ListTagsForResourcesResponseTypeDef:
        """
        Lists the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.list_tags_for_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#list_tags_for_resources)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#untag_resource)
        """

    def update_cell(
        self, **kwargs: Unpack[UpdateCellRequestRequestTypeDef]
    ) -> UpdateCellResponseTypeDef:
        """
        Updates a cell to replace the list of nested cells with a new list of nested
        cells.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.update_cell)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#update_cell)
        """

    def update_readiness_check(
        self, **kwargs: Unpack[UpdateReadinessCheckRequestRequestTypeDef]
    ) -> UpdateReadinessCheckResponseTypeDef:
        """
        Updates a readiness check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.update_readiness_check)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#update_readiness_check)
        """

    def update_recovery_group(
        self, **kwargs: Unpack[UpdateRecoveryGroupRequestRequestTypeDef]
    ) -> UpdateRecoveryGroupResponseTypeDef:
        """
        Updates a recovery group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.update_recovery_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#update_recovery_group)
        """

    def update_resource_set(
        self, **kwargs: Unpack[UpdateResourceSetRequestRequestTypeDef]
    ) -> UpdateResourceSetResponseTypeDef:
        """
        Updates a resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.update_resource_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#update_resource_set)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_cell_readiness_summary"]
    ) -> GetCellReadinessSummaryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_readiness_check_resource_status"]
    ) -> GetReadinessCheckResourceStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_readiness_check_status"]
    ) -> GetReadinessCheckStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_recovery_group_readiness_summary"]
    ) -> GetRecoveryGroupReadinessSummaryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_cells"]) -> ListCellsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cross_account_authorizations"]
    ) -> ListCrossAccountAuthorizationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_readiness_checks"]
    ) -> ListReadinessChecksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recovery_groups"]
    ) -> ListRecoveryGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_sets"]
    ) -> ListResourceSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rules"]) -> ListRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/client/#get_paginator)
        """
