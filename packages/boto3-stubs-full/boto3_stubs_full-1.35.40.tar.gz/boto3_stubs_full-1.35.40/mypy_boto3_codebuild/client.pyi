"""
Type annotations for codebuild service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codebuild.client import CodeBuildClient

    session = Session()
    client: CodeBuildClient = session.client("codebuild")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeCodeCoveragesPaginator,
    DescribeTestCasesPaginator,
    ListBuildBatchesForProjectPaginator,
    ListBuildBatchesPaginator,
    ListBuildsForProjectPaginator,
    ListBuildsPaginator,
    ListProjectsPaginator,
    ListReportGroupsPaginator,
    ListReportsForReportGroupPaginator,
    ListReportsPaginator,
    ListSharedProjectsPaginator,
    ListSharedReportGroupsPaginator,
)
from .type_defs import (
    BatchDeleteBuildsInputRequestTypeDef,
    BatchDeleteBuildsOutputTypeDef,
    BatchGetBuildBatchesInputRequestTypeDef,
    BatchGetBuildBatchesOutputTypeDef,
    BatchGetBuildsInputRequestTypeDef,
    BatchGetBuildsOutputTypeDef,
    BatchGetFleetsInputRequestTypeDef,
    BatchGetFleetsOutputTypeDef,
    BatchGetProjectsInputRequestTypeDef,
    BatchGetProjectsOutputTypeDef,
    BatchGetReportGroupsInputRequestTypeDef,
    BatchGetReportGroupsOutputTypeDef,
    BatchGetReportsInputRequestTypeDef,
    BatchGetReportsOutputTypeDef,
    CreateFleetInputRequestTypeDef,
    CreateFleetOutputTypeDef,
    CreateProjectInputRequestTypeDef,
    CreateProjectOutputTypeDef,
    CreateReportGroupInputRequestTypeDef,
    CreateReportGroupOutputTypeDef,
    CreateWebhookInputRequestTypeDef,
    CreateWebhookOutputTypeDef,
    DeleteBuildBatchInputRequestTypeDef,
    DeleteBuildBatchOutputTypeDef,
    DeleteFleetInputRequestTypeDef,
    DeleteProjectInputRequestTypeDef,
    DeleteReportGroupInputRequestTypeDef,
    DeleteReportInputRequestTypeDef,
    DeleteResourcePolicyInputRequestTypeDef,
    DeleteSourceCredentialsInputRequestTypeDef,
    DeleteSourceCredentialsOutputTypeDef,
    DeleteWebhookInputRequestTypeDef,
    DescribeCodeCoveragesInputRequestTypeDef,
    DescribeCodeCoveragesOutputTypeDef,
    DescribeTestCasesInputRequestTypeDef,
    DescribeTestCasesOutputTypeDef,
    GetReportGroupTrendInputRequestTypeDef,
    GetReportGroupTrendOutputTypeDef,
    GetResourcePolicyInputRequestTypeDef,
    GetResourcePolicyOutputTypeDef,
    ImportSourceCredentialsInputRequestTypeDef,
    ImportSourceCredentialsOutputTypeDef,
    InvalidateProjectCacheInputRequestTypeDef,
    ListBuildBatchesForProjectInputRequestTypeDef,
    ListBuildBatchesForProjectOutputTypeDef,
    ListBuildBatchesInputRequestTypeDef,
    ListBuildBatchesOutputTypeDef,
    ListBuildsForProjectInputRequestTypeDef,
    ListBuildsForProjectOutputTypeDef,
    ListBuildsInputRequestTypeDef,
    ListBuildsOutputTypeDef,
    ListCuratedEnvironmentImagesOutputTypeDef,
    ListFleetsInputRequestTypeDef,
    ListFleetsOutputTypeDef,
    ListProjectsInputRequestTypeDef,
    ListProjectsOutputTypeDef,
    ListReportGroupsInputRequestTypeDef,
    ListReportGroupsOutputTypeDef,
    ListReportsForReportGroupInputRequestTypeDef,
    ListReportsForReportGroupOutputTypeDef,
    ListReportsInputRequestTypeDef,
    ListReportsOutputTypeDef,
    ListSharedProjectsInputRequestTypeDef,
    ListSharedProjectsOutputTypeDef,
    ListSharedReportGroupsInputRequestTypeDef,
    ListSharedReportGroupsOutputTypeDef,
    ListSourceCredentialsOutputTypeDef,
    PutResourcePolicyInputRequestTypeDef,
    PutResourcePolicyOutputTypeDef,
    RetryBuildBatchInputRequestTypeDef,
    RetryBuildBatchOutputTypeDef,
    RetryBuildInputRequestTypeDef,
    RetryBuildOutputTypeDef,
    StartBuildBatchInputRequestTypeDef,
    StartBuildBatchOutputTypeDef,
    StartBuildInputRequestTypeDef,
    StartBuildOutputTypeDef,
    StopBuildBatchInputRequestTypeDef,
    StopBuildBatchOutputTypeDef,
    StopBuildInputRequestTypeDef,
    StopBuildOutputTypeDef,
    UpdateFleetInputRequestTypeDef,
    UpdateFleetOutputTypeDef,
    UpdateProjectInputRequestTypeDef,
    UpdateProjectOutputTypeDef,
    UpdateProjectVisibilityInputRequestTypeDef,
    UpdateProjectVisibilityOutputTypeDef,
    UpdateReportGroupInputRequestTypeDef,
    UpdateReportGroupOutputTypeDef,
    UpdateWebhookInputRequestTypeDef,
    UpdateWebhookOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CodeBuildClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccountLimitExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    OAuthProviderException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class CodeBuildClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeBuildClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#exceptions)
        """

    def batch_delete_builds(
        self, **kwargs: Unpack[BatchDeleteBuildsInputRequestTypeDef]
    ) -> BatchDeleteBuildsOutputTypeDef:
        """
        Deletes one or more builds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_delete_builds)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#batch_delete_builds)
        """

    def batch_get_build_batches(
        self, **kwargs: Unpack[BatchGetBuildBatchesInputRequestTypeDef]
    ) -> BatchGetBuildBatchesOutputTypeDef:
        """
        Retrieves information about one or more batch builds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_build_batches)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#batch_get_build_batches)
        """

    def batch_get_builds(
        self, **kwargs: Unpack[BatchGetBuildsInputRequestTypeDef]
    ) -> BatchGetBuildsOutputTypeDef:
        """
        Gets information about one or more builds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_builds)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#batch_get_builds)
        """

    def batch_get_fleets(
        self, **kwargs: Unpack[BatchGetFleetsInputRequestTypeDef]
    ) -> BatchGetFleetsOutputTypeDef:
        """
        Gets information about one or more compute fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_fleets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#batch_get_fleets)
        """

    def batch_get_projects(
        self, **kwargs: Unpack[BatchGetProjectsInputRequestTypeDef]
    ) -> BatchGetProjectsOutputTypeDef:
        """
        Gets information about one or more build projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_projects)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#batch_get_projects)
        """

    def batch_get_report_groups(
        self, **kwargs: Unpack[BatchGetReportGroupsInputRequestTypeDef]
    ) -> BatchGetReportGroupsOutputTypeDef:
        """
        Returns an array of report groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_report_groups)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#batch_get_report_groups)
        """

    def batch_get_reports(
        self, **kwargs: Unpack[BatchGetReportsInputRequestTypeDef]
    ) -> BatchGetReportsOutputTypeDef:
        """
        Returns an array of reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_reports)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#batch_get_reports)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#close)
        """

    def create_fleet(
        self, **kwargs: Unpack[CreateFleetInputRequestTypeDef]
    ) -> CreateFleetOutputTypeDef:
        """
        Creates a compute fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.create_fleet)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#create_fleet)
        """

    def create_project(
        self, **kwargs: Unpack[CreateProjectInputRequestTypeDef]
    ) -> CreateProjectOutputTypeDef:
        """
        Creates a build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.create_project)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#create_project)
        """

    def create_report_group(
        self, **kwargs: Unpack[CreateReportGroupInputRequestTypeDef]
    ) -> CreateReportGroupOutputTypeDef:
        """
        Creates a report group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.create_report_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#create_report_group)
        """

    def create_webhook(
        self, **kwargs: Unpack[CreateWebhookInputRequestTypeDef]
    ) -> CreateWebhookOutputTypeDef:
        """
        For an existing CodeBuild build project that has its source code stored in a
        GitHub or Bitbucket repository, enables CodeBuild to start rebuilding the
        source code every time a code change is pushed to the
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.create_webhook)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#create_webhook)
        """

    def delete_build_batch(
        self, **kwargs: Unpack[DeleteBuildBatchInputRequestTypeDef]
    ) -> DeleteBuildBatchOutputTypeDef:
        """
        Deletes a batch build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_build_batch)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#delete_build_batch)
        """

    def delete_fleet(self, **kwargs: Unpack[DeleteFleetInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a compute fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_fleet)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#delete_fleet)
        """

    def delete_project(self, **kwargs: Unpack[DeleteProjectInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_project)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#delete_project)
        """

    def delete_report(self, **kwargs: Unpack[DeleteReportInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_report)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#delete_report)
        """

    def delete_report_group(
        self, **kwargs: Unpack[DeleteReportGroupInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a report group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_report_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#delete_report_group)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a resource policy that is identified by its resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_resource_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#delete_resource_policy)
        """

    def delete_source_credentials(
        self, **kwargs: Unpack[DeleteSourceCredentialsInputRequestTypeDef]
    ) -> DeleteSourceCredentialsOutputTypeDef:
        """
        Deletes a set of GitHub, GitHub Enterprise, or Bitbucket source credentials.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_source_credentials)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#delete_source_credentials)
        """

    def delete_webhook(self, **kwargs: Unpack[DeleteWebhookInputRequestTypeDef]) -> Dict[str, Any]:
        """
        For an existing CodeBuild build project that has its source code stored in a
        GitHub or Bitbucket repository, stops CodeBuild from rebuilding the source code
        every time a code change is pushed to the
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_webhook)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#delete_webhook)
        """

    def describe_code_coverages(
        self, **kwargs: Unpack[DescribeCodeCoveragesInputRequestTypeDef]
    ) -> DescribeCodeCoveragesOutputTypeDef:
        """
        Retrieves one or more code coverage reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.describe_code_coverages)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#describe_code_coverages)
        """

    def describe_test_cases(
        self, **kwargs: Unpack[DescribeTestCasesInputRequestTypeDef]
    ) -> DescribeTestCasesOutputTypeDef:
        """
        Returns a list of details about test cases for a report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.describe_test_cases)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#describe_test_cases)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#generate_presigned_url)
        """

    def get_report_group_trend(
        self, **kwargs: Unpack[GetReportGroupTrendInputRequestTypeDef]
    ) -> GetReportGroupTrendOutputTypeDef:
        """
        Analyzes and accumulates test report values for the specified test reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_report_group_trend)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_report_group_trend)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyInputRequestTypeDef]
    ) -> GetResourcePolicyOutputTypeDef:
        """
        Gets a resource policy that is identified by its resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_resource_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_resource_policy)
        """

    def import_source_credentials(
        self, **kwargs: Unpack[ImportSourceCredentialsInputRequestTypeDef]
    ) -> ImportSourceCredentialsOutputTypeDef:
        """
        Imports the source repository credentials for an CodeBuild project that has its
        source code stored in a GitHub, GitHub Enterprise, GitLab, GitLab Self Managed,
        or Bitbucket
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.import_source_credentials)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#import_source_credentials)
        """

    def invalidate_project_cache(
        self, **kwargs: Unpack[InvalidateProjectCacheInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Resets the cache for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.invalidate_project_cache)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#invalidate_project_cache)
        """

    def list_build_batches(
        self, **kwargs: Unpack[ListBuildBatchesInputRequestTypeDef]
    ) -> ListBuildBatchesOutputTypeDef:
        """
        Retrieves the identifiers of your build batches in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_build_batches)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_build_batches)
        """

    def list_build_batches_for_project(
        self, **kwargs: Unpack[ListBuildBatchesForProjectInputRequestTypeDef]
    ) -> ListBuildBatchesForProjectOutputTypeDef:
        """
        Retrieves the identifiers of the build batches for a specific project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_build_batches_for_project)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_build_batches_for_project)
        """

    def list_builds(
        self, **kwargs: Unpack[ListBuildsInputRequestTypeDef]
    ) -> ListBuildsOutputTypeDef:
        """
        Gets a list of build IDs, with each build ID representing a single build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_builds)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_builds)
        """

    def list_builds_for_project(
        self, **kwargs: Unpack[ListBuildsForProjectInputRequestTypeDef]
    ) -> ListBuildsForProjectOutputTypeDef:
        """
        Gets a list of build identifiers for the specified build project, with each
        build identifier representing a single
        build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_builds_for_project)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_builds_for_project)
        """

    def list_curated_environment_images(self) -> ListCuratedEnvironmentImagesOutputTypeDef:
        """
        Gets information about Docker images that are managed by CodeBuild.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_curated_environment_images)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_curated_environment_images)
        """

    def list_fleets(
        self, **kwargs: Unpack[ListFleetsInputRequestTypeDef]
    ) -> ListFleetsOutputTypeDef:
        """
        Gets a list of compute fleet names with each compute fleet name representing a
        single compute
        fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_fleets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_fleets)
        """

    def list_projects(
        self, **kwargs: Unpack[ListProjectsInputRequestTypeDef]
    ) -> ListProjectsOutputTypeDef:
        """
        Gets a list of build project names, with each build project name representing a
        single build
        project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_projects)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_projects)
        """

    def list_report_groups(
        self, **kwargs: Unpack[ListReportGroupsInputRequestTypeDef]
    ) -> ListReportGroupsOutputTypeDef:
        """
        Gets a list ARNs for the report groups in the current Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_report_groups)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_report_groups)
        """

    def list_reports(
        self, **kwargs: Unpack[ListReportsInputRequestTypeDef]
    ) -> ListReportsOutputTypeDef:
        """
        Returns a list of ARNs for the reports in the current Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_reports)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_reports)
        """

    def list_reports_for_report_group(
        self, **kwargs: Unpack[ListReportsForReportGroupInputRequestTypeDef]
    ) -> ListReportsForReportGroupOutputTypeDef:
        """
        Returns a list of ARNs for the reports that belong to a `ReportGroup`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_reports_for_report_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_reports_for_report_group)
        """

    def list_shared_projects(
        self, **kwargs: Unpack[ListSharedProjectsInputRequestTypeDef]
    ) -> ListSharedProjectsOutputTypeDef:
        """
        Gets a list of projects that are shared with other Amazon Web Services accounts
        or
        users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_shared_projects)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_shared_projects)
        """

    def list_shared_report_groups(
        self, **kwargs: Unpack[ListSharedReportGroupsInputRequestTypeDef]
    ) -> ListSharedReportGroupsOutputTypeDef:
        """
        Gets a list of report groups that are shared with other Amazon Web Services
        accounts or
        users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_shared_report_groups)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_shared_report_groups)
        """

    def list_source_credentials(self) -> ListSourceCredentialsOutputTypeDef:
        """
        Returns a list of `SourceCredentialsInfo` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_source_credentials)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#list_source_credentials)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyInputRequestTypeDef]
    ) -> PutResourcePolicyOutputTypeDef:
        """
        Stores a resource policy for the ARN of a `Project` or `ReportGroup` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.put_resource_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#put_resource_policy)
        """

    def retry_build(
        self, **kwargs: Unpack[RetryBuildInputRequestTypeDef]
    ) -> RetryBuildOutputTypeDef:
        """
        Restarts a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.retry_build)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#retry_build)
        """

    def retry_build_batch(
        self, **kwargs: Unpack[RetryBuildBatchInputRequestTypeDef]
    ) -> RetryBuildBatchOutputTypeDef:
        """
        Restarts a failed batch build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.retry_build_batch)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#retry_build_batch)
        """

    def start_build(
        self, **kwargs: Unpack[StartBuildInputRequestTypeDef]
    ) -> StartBuildOutputTypeDef:
        """
        Starts running a build with the settings defined in the project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.start_build)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#start_build)
        """

    def start_build_batch(
        self, **kwargs: Unpack[StartBuildBatchInputRequestTypeDef]
    ) -> StartBuildBatchOutputTypeDef:
        """
        Starts a batch build for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.start_build_batch)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#start_build_batch)
        """

    def stop_build(self, **kwargs: Unpack[StopBuildInputRequestTypeDef]) -> StopBuildOutputTypeDef:
        """
        Attempts to stop running a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.stop_build)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#stop_build)
        """

    def stop_build_batch(
        self, **kwargs: Unpack[StopBuildBatchInputRequestTypeDef]
    ) -> StopBuildBatchOutputTypeDef:
        """
        Stops a running batch build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.stop_build_batch)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#stop_build_batch)
        """

    def update_fleet(
        self, **kwargs: Unpack[UpdateFleetInputRequestTypeDef]
    ) -> UpdateFleetOutputTypeDef:
        """
        Updates a compute fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.update_fleet)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#update_fleet)
        """

    def update_project(
        self, **kwargs: Unpack[UpdateProjectInputRequestTypeDef]
    ) -> UpdateProjectOutputTypeDef:
        """
        Changes the settings of a build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.update_project)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#update_project)
        """

    def update_project_visibility(
        self, **kwargs: Unpack[UpdateProjectVisibilityInputRequestTypeDef]
    ) -> UpdateProjectVisibilityOutputTypeDef:
        """
        Changes the public visibility for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.update_project_visibility)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#update_project_visibility)
        """

    def update_report_group(
        self, **kwargs: Unpack[UpdateReportGroupInputRequestTypeDef]
    ) -> UpdateReportGroupOutputTypeDef:
        """
        Updates a report group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.update_report_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#update_report_group)
        """

    def update_webhook(
        self, **kwargs: Unpack[UpdateWebhookInputRequestTypeDef]
    ) -> UpdateWebhookOutputTypeDef:
        """
        Updates the webhook associated with an CodeBuild build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.update_webhook)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#update_webhook)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_code_coverages"]
    ) -> DescribeCodeCoveragesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_test_cases"]
    ) -> DescribeTestCasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_build_batches"]
    ) -> ListBuildBatchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_build_batches_for_project"]
    ) -> ListBuildBatchesForProjectPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_builds"]) -> ListBuildsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_builds_for_project"]
    ) -> ListBuildsForProjectPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_report_groups"]
    ) -> ListReportGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_reports"]) -> ListReportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reports_for_report_group"]
    ) -> ListReportsForReportGroupPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_shared_projects"]
    ) -> ListSharedProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_shared_report_groups"]
    ) -> ListSharedReportGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/client/#get_paginator)
        """
