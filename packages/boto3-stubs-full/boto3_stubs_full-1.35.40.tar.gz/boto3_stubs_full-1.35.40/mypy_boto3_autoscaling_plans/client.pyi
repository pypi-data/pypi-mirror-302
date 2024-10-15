"""
Type annotations for autoscaling-plans service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_autoscaling_plans.client import AutoScalingPlansClient

    session = Session()
    client: AutoScalingPlansClient = session.client("autoscaling-plans")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import DescribeScalingPlanResourcesPaginator, DescribeScalingPlansPaginator
from .type_defs import (
    CreateScalingPlanRequestRequestTypeDef,
    CreateScalingPlanResponseTypeDef,
    DeleteScalingPlanRequestRequestTypeDef,
    DescribeScalingPlanResourcesRequestRequestTypeDef,
    DescribeScalingPlanResourcesResponseTypeDef,
    DescribeScalingPlansRequestRequestTypeDef,
    DescribeScalingPlansResponseTypeDef,
    GetScalingPlanResourceForecastDataRequestRequestTypeDef,
    GetScalingPlanResourceForecastDataResponseTypeDef,
    UpdateScalingPlanRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AutoScalingPlansClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentUpdateException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ObjectNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class AutoScalingPlansClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AutoScalingPlansClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#close)
        """

    def create_scaling_plan(
        self, **kwargs: Unpack[CreateScalingPlanRequestRequestTypeDef]
    ) -> CreateScalingPlanResponseTypeDef:
        """
        Creates a scaling plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.create_scaling_plan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#create_scaling_plan)
        """

    def delete_scaling_plan(
        self, **kwargs: Unpack[DeleteScalingPlanRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified scaling plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.delete_scaling_plan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#delete_scaling_plan)
        """

    def describe_scaling_plan_resources(
        self, **kwargs: Unpack[DescribeScalingPlanResourcesRequestRequestTypeDef]
    ) -> DescribeScalingPlanResourcesResponseTypeDef:
        """
        Describes the scalable resources in the specified scaling plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.describe_scaling_plan_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#describe_scaling_plan_resources)
        """

    def describe_scaling_plans(
        self, **kwargs: Unpack[DescribeScalingPlansRequestRequestTypeDef]
    ) -> DescribeScalingPlansResponseTypeDef:
        """
        Describes one or more of your scaling plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.describe_scaling_plans)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#describe_scaling_plans)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#generate_presigned_url)
        """

    def get_scaling_plan_resource_forecast_data(
        self, **kwargs: Unpack[GetScalingPlanResourceForecastDataRequestRequestTypeDef]
    ) -> GetScalingPlanResourceForecastDataResponseTypeDef:
        """
        Retrieves the forecast data for a scalable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.get_scaling_plan_resource_forecast_data)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#get_scaling_plan_resource_forecast_data)
        """

    def update_scaling_plan(
        self, **kwargs: Unpack[UpdateScalingPlanRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the specified scaling plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.update_scaling_plan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#update_scaling_plan)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_plan_resources"]
    ) -> DescribeScalingPlanResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_plans"]
    ) -> DescribeScalingPlansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/client/#get_paginator)
        """
