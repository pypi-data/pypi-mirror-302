"""
Type annotations for ecr service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ecr.client import ECRClient
    from mypy_boto3_ecr.paginator import (
        DescribeImageScanFindingsPaginator,
        DescribeImagesPaginator,
        DescribePullThroughCacheRulesPaginator,
        DescribeRepositoriesPaginator,
        DescribeRepositoryCreationTemplatesPaginator,
        GetLifecyclePolicyPreviewPaginator,
        ListImagesPaginator,
    )

    session = Session()
    client: ECRClient = session.client("ecr")

    describe_image_scan_findings_paginator: DescribeImageScanFindingsPaginator = client.get_paginator("describe_image_scan_findings")
    describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
    describe_pull_through_cache_rules_paginator: DescribePullThroughCacheRulesPaginator = client.get_paginator("describe_pull_through_cache_rules")
    describe_repositories_paginator: DescribeRepositoriesPaginator = client.get_paginator("describe_repositories")
    describe_repository_creation_templates_paginator: DescribeRepositoryCreationTemplatesPaginator = client.get_paginator("describe_repository_creation_templates")
    get_lifecycle_policy_preview_paginator: GetLifecyclePolicyPreviewPaginator = client.get_paginator("get_lifecycle_policy_preview")
    list_images_paginator: ListImagesPaginator = client.get_paginator("list_images")
    ```
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef,
    DescribeImageScanFindingsResponseTypeDef,
    DescribeImagesRequestDescribeImagesPaginateTypeDef,
    DescribeImagesResponseTypeDef,
    DescribePullThroughCacheRulesRequestDescribePullThroughCacheRulesPaginateTypeDef,
    DescribePullThroughCacheRulesResponseTypeDef,
    DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef,
    DescribeRepositoriesResponseTypeDef,
    DescribeRepositoryCreationTemplatesRequestDescribeRepositoryCreationTemplatesPaginateTypeDef,
    DescribeRepositoryCreationTemplatesResponseTypeDef,
    GetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef,
    GetLifecyclePolicyPreviewResponseTypeDef,
    ListImagesRequestListImagesPaginateTypeDef,
    ListImagesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeImageScanFindingsPaginator",
    "DescribeImagesPaginator",
    "DescribePullThroughCacheRulesPaginator",
    "DescribeRepositoriesPaginator",
    "DescribeRepositoryCreationTemplatesPaginator",
    "GetLifecyclePolicyPreviewPaginator",
    "ListImagesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeImageScanFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribeImageScanFindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describeimagescanfindingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef],
    ) -> _PageIterator[DescribeImageScanFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribeImageScanFindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describeimagescanfindingspaginator)
        """

class DescribeImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribeImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describeimagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeImagesRequestDescribeImagesPaginateTypeDef]
    ) -> _PageIterator[DescribeImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribeImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describeimagespaginator)
        """

class DescribePullThroughCacheRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribePullThroughCacheRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describepullthroughcacherulespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribePullThroughCacheRulesRequestDescribePullThroughCacheRulesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribePullThroughCacheRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribePullThroughCacheRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describepullthroughcacherulespaginator)
        """

class DescribeRepositoriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribeRepositories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describerepositoriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef]
    ) -> _PageIterator[DescribeRepositoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribeRepositories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describerepositoriespaginator)
        """

class DescribeRepositoryCreationTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribeRepositoryCreationTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describerepositorycreationtemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRepositoryCreationTemplatesRequestDescribeRepositoryCreationTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRepositoryCreationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.DescribeRepositoryCreationTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#describerepositorycreationtemplatespaginator)
        """

class GetLifecyclePolicyPreviewPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.GetLifecyclePolicyPreview)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#getlifecyclepolicypreviewpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[GetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef],
    ) -> _PageIterator[GetLifecyclePolicyPreviewResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.GetLifecyclePolicyPreview.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#getlifecyclepolicypreviewpaginator)
        """

class ListImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.ListImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#listimagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListImagesRequestListImagesPaginateTypeDef]
    ) -> _PageIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Paginator.ListImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators/#listimagespaginator)
        """
