"""
Type annotations for application-autoscaling service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_application_autoscaling.client import ApplicationAutoScalingClient

    session = Session()
    client: ApplicationAutoScalingClient = session.client("application-autoscaling")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeScalableTargetsPaginator,
    DescribeScalingActivitiesPaginator,
    DescribeScalingPoliciesPaginator,
    DescribeScheduledActionsPaginator,
)
from .type_defs import (
    DeleteScalingPolicyRequestRequestTypeDef,
    DeleteScheduledActionRequestRequestTypeDef,
    DeregisterScalableTargetRequestRequestTypeDef,
    DescribeScalableTargetsRequestRequestTypeDef,
    DescribeScalableTargetsResponseTypeDef,
    DescribeScalingActivitiesRequestRequestTypeDef,
    DescribeScalingActivitiesResponseTypeDef,
    DescribeScalingPoliciesRequestRequestTypeDef,
    DescribeScalingPoliciesResponseTypeDef,
    DescribeScheduledActionsRequestRequestTypeDef,
    DescribeScheduledActionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutScalingPolicyRequestRequestTypeDef,
    PutScalingPolicyResponseTypeDef,
    PutScheduledActionRequestRequestTypeDef,
    RegisterScalableTargetRequestRequestTypeDef,
    RegisterScalableTargetResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ApplicationAutoScalingClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentUpdateException: Type[BotocoreClientError]
    FailedResourceAccessException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ObjectNotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ApplicationAutoScalingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ApplicationAutoScalingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#close)
        """

    def delete_scaling_policy(
        self, **kwargs: Unpack[DeleteScalingPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified scaling policy for an Application Auto Scaling scalable
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.delete_scaling_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#delete_scaling_policy)
        """

    def delete_scheduled_action(
        self, **kwargs: Unpack[DeleteScheduledActionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified scheduled action for an Application Auto Scaling scalable
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.delete_scheduled_action)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#delete_scheduled_action)
        """

    def deregister_scalable_target(
        self, **kwargs: Unpack[DeregisterScalableTargetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregisters an Application Auto Scaling scalable target when you have finished
        using
        it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.deregister_scalable_target)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#deregister_scalable_target)
        """

    def describe_scalable_targets(
        self, **kwargs: Unpack[DescribeScalableTargetsRequestRequestTypeDef]
    ) -> DescribeScalableTargetsResponseTypeDef:
        """
        Gets information about the scalable targets in the specified namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.describe_scalable_targets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#describe_scalable_targets)
        """

    def describe_scaling_activities(
        self, **kwargs: Unpack[DescribeScalingActivitiesRequestRequestTypeDef]
    ) -> DescribeScalingActivitiesResponseTypeDef:
        """
        Provides descriptive information about the scaling activities in the specified
        namespace from the previous six
        weeks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.describe_scaling_activities)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#describe_scaling_activities)
        """

    def describe_scaling_policies(
        self, **kwargs: Unpack[DescribeScalingPoliciesRequestRequestTypeDef]
    ) -> DescribeScalingPoliciesResponseTypeDef:
        """
        Describes the Application Auto Scaling scaling policies for the specified
        service
        namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.describe_scaling_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#describe_scaling_policies)
        """

    def describe_scheduled_actions(
        self, **kwargs: Unpack[DescribeScheduledActionsRequestRequestTypeDef]
    ) -> DescribeScheduledActionsResponseTypeDef:
        """
        Describes the Application Auto Scaling scheduled actions for the specified
        service
        namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.describe_scheduled_actions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#describe_scheduled_actions)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#generate_presigned_url)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns all the tags on the specified Application Auto Scaling scalable target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#list_tags_for_resource)
        """

    def put_scaling_policy(
        self, **kwargs: Unpack[PutScalingPolicyRequestRequestTypeDef]
    ) -> PutScalingPolicyResponseTypeDef:
        """
        Creates or updates a scaling policy for an Application Auto Scaling scalable
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.put_scaling_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#put_scaling_policy)
        """

    def put_scheduled_action(
        self, **kwargs: Unpack[PutScheduledActionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates a scheduled action for an Application Auto Scaling scalable
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.put_scheduled_action)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#put_scheduled_action)
        """

    def register_scalable_target(
        self, **kwargs: Unpack[RegisterScalableTargetRequestRequestTypeDef]
    ) -> RegisterScalableTargetResponseTypeDef:
        """
        Registers or updates a scalable target, which is the resource that you want to
        scale.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.register_scalable_target)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#register_scalable_target)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or edits tags on an Application Auto Scaling scalable target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes tags from an Application Auto Scaling scalable target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scalable_targets"]
    ) -> DescribeScalableTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_activities"]
    ) -> DescribeScalingActivitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_policies"]
    ) -> DescribeScalingPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scheduled_actions"]
    ) -> DescribeScheduledActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_autoscaling/client/#get_paginator)
        """
