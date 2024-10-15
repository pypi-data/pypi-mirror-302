"""
Type annotations for accessanalyzer service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_accessanalyzer.client import AccessAnalyzerClient

    session = Session()
    client: AccessAnalyzerClient = session.client("accessanalyzer")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetFindingRecommendationPaginator,
    GetFindingV2Paginator,
    ListAccessPreviewFindingsPaginator,
    ListAccessPreviewsPaginator,
    ListAnalyzedResourcesPaginator,
    ListAnalyzersPaginator,
    ListArchiveRulesPaginator,
    ListFindingsPaginator,
    ListFindingsV2Paginator,
    ListPolicyGenerationsPaginator,
    ValidatePolicyPaginator,
)
from .type_defs import (
    ApplyArchiveRuleRequestRequestTypeDef,
    CancelPolicyGenerationRequestRequestTypeDef,
    CheckAccessNotGrantedRequestRequestTypeDef,
    CheckAccessNotGrantedResponseTypeDef,
    CheckNoNewAccessRequestRequestTypeDef,
    CheckNoNewAccessResponseTypeDef,
    CheckNoPublicAccessRequestRequestTypeDef,
    CheckNoPublicAccessResponseTypeDef,
    CreateAccessPreviewRequestRequestTypeDef,
    CreateAccessPreviewResponseTypeDef,
    CreateAnalyzerRequestRequestTypeDef,
    CreateAnalyzerResponseTypeDef,
    CreateArchiveRuleRequestRequestTypeDef,
    DeleteAnalyzerRequestRequestTypeDef,
    DeleteArchiveRuleRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GenerateFindingRecommendationRequestRequestTypeDef,
    GetAccessPreviewRequestRequestTypeDef,
    GetAccessPreviewResponseTypeDef,
    GetAnalyzedResourceRequestRequestTypeDef,
    GetAnalyzedResourceResponseTypeDef,
    GetAnalyzerRequestRequestTypeDef,
    GetAnalyzerResponseTypeDef,
    GetArchiveRuleRequestRequestTypeDef,
    GetArchiveRuleResponseTypeDef,
    GetFindingRecommendationRequestRequestTypeDef,
    GetFindingRecommendationResponseTypeDef,
    GetFindingRequestRequestTypeDef,
    GetFindingResponseTypeDef,
    GetFindingV2RequestRequestTypeDef,
    GetFindingV2ResponseTypeDef,
    GetGeneratedPolicyRequestRequestTypeDef,
    GetGeneratedPolicyResponseTypeDef,
    ListAccessPreviewFindingsRequestRequestTypeDef,
    ListAccessPreviewFindingsResponseTypeDef,
    ListAccessPreviewsRequestRequestTypeDef,
    ListAccessPreviewsResponseTypeDef,
    ListAnalyzedResourcesRequestRequestTypeDef,
    ListAnalyzedResourcesResponseTypeDef,
    ListAnalyzersRequestRequestTypeDef,
    ListAnalyzersResponseTypeDef,
    ListArchiveRulesRequestRequestTypeDef,
    ListArchiveRulesResponseTypeDef,
    ListFindingsRequestRequestTypeDef,
    ListFindingsResponseTypeDef,
    ListFindingsV2RequestRequestTypeDef,
    ListFindingsV2ResponseTypeDef,
    ListPolicyGenerationsRequestRequestTypeDef,
    ListPolicyGenerationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartPolicyGenerationRequestRequestTypeDef,
    StartPolicyGenerationResponseTypeDef,
    StartResourceScanRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateArchiveRuleRequestRequestTypeDef,
    UpdateFindingsRequestRequestTypeDef,
    ValidatePolicyRequestRequestTypeDef,
    ValidatePolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AccessAnalyzerClient",)


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
    InvalidParameterException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AccessAnalyzerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AccessAnalyzerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#exceptions)
        """

    def apply_archive_rule(
        self, **kwargs: Unpack[ApplyArchiveRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Retroactively applies the archive rule to existing findings that meet the
        archive rule
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.apply_archive_rule)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#apply_archive_rule)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#can_paginate)
        """

    def cancel_policy_generation(
        self, **kwargs: Unpack[CancelPolicyGenerationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the requested policy generation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.cancel_policy_generation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#cancel_policy_generation)
        """

    def check_access_not_granted(
        self, **kwargs: Unpack[CheckAccessNotGrantedRequestRequestTypeDef]
    ) -> CheckAccessNotGrantedResponseTypeDef:
        """
        Checks whether the specified access isn't allowed by a policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.check_access_not_granted)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#check_access_not_granted)
        """

    def check_no_new_access(
        self, **kwargs: Unpack[CheckNoNewAccessRequestRequestTypeDef]
    ) -> CheckNoNewAccessResponseTypeDef:
        """
        Checks whether new access is allowed for an updated policy when compared to the
        existing
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.check_no_new_access)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#check_no_new_access)
        """

    def check_no_public_access(
        self, **kwargs: Unpack[CheckNoPublicAccessRequestRequestTypeDef]
    ) -> CheckNoPublicAccessResponseTypeDef:
        """
        Checks whether a resource policy can grant public access to the specified
        resource
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.check_no_public_access)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#check_no_public_access)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#close)
        """

    def create_access_preview(
        self, **kwargs: Unpack[CreateAccessPreviewRequestRequestTypeDef]
    ) -> CreateAccessPreviewResponseTypeDef:
        """
        Creates an access preview that allows you to preview IAM Access Analyzer
        findings for your resource before deploying resource
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.create_access_preview)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#create_access_preview)
        """

    def create_analyzer(
        self, **kwargs: Unpack[CreateAnalyzerRequestRequestTypeDef]
    ) -> CreateAnalyzerResponseTypeDef:
        """
        Creates an analyzer for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.create_analyzer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#create_analyzer)
        """

    def create_archive_rule(
        self, **kwargs: Unpack[CreateArchiveRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates an archive rule for the specified analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.create_archive_rule)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#create_archive_rule)
        """

    def delete_analyzer(
        self, **kwargs: Unpack[DeleteAnalyzerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.delete_analyzer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#delete_analyzer)
        """

    def delete_archive_rule(
        self, **kwargs: Unpack[DeleteArchiveRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified archive rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.delete_archive_rule)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#delete_archive_rule)
        """

    def generate_finding_recommendation(
        self, **kwargs: Unpack[GenerateFindingRecommendationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a recommendation for an unused permissions finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.generate_finding_recommendation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#generate_finding_recommendation)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#generate_presigned_url)
        """

    def get_access_preview(
        self, **kwargs: Unpack[GetAccessPreviewRequestRequestTypeDef]
    ) -> GetAccessPreviewResponseTypeDef:
        """
        Retrieves information about an access preview for the specified analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_access_preview)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_access_preview)
        """

    def get_analyzed_resource(
        self, **kwargs: Unpack[GetAnalyzedResourceRequestRequestTypeDef]
    ) -> GetAnalyzedResourceResponseTypeDef:
        """
        Retrieves information about a resource that was analyzed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_analyzed_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_analyzed_resource)
        """

    def get_analyzer(
        self, **kwargs: Unpack[GetAnalyzerRequestRequestTypeDef]
    ) -> GetAnalyzerResponseTypeDef:
        """
        Retrieves information about the specified analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_analyzer)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_analyzer)
        """

    def get_archive_rule(
        self, **kwargs: Unpack[GetArchiveRuleRequestRequestTypeDef]
    ) -> GetArchiveRuleResponseTypeDef:
        """
        Retrieves information about an archive rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_archive_rule)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_archive_rule)
        """

    def get_finding(
        self, **kwargs: Unpack[GetFindingRequestRequestTypeDef]
    ) -> GetFindingResponseTypeDef:
        """
        Retrieves information about the specified finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_finding)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_finding)
        """

    def get_finding_recommendation(
        self, **kwargs: Unpack[GetFindingRecommendationRequestRequestTypeDef]
    ) -> GetFindingRecommendationResponseTypeDef:
        """
        Retrieves information about a finding recommendation for the specified analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_finding_recommendation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_finding_recommendation)
        """

    def get_finding_v2(
        self, **kwargs: Unpack[GetFindingV2RequestRequestTypeDef]
    ) -> GetFindingV2ResponseTypeDef:
        """
        Retrieves information about the specified finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_finding_v2)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_finding_v2)
        """

    def get_generated_policy(
        self, **kwargs: Unpack[GetGeneratedPolicyRequestRequestTypeDef]
    ) -> GetGeneratedPolicyResponseTypeDef:
        """
        Retrieves the policy that was generated using `StartPolicyGeneration`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_generated_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_generated_policy)
        """

    def list_access_preview_findings(
        self, **kwargs: Unpack[ListAccessPreviewFindingsRequestRequestTypeDef]
    ) -> ListAccessPreviewFindingsResponseTypeDef:
        """
        Retrieves a list of access preview findings generated by the specified access
        preview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_access_preview_findings)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#list_access_preview_findings)
        """

    def list_access_previews(
        self, **kwargs: Unpack[ListAccessPreviewsRequestRequestTypeDef]
    ) -> ListAccessPreviewsResponseTypeDef:
        """
        Retrieves a list of access previews for the specified analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_access_previews)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#list_access_previews)
        """

    def list_analyzed_resources(
        self, **kwargs: Unpack[ListAnalyzedResourcesRequestRequestTypeDef]
    ) -> ListAnalyzedResourcesResponseTypeDef:
        """
        Retrieves a list of resources of the specified type that have been analyzed by
        the specified external access
        analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_analyzed_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#list_analyzed_resources)
        """

    def list_analyzers(
        self, **kwargs: Unpack[ListAnalyzersRequestRequestTypeDef]
    ) -> ListAnalyzersResponseTypeDef:
        """
        Retrieves a list of analyzers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_analyzers)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#list_analyzers)
        """

    def list_archive_rules(
        self, **kwargs: Unpack[ListArchiveRulesRequestRequestTypeDef]
    ) -> ListArchiveRulesResponseTypeDef:
        """
        Retrieves a list of archive rules created for the specified analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_archive_rules)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#list_archive_rules)
        """

    def list_findings(
        self, **kwargs: Unpack[ListFindingsRequestRequestTypeDef]
    ) -> ListFindingsResponseTypeDef:
        """
        Retrieves a list of findings generated by the specified analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_findings)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#list_findings)
        """

    def list_findings_v2(
        self, **kwargs: Unpack[ListFindingsV2RequestRequestTypeDef]
    ) -> ListFindingsV2ResponseTypeDef:
        """
        Retrieves a list of findings generated by the specified analyzer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_findings_v2)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#list_findings_v2)
        """

    def list_policy_generations(
        self, **kwargs: Unpack[ListPolicyGenerationsRequestRequestTypeDef]
    ) -> ListPolicyGenerationsResponseTypeDef:
        """
        Lists all of the policy generations requested in the last seven days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_policy_generations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#list_policy_generations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of tags applied to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#list_tags_for_resource)
        """

    def start_policy_generation(
        self, **kwargs: Unpack[StartPolicyGenerationRequestRequestTypeDef]
    ) -> StartPolicyGenerationResponseTypeDef:
        """
        Starts the policy generation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.start_policy_generation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#start_policy_generation)
        """

    def start_resource_scan(
        self, **kwargs: Unpack[StartResourceScanRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Immediately starts a scan of the policies applied to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.start_resource_scan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#start_resource_scan)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds a tag to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#untag_resource)
        """

    def update_archive_rule(
        self, **kwargs: Unpack[UpdateArchiveRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the criteria and values for the specified archive rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.update_archive_rule)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#update_archive_rule)
        """

    def update_findings(
        self, **kwargs: Unpack[UpdateFindingsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the status for the specified findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.update_findings)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#update_findings)
        """

    def validate_policy(
        self, **kwargs: Unpack[ValidatePolicyRequestRequestTypeDef]
    ) -> ValidatePolicyResponseTypeDef:
        """
        Requests the validation of a policy and returns a list of findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.validate_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#validate_policy)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_finding_recommendation"]
    ) -> GetFindingRecommendationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_finding_v2"]) -> GetFindingV2Paginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_access_preview_findings"]
    ) -> ListAccessPreviewFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_access_previews"]
    ) -> ListAccessPreviewsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_analyzed_resources"]
    ) -> ListAnalyzedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_analyzers"]) -> ListAnalyzersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_archive_rules"]
    ) -> ListArchiveRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_findings"]) -> ListFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_findings_v2"]) -> ListFindingsV2Paginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_generations"]
    ) -> ListPolicyGenerationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["validate_policy"]) -> ValidatePolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/client/#get_paginator)
        """
