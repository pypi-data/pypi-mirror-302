"""
Type annotations for codeartifact service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codeartifact.client import CodeArtifactClient

    session = Session()
    client: CodeArtifactClient = session.client("codeartifact")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAllowedRepositoriesForGroupPaginator,
    ListAssociatedPackagesPaginator,
    ListDomainsPaginator,
    ListPackageGroupsPaginator,
    ListPackagesPaginator,
    ListPackageVersionAssetsPaginator,
    ListPackageVersionsPaginator,
    ListRepositoriesInDomainPaginator,
    ListRepositoriesPaginator,
    ListSubPackageGroupsPaginator,
)
from .type_defs import (
    AssociateExternalConnectionRequestRequestTypeDef,
    AssociateExternalConnectionResultTypeDef,
    CopyPackageVersionsRequestRequestTypeDef,
    CopyPackageVersionsResultTypeDef,
    CreateDomainRequestRequestTypeDef,
    CreateDomainResultTypeDef,
    CreatePackageGroupRequestRequestTypeDef,
    CreatePackageGroupResultTypeDef,
    CreateRepositoryRequestRequestTypeDef,
    CreateRepositoryResultTypeDef,
    DeleteDomainPermissionsPolicyRequestRequestTypeDef,
    DeleteDomainPermissionsPolicyResultTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DeleteDomainResultTypeDef,
    DeletePackageGroupRequestRequestTypeDef,
    DeletePackageGroupResultTypeDef,
    DeletePackageRequestRequestTypeDef,
    DeletePackageResultTypeDef,
    DeletePackageVersionsRequestRequestTypeDef,
    DeletePackageVersionsResultTypeDef,
    DeleteRepositoryPermissionsPolicyRequestRequestTypeDef,
    DeleteRepositoryPermissionsPolicyResultTypeDef,
    DeleteRepositoryRequestRequestTypeDef,
    DeleteRepositoryResultTypeDef,
    DescribeDomainRequestRequestTypeDef,
    DescribeDomainResultTypeDef,
    DescribePackageGroupRequestRequestTypeDef,
    DescribePackageGroupResultTypeDef,
    DescribePackageRequestRequestTypeDef,
    DescribePackageResultTypeDef,
    DescribePackageVersionRequestRequestTypeDef,
    DescribePackageVersionResultTypeDef,
    DescribeRepositoryRequestRequestTypeDef,
    DescribeRepositoryResultTypeDef,
    DisassociateExternalConnectionRequestRequestTypeDef,
    DisassociateExternalConnectionResultTypeDef,
    DisposePackageVersionsRequestRequestTypeDef,
    DisposePackageVersionsResultTypeDef,
    GetAssociatedPackageGroupRequestRequestTypeDef,
    GetAssociatedPackageGroupResultTypeDef,
    GetAuthorizationTokenRequestRequestTypeDef,
    GetAuthorizationTokenResultTypeDef,
    GetDomainPermissionsPolicyRequestRequestTypeDef,
    GetDomainPermissionsPolicyResultTypeDef,
    GetPackageVersionAssetRequestRequestTypeDef,
    GetPackageVersionAssetResultTypeDef,
    GetPackageVersionReadmeRequestRequestTypeDef,
    GetPackageVersionReadmeResultTypeDef,
    GetRepositoryEndpointRequestRequestTypeDef,
    GetRepositoryEndpointResultTypeDef,
    GetRepositoryPermissionsPolicyRequestRequestTypeDef,
    GetRepositoryPermissionsPolicyResultTypeDef,
    ListAllowedRepositoriesForGroupRequestRequestTypeDef,
    ListAllowedRepositoriesForGroupResultTypeDef,
    ListAssociatedPackagesRequestRequestTypeDef,
    ListAssociatedPackagesResultTypeDef,
    ListDomainsRequestRequestTypeDef,
    ListDomainsResultTypeDef,
    ListPackageGroupsRequestRequestTypeDef,
    ListPackageGroupsResultTypeDef,
    ListPackagesRequestRequestTypeDef,
    ListPackagesResultTypeDef,
    ListPackageVersionAssetsRequestRequestTypeDef,
    ListPackageVersionAssetsResultTypeDef,
    ListPackageVersionDependenciesRequestRequestTypeDef,
    ListPackageVersionDependenciesResultTypeDef,
    ListPackageVersionsRequestRequestTypeDef,
    ListPackageVersionsResultTypeDef,
    ListRepositoriesInDomainRequestRequestTypeDef,
    ListRepositoriesInDomainResultTypeDef,
    ListRepositoriesRequestRequestTypeDef,
    ListRepositoriesResultTypeDef,
    ListSubPackageGroupsRequestRequestTypeDef,
    ListSubPackageGroupsResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResultTypeDef,
    PublishPackageVersionRequestRequestTypeDef,
    PublishPackageVersionResultTypeDef,
    PutDomainPermissionsPolicyRequestRequestTypeDef,
    PutDomainPermissionsPolicyResultTypeDef,
    PutPackageOriginConfigurationRequestRequestTypeDef,
    PutPackageOriginConfigurationResultTypeDef,
    PutRepositoryPermissionsPolicyRequestRequestTypeDef,
    PutRepositoryPermissionsPolicyResultTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdatePackageGroupOriginConfigurationRequestRequestTypeDef,
    UpdatePackageGroupOriginConfigurationResultTypeDef,
    UpdatePackageGroupRequestRequestTypeDef,
    UpdatePackageGroupResultTypeDef,
    UpdatePackageVersionsStatusRequestRequestTypeDef,
    UpdatePackageVersionsStatusResultTypeDef,
    UpdateRepositoryRequestRequestTypeDef,
    UpdateRepositoryResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CodeArtifactClient",)

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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CodeArtifactClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeArtifactClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#exceptions)
        """

    def associate_external_connection(
        self, **kwargs: Unpack[AssociateExternalConnectionRequestRequestTypeDef]
    ) -> AssociateExternalConnectionResultTypeDef:
        """
        Adds an existing external connection to a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.associate_external_connection)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#associate_external_connection)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#close)
        """

    def copy_package_versions(
        self, **kwargs: Unpack[CopyPackageVersionsRequestRequestTypeDef]
    ) -> CopyPackageVersionsResultTypeDef:
        """
        Copies package versions from one repository to another repository in the same
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.copy_package_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#copy_package_versions)
        """

    def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestRequestTypeDef]
    ) -> CreateDomainResultTypeDef:
        """
        Creates a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.create_domain)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#create_domain)
        """

    def create_package_group(
        self, **kwargs: Unpack[CreatePackageGroupRequestRequestTypeDef]
    ) -> CreatePackageGroupResultTypeDef:
        """
        Creates a package group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.create_package_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#create_package_group)
        """

    def create_repository(
        self, **kwargs: Unpack[CreateRepositoryRequestRequestTypeDef]
    ) -> CreateRepositoryResultTypeDef:
        """
        Creates a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.create_repository)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#create_repository)
        """

    def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]
    ) -> DeleteDomainResultTypeDef:
        """
        Deletes a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.delete_domain)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#delete_domain)
        """

    def delete_domain_permissions_policy(
        self, **kwargs: Unpack[DeleteDomainPermissionsPolicyRequestRequestTypeDef]
    ) -> DeleteDomainPermissionsPolicyResultTypeDef:
        """
        Deletes the resource policy set on a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.delete_domain_permissions_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#delete_domain_permissions_policy)
        """

    def delete_package(
        self, **kwargs: Unpack[DeletePackageRequestRequestTypeDef]
    ) -> DeletePackageResultTypeDef:
        """
        Deletes a package and all associated package versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.delete_package)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#delete_package)
        """

    def delete_package_group(
        self, **kwargs: Unpack[DeletePackageGroupRequestRequestTypeDef]
    ) -> DeletePackageGroupResultTypeDef:
        """
        Deletes a package group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.delete_package_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#delete_package_group)
        """

    def delete_package_versions(
        self, **kwargs: Unpack[DeletePackageVersionsRequestRequestTypeDef]
    ) -> DeletePackageVersionsResultTypeDef:
        """
        Deletes one or more versions of a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.delete_package_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#delete_package_versions)
        """

    def delete_repository(
        self, **kwargs: Unpack[DeleteRepositoryRequestRequestTypeDef]
    ) -> DeleteRepositoryResultTypeDef:
        """
        Deletes a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.delete_repository)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#delete_repository)
        """

    def delete_repository_permissions_policy(
        self, **kwargs: Unpack[DeleteRepositoryPermissionsPolicyRequestRequestTypeDef]
    ) -> DeleteRepositoryPermissionsPolicyResultTypeDef:
        """
        Deletes the resource policy that is set on a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.delete_repository_permissions_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#delete_repository_permissions_policy)
        """

    def describe_domain(
        self, **kwargs: Unpack[DescribeDomainRequestRequestTypeDef]
    ) -> DescribeDomainResultTypeDef:
        """
        Returns a
        [DomainDescription](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_DomainDescription.html)
        object that contains information about the requested
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.describe_domain)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#describe_domain)
        """

    def describe_package(
        self, **kwargs: Unpack[DescribePackageRequestRequestTypeDef]
    ) -> DescribePackageResultTypeDef:
        """
        Returns a
        [PackageDescription](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_PackageDescription.html)
        object that contains information about the requested
        package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.describe_package)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#describe_package)
        """

    def describe_package_group(
        self, **kwargs: Unpack[DescribePackageGroupRequestRequestTypeDef]
    ) -> DescribePackageGroupResultTypeDef:
        """
        Returns a
        [PackageGroupDescription](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_PackageGroupDescription.html)
        object that contains information about the requested package
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.describe_package_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#describe_package_group)
        """

    def describe_package_version(
        self, **kwargs: Unpack[DescribePackageVersionRequestRequestTypeDef]
    ) -> DescribePackageVersionResultTypeDef:
        """
        Returns a
        [PackageVersionDescription](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_PackageVersionDescription.html)
        object that contains information about the requested package
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.describe_package_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#describe_package_version)
        """

    def describe_repository(
        self, **kwargs: Unpack[DescribeRepositoryRequestRequestTypeDef]
    ) -> DescribeRepositoryResultTypeDef:
        """
        Returns a `RepositoryDescription` object that contains detailed information
        about the requested
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.describe_repository)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#describe_repository)
        """

    def disassociate_external_connection(
        self, **kwargs: Unpack[DisassociateExternalConnectionRequestRequestTypeDef]
    ) -> DisassociateExternalConnectionResultTypeDef:
        """
        Removes an existing external connection from a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.disassociate_external_connection)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#disassociate_external_connection)
        """

    def dispose_package_versions(
        self, **kwargs: Unpack[DisposePackageVersionsRequestRequestTypeDef]
    ) -> DisposePackageVersionsResultTypeDef:
        """
        Deletes the assets in package versions and sets the package versions' status to
        `Disposed`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.dispose_package_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#dispose_package_versions)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#generate_presigned_url)
        """

    def get_associated_package_group(
        self, **kwargs: Unpack[GetAssociatedPackageGroupRequestRequestTypeDef]
    ) -> GetAssociatedPackageGroupResultTypeDef:
        """
        Returns the most closely associated package group to the specified package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_associated_package_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_associated_package_group)
        """

    def get_authorization_token(
        self, **kwargs: Unpack[GetAuthorizationTokenRequestRequestTypeDef]
    ) -> GetAuthorizationTokenResultTypeDef:
        """
        Generates a temporary authorization token for accessing repositories in the
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_authorization_token)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_authorization_token)
        """

    def get_domain_permissions_policy(
        self, **kwargs: Unpack[GetDomainPermissionsPolicyRequestRequestTypeDef]
    ) -> GetDomainPermissionsPolicyResultTypeDef:
        """
        Returns the resource policy attached to the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_domain_permissions_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_domain_permissions_policy)
        """

    def get_package_version_asset(
        self, **kwargs: Unpack[GetPackageVersionAssetRequestRequestTypeDef]
    ) -> GetPackageVersionAssetResultTypeDef:
        """
        Returns an asset (or file) that is in a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_package_version_asset)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_package_version_asset)
        """

    def get_package_version_readme(
        self, **kwargs: Unpack[GetPackageVersionReadmeRequestRequestTypeDef]
    ) -> GetPackageVersionReadmeResultTypeDef:
        """
        Gets the readme file or descriptive text for a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_package_version_readme)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_package_version_readme)
        """

    def get_repository_endpoint(
        self, **kwargs: Unpack[GetRepositoryEndpointRequestRequestTypeDef]
    ) -> GetRepositoryEndpointResultTypeDef:
        """
        Returns the endpoint of a repository for a specific package format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_repository_endpoint)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_repository_endpoint)
        """

    def get_repository_permissions_policy(
        self, **kwargs: Unpack[GetRepositoryPermissionsPolicyRequestRequestTypeDef]
    ) -> GetRepositoryPermissionsPolicyResultTypeDef:
        """
        Returns the resource policy that is set on a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_repository_permissions_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_repository_permissions_policy)
        """

    def list_allowed_repositories_for_group(
        self, **kwargs: Unpack[ListAllowedRepositoriesForGroupRequestRequestTypeDef]
    ) -> ListAllowedRepositoriesForGroupResultTypeDef:
        """
        Lists the repositories in the added repositories list of the specified
        restriction type for a package
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_allowed_repositories_for_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_allowed_repositories_for_group)
        """

    def list_associated_packages(
        self, **kwargs: Unpack[ListAssociatedPackagesRequestRequestTypeDef]
    ) -> ListAssociatedPackagesResultTypeDef:
        """
        Returns a list of packages associated with the requested package group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_associated_packages)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_associated_packages)
        """

    def list_domains(
        self, **kwargs: Unpack[ListDomainsRequestRequestTypeDef]
    ) -> ListDomainsResultTypeDef:
        """
        Returns a list of
        [DomainSummary](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_PackageVersionDescription.html)
        objects for all domains owned by the Amazon Web Services account that makes
        this
        call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_domains)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_domains)
        """

    def list_package_groups(
        self, **kwargs: Unpack[ListPackageGroupsRequestRequestTypeDef]
    ) -> ListPackageGroupsResultTypeDef:
        """
        Returns a list of package groups in the requested domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_package_groups)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_package_groups)
        """

    def list_package_version_assets(
        self, **kwargs: Unpack[ListPackageVersionAssetsRequestRequestTypeDef]
    ) -> ListPackageVersionAssetsResultTypeDef:
        """
        Returns a list of
        [AssetSummary](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_AssetSummary.html)
        objects for assets in a package
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_package_version_assets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_package_version_assets)
        """

    def list_package_version_dependencies(
        self, **kwargs: Unpack[ListPackageVersionDependenciesRequestRequestTypeDef]
    ) -> ListPackageVersionDependenciesResultTypeDef:
        """
        Returns the direct dependencies for a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_package_version_dependencies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_package_version_dependencies)
        """

    def list_package_versions(
        self, **kwargs: Unpack[ListPackageVersionsRequestRequestTypeDef]
    ) -> ListPackageVersionsResultTypeDef:
        """
        Returns a list of
        [PackageVersionSummary](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_PackageVersionSummary.html)
        objects for package versions in a repository that match the request
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_package_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_package_versions)
        """

    def list_packages(
        self, **kwargs: Unpack[ListPackagesRequestRequestTypeDef]
    ) -> ListPackagesResultTypeDef:
        """
        Returns a list of
        [PackageSummary](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_PackageSummary.html)
        objects for packages in a repository that match the request
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_packages)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_packages)
        """

    def list_repositories(
        self, **kwargs: Unpack[ListRepositoriesRequestRequestTypeDef]
    ) -> ListRepositoriesResultTypeDef:
        """
        Returns a list of
        [RepositorySummary](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_RepositorySummary.html)
        objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_repositories)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_repositories)
        """

    def list_repositories_in_domain(
        self, **kwargs: Unpack[ListRepositoriesInDomainRequestRequestTypeDef]
    ) -> ListRepositoriesInDomainResultTypeDef:
        """
        Returns a list of
        [RepositorySummary](https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_RepositorySummary.html)
        objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_repositories_in_domain)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_repositories_in_domain)
        """

    def list_sub_package_groups(
        self, **kwargs: Unpack[ListSubPackageGroupsRequestRequestTypeDef]
    ) -> ListSubPackageGroupsResultTypeDef:
        """
        Returns a list of direct children of the specified package group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_sub_package_groups)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_sub_package_groups)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResultTypeDef:
        """
        Gets information about Amazon Web Services tags for a specified Amazon Resource
        Name (ARN) in
        CodeArtifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#list_tags_for_resource)
        """

    def publish_package_version(
        self, **kwargs: Unpack[PublishPackageVersionRequestRequestTypeDef]
    ) -> PublishPackageVersionResultTypeDef:
        """
        Creates a new package version containing one or more assets (or files).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.publish_package_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#publish_package_version)
        """

    def put_domain_permissions_policy(
        self, **kwargs: Unpack[PutDomainPermissionsPolicyRequestRequestTypeDef]
    ) -> PutDomainPermissionsPolicyResultTypeDef:
        """
        Sets a resource policy on a domain that specifies permissions to access it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.put_domain_permissions_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#put_domain_permissions_policy)
        """

    def put_package_origin_configuration(
        self, **kwargs: Unpack[PutPackageOriginConfigurationRequestRequestTypeDef]
    ) -> PutPackageOriginConfigurationResultTypeDef:
        """
        Sets the package origin configuration for a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.put_package_origin_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#put_package_origin_configuration)
        """

    def put_repository_permissions_policy(
        self, **kwargs: Unpack[PutRepositoryPermissionsPolicyRequestRequestTypeDef]
    ) -> PutRepositoryPermissionsPolicyResultTypeDef:
        """
        Sets the resource policy on a repository that specifies permissions to access
        it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.put_repository_permissions_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#put_repository_permissions_policy)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or updates tags for a resource in CodeArtifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource in CodeArtifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#untag_resource)
        """

    def update_package_group(
        self, **kwargs: Unpack[UpdatePackageGroupRequestRequestTypeDef]
    ) -> UpdatePackageGroupResultTypeDef:
        """
        Updates a package group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.update_package_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#update_package_group)
        """

    def update_package_group_origin_configuration(
        self, **kwargs: Unpack[UpdatePackageGroupOriginConfigurationRequestRequestTypeDef]
    ) -> UpdatePackageGroupOriginConfigurationResultTypeDef:
        """
        Updates the package origin configuration for a package group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.update_package_group_origin_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#update_package_group_origin_configuration)
        """

    def update_package_versions_status(
        self, **kwargs: Unpack[UpdatePackageVersionsStatusRequestRequestTypeDef]
    ) -> UpdatePackageVersionsStatusResultTypeDef:
        """
        Updates the status of one or more versions of a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.update_package_versions_status)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#update_package_versions_status)
        """

    def update_repository(
        self, **kwargs: Unpack[UpdateRepositoryRequestRequestTypeDef]
    ) -> UpdateRepositoryResultTypeDef:
        """
        Update the properties of a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.update_repository)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#update_repository)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_allowed_repositories_for_group"]
    ) -> ListAllowedRepositoriesForGroupPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associated_packages"]
    ) -> ListAssociatedPackagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_package_groups"]
    ) -> ListPackageGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_package_version_assets"]
    ) -> ListPackageVersionAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_package_versions"]
    ) -> ListPackageVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_packages"]) -> ListPackagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories_in_domain"]
    ) -> ListRepositoriesInDomainPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sub_package_groups"]
    ) -> ListSubPackageGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client/#get_paginator)
        """
