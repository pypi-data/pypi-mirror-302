"""
Type annotations for personalize service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_personalize.client import PersonalizeClient

    session = Session()
    client: PersonalizeClient = session.client("personalize")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListBatchInferenceJobsPaginator,
    ListBatchSegmentJobsPaginator,
    ListCampaignsPaginator,
    ListDatasetExportJobsPaginator,
    ListDatasetGroupsPaginator,
    ListDatasetImportJobsPaginator,
    ListDatasetsPaginator,
    ListEventTrackersPaginator,
    ListFiltersPaginator,
    ListMetricAttributionMetricsPaginator,
    ListMetricAttributionsPaginator,
    ListRecipesPaginator,
    ListRecommendersPaginator,
    ListSchemasPaginator,
    ListSolutionsPaginator,
    ListSolutionVersionsPaginator,
)
from .type_defs import (
    CreateBatchInferenceJobRequestRequestTypeDef,
    CreateBatchInferenceJobResponseTypeDef,
    CreateBatchSegmentJobRequestRequestTypeDef,
    CreateBatchSegmentJobResponseTypeDef,
    CreateCampaignRequestRequestTypeDef,
    CreateCampaignResponseTypeDef,
    CreateDataDeletionJobRequestRequestTypeDef,
    CreateDataDeletionJobResponseTypeDef,
    CreateDatasetExportJobRequestRequestTypeDef,
    CreateDatasetExportJobResponseTypeDef,
    CreateDatasetGroupRequestRequestTypeDef,
    CreateDatasetGroupResponseTypeDef,
    CreateDatasetImportJobRequestRequestTypeDef,
    CreateDatasetImportJobResponseTypeDef,
    CreateDatasetRequestRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateEventTrackerRequestRequestTypeDef,
    CreateEventTrackerResponseTypeDef,
    CreateFilterRequestRequestTypeDef,
    CreateFilterResponseTypeDef,
    CreateMetricAttributionRequestRequestTypeDef,
    CreateMetricAttributionResponseTypeDef,
    CreateRecommenderRequestRequestTypeDef,
    CreateRecommenderResponseTypeDef,
    CreateSchemaRequestRequestTypeDef,
    CreateSchemaResponseTypeDef,
    CreateSolutionRequestRequestTypeDef,
    CreateSolutionResponseTypeDef,
    CreateSolutionVersionRequestRequestTypeDef,
    CreateSolutionVersionResponseTypeDef,
    DeleteCampaignRequestRequestTypeDef,
    DeleteDatasetGroupRequestRequestTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteEventTrackerRequestRequestTypeDef,
    DeleteFilterRequestRequestTypeDef,
    DeleteMetricAttributionRequestRequestTypeDef,
    DeleteRecommenderRequestRequestTypeDef,
    DeleteSchemaRequestRequestTypeDef,
    DeleteSolutionRequestRequestTypeDef,
    DescribeAlgorithmRequestRequestTypeDef,
    DescribeAlgorithmResponseTypeDef,
    DescribeBatchInferenceJobRequestRequestTypeDef,
    DescribeBatchInferenceJobResponseTypeDef,
    DescribeBatchSegmentJobRequestRequestTypeDef,
    DescribeBatchSegmentJobResponseTypeDef,
    DescribeCampaignRequestRequestTypeDef,
    DescribeCampaignResponseTypeDef,
    DescribeDataDeletionJobRequestRequestTypeDef,
    DescribeDataDeletionJobResponseTypeDef,
    DescribeDatasetExportJobRequestRequestTypeDef,
    DescribeDatasetExportJobResponseTypeDef,
    DescribeDatasetGroupRequestRequestTypeDef,
    DescribeDatasetGroupResponseTypeDef,
    DescribeDatasetImportJobRequestRequestTypeDef,
    DescribeDatasetImportJobResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeEventTrackerRequestRequestTypeDef,
    DescribeEventTrackerResponseTypeDef,
    DescribeFeatureTransformationRequestRequestTypeDef,
    DescribeFeatureTransformationResponseTypeDef,
    DescribeFilterRequestRequestTypeDef,
    DescribeFilterResponseTypeDef,
    DescribeMetricAttributionRequestRequestTypeDef,
    DescribeMetricAttributionResponseTypeDef,
    DescribeRecipeRequestRequestTypeDef,
    DescribeRecipeResponseTypeDef,
    DescribeRecommenderRequestRequestTypeDef,
    DescribeRecommenderResponseTypeDef,
    DescribeSchemaRequestRequestTypeDef,
    DescribeSchemaResponseTypeDef,
    DescribeSolutionRequestRequestTypeDef,
    DescribeSolutionResponseTypeDef,
    DescribeSolutionVersionRequestRequestTypeDef,
    DescribeSolutionVersionResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetSolutionMetricsRequestRequestTypeDef,
    GetSolutionMetricsResponseTypeDef,
    ListBatchInferenceJobsRequestRequestTypeDef,
    ListBatchInferenceJobsResponseTypeDef,
    ListBatchSegmentJobsRequestRequestTypeDef,
    ListBatchSegmentJobsResponseTypeDef,
    ListCampaignsRequestRequestTypeDef,
    ListCampaignsResponseTypeDef,
    ListDataDeletionJobsRequestRequestTypeDef,
    ListDataDeletionJobsResponseTypeDef,
    ListDatasetExportJobsRequestRequestTypeDef,
    ListDatasetExportJobsResponseTypeDef,
    ListDatasetGroupsRequestRequestTypeDef,
    ListDatasetGroupsResponseTypeDef,
    ListDatasetImportJobsRequestRequestTypeDef,
    ListDatasetImportJobsResponseTypeDef,
    ListDatasetsRequestRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListEventTrackersRequestRequestTypeDef,
    ListEventTrackersResponseTypeDef,
    ListFiltersRequestRequestTypeDef,
    ListFiltersResponseTypeDef,
    ListMetricAttributionMetricsRequestRequestTypeDef,
    ListMetricAttributionMetricsResponseTypeDef,
    ListMetricAttributionsRequestRequestTypeDef,
    ListMetricAttributionsResponseTypeDef,
    ListRecipesRequestRequestTypeDef,
    ListRecipesResponseTypeDef,
    ListRecommendersRequestRequestTypeDef,
    ListRecommendersResponseTypeDef,
    ListSchemasRequestRequestTypeDef,
    ListSchemasResponseTypeDef,
    ListSolutionsRequestRequestTypeDef,
    ListSolutionsResponseTypeDef,
    ListSolutionVersionsRequestRequestTypeDef,
    ListSolutionVersionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartRecommenderRequestRequestTypeDef,
    StartRecommenderResponseTypeDef,
    StopRecommenderRequestRequestTypeDef,
    StopRecommenderResponseTypeDef,
    StopSolutionVersionCreationRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCampaignRequestRequestTypeDef,
    UpdateCampaignResponseTypeDef,
    UpdateDatasetRequestRequestTypeDef,
    UpdateDatasetResponseTypeDef,
    UpdateMetricAttributionRequestRequestTypeDef,
    UpdateMetricAttributionResponseTypeDef,
    UpdateRecommenderRequestRequestTypeDef,
    UpdateRecommenderResponseTypeDef,
    UpdateSolutionRequestRequestTypeDef,
    UpdateSolutionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("PersonalizeClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagKeysException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class PersonalizeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PersonalizeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#close)
        """

    def create_batch_inference_job(
        self, **kwargs: Unpack[CreateBatchInferenceJobRequestRequestTypeDef]
    ) -> CreateBatchInferenceJobResponseTypeDef:
        """
        Generates batch recommendations based on a list of items or users stored in
        Amazon S3 and exports the recommendations to an Amazon S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_batch_inference_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_batch_inference_job)
        """

    def create_batch_segment_job(
        self, **kwargs: Unpack[CreateBatchSegmentJobRequestRequestTypeDef]
    ) -> CreateBatchSegmentJobResponseTypeDef:
        """
        Creates a batch segment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_batch_segment_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_batch_segment_job)
        """

    def create_campaign(
        self, **kwargs: Unpack[CreateCampaignRequestRequestTypeDef]
    ) -> CreateCampaignResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_campaign)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_campaign)
        """

    def create_data_deletion_job(
        self, **kwargs: Unpack[CreateDataDeletionJobRequestRequestTypeDef]
    ) -> CreateDataDeletionJobResponseTypeDef:
        """
        Creates a batch job that deletes all references to specific users from an
        Amazon Personalize dataset group in
        batches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_data_deletion_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_data_deletion_job)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates an empty dataset and adds it to the specified dataset group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_dataset)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_dataset)
        """

    def create_dataset_export_job(
        self, **kwargs: Unpack[CreateDatasetExportJobRequestRequestTypeDef]
    ) -> CreateDatasetExportJobResponseTypeDef:
        """
        Creates a job that exports data from your dataset to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_dataset_export_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_dataset_export_job)
        """

    def create_dataset_group(
        self, **kwargs: Unpack[CreateDatasetGroupRequestRequestTypeDef]
    ) -> CreateDatasetGroupResponseTypeDef:
        """
        Creates an empty dataset group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_dataset_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_dataset_group)
        """

    def create_dataset_import_job(
        self, **kwargs: Unpack[CreateDatasetImportJobRequestRequestTypeDef]
    ) -> CreateDatasetImportJobResponseTypeDef:
        """
        Creates a job that imports training data from your data source (an Amazon S3
        bucket) to an Amazon Personalize
        dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_dataset_import_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_dataset_import_job)
        """

    def create_event_tracker(
        self, **kwargs: Unpack[CreateEventTrackerRequestRequestTypeDef]
    ) -> CreateEventTrackerResponseTypeDef:
        """
        Creates an event tracker that you use when adding event data to a specified
        dataset group using the
        [PutEvents](https://docs.aws.amazon.com/personalize/latest/dg/API_UBS_PutEvents.html)
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_event_tracker)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_event_tracker)
        """

    def create_filter(
        self, **kwargs: Unpack[CreateFilterRequestRequestTypeDef]
    ) -> CreateFilterResponseTypeDef:
        """
        Creates a recommendation filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_filter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_filter)
        """

    def create_metric_attribution(
        self, **kwargs: Unpack[CreateMetricAttributionRequestRequestTypeDef]
    ) -> CreateMetricAttributionResponseTypeDef:
        """
        Creates a metric attribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_metric_attribution)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_metric_attribution)
        """

    def create_recommender(
        self, **kwargs: Unpack[CreateRecommenderRequestRequestTypeDef]
    ) -> CreateRecommenderResponseTypeDef:
        """
        Creates a recommender with the recipe (a Domain dataset group use case) you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_recommender)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_recommender)
        """

    def create_schema(
        self, **kwargs: Unpack[CreateSchemaRequestRequestTypeDef]
    ) -> CreateSchemaResponseTypeDef:
        """
        Creates an Amazon Personalize schema from the specified schema string.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_schema)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_schema)
        """

    def create_solution(
        self, **kwargs: Unpack[CreateSolutionRequestRequestTypeDef]
    ) -> CreateSolutionResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_solution)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_solution)
        """

    def create_solution_version(
        self, **kwargs: Unpack[CreateSolutionVersionRequestRequestTypeDef]
    ) -> CreateSolutionVersionResponseTypeDef:
        """
        Trains or retrains an active solution in a Custom dataset group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_solution_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#create_solution_version)
        """

    def delete_campaign(
        self, **kwargs: Unpack[DeleteCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a campaign by deleting the solution deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.delete_campaign)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#delete_campaign)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.delete_dataset)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#delete_dataset)
        """

    def delete_dataset_group(
        self, **kwargs: Unpack[DeleteDatasetGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a dataset group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.delete_dataset_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#delete_dataset_group)
        """

    def delete_event_tracker(
        self, **kwargs: Unpack[DeleteEventTrackerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the event tracker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.delete_event_tracker)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#delete_event_tracker)
        """

    def delete_filter(
        self, **kwargs: Unpack[DeleteFilterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.delete_filter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#delete_filter)
        """

    def delete_metric_attribution(
        self, **kwargs: Unpack[DeleteMetricAttributionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a metric attribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.delete_metric_attribution)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#delete_metric_attribution)
        """

    def delete_recommender(
        self, **kwargs: Unpack[DeleteRecommenderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deactivates and removes a recommender.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.delete_recommender)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#delete_recommender)
        """

    def delete_schema(
        self, **kwargs: Unpack[DeleteSchemaRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.delete_schema)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#delete_schema)
        """

    def delete_solution(
        self, **kwargs: Unpack[DeleteSolutionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes all versions of a solution and the `Solution` object itself.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.delete_solution)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#delete_solution)
        """

    def describe_algorithm(
        self, **kwargs: Unpack[DescribeAlgorithmRequestRequestTypeDef]
    ) -> DescribeAlgorithmResponseTypeDef:
        """
        Describes the given algorithm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_algorithm)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_algorithm)
        """

    def describe_batch_inference_job(
        self, **kwargs: Unpack[DescribeBatchInferenceJobRequestRequestTypeDef]
    ) -> DescribeBatchInferenceJobResponseTypeDef:
        """
        Gets the properties of a batch inference job including name, Amazon Resource
        Name (ARN), status, input and output configurations, and the ARN of the
        solution version used to generate the
        recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_batch_inference_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_batch_inference_job)
        """

    def describe_batch_segment_job(
        self, **kwargs: Unpack[DescribeBatchSegmentJobRequestRequestTypeDef]
    ) -> DescribeBatchSegmentJobResponseTypeDef:
        """
        Gets the properties of a batch segment job including name, Amazon Resource Name
        (ARN), status, input and output configurations, and the ARN of the solution
        version used to generate
        segments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_batch_segment_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_batch_segment_job)
        """

    def describe_campaign(
        self, **kwargs: Unpack[DescribeCampaignRequestRequestTypeDef]
    ) -> DescribeCampaignResponseTypeDef:
        """
        Describes the given campaign, including its status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_campaign)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_campaign)
        """

    def describe_data_deletion_job(
        self, **kwargs: Unpack[DescribeDataDeletionJobRequestRequestTypeDef]
    ) -> DescribeDataDeletionJobResponseTypeDef:
        """
        Describes the data deletion job created by
        [CreateDataDeletionJob](https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDataDeletionJob.html),
        including the job
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_data_deletion_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_data_deletion_job)
        """

    def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Describes the given dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_dataset)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_dataset)
        """

    def describe_dataset_export_job(
        self, **kwargs: Unpack[DescribeDatasetExportJobRequestRequestTypeDef]
    ) -> DescribeDatasetExportJobResponseTypeDef:
        """
        Describes the dataset export job created by
        [CreateDatasetExportJob](https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDatasetExportJob.html),
        including the export job
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_dataset_export_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_dataset_export_job)
        """

    def describe_dataset_group(
        self, **kwargs: Unpack[DescribeDatasetGroupRequestRequestTypeDef]
    ) -> DescribeDatasetGroupResponseTypeDef:
        """
        Describes the given dataset group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_dataset_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_dataset_group)
        """

    def describe_dataset_import_job(
        self, **kwargs: Unpack[DescribeDatasetImportJobRequestRequestTypeDef]
    ) -> DescribeDatasetImportJobResponseTypeDef:
        """
        Describes the dataset import job created by
        [CreateDatasetImportJob](https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDatasetImportJob.html),
        including the import job
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_dataset_import_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_dataset_import_job)
        """

    def describe_event_tracker(
        self, **kwargs: Unpack[DescribeEventTrackerRequestRequestTypeDef]
    ) -> DescribeEventTrackerResponseTypeDef:
        """
        Describes an event tracker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_event_tracker)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_event_tracker)
        """

    def describe_feature_transformation(
        self, **kwargs: Unpack[DescribeFeatureTransformationRequestRequestTypeDef]
    ) -> DescribeFeatureTransformationResponseTypeDef:
        """
        Describes the given feature transformation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_feature_transformation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_feature_transformation)
        """

    def describe_filter(
        self, **kwargs: Unpack[DescribeFilterRequestRequestTypeDef]
    ) -> DescribeFilterResponseTypeDef:
        """
        Describes a filter's properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_filter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_filter)
        """

    def describe_metric_attribution(
        self, **kwargs: Unpack[DescribeMetricAttributionRequestRequestTypeDef]
    ) -> DescribeMetricAttributionResponseTypeDef:
        """
        Describes a metric attribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_metric_attribution)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_metric_attribution)
        """

    def describe_recipe(
        self, **kwargs: Unpack[DescribeRecipeRequestRequestTypeDef]
    ) -> DescribeRecipeResponseTypeDef:
        """
        Describes a recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_recipe)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_recipe)
        """

    def describe_recommender(
        self, **kwargs: Unpack[DescribeRecommenderRequestRequestTypeDef]
    ) -> DescribeRecommenderResponseTypeDef:
        """
        Describes the given recommender, including its status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_recommender)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_recommender)
        """

    def describe_schema(
        self, **kwargs: Unpack[DescribeSchemaRequestRequestTypeDef]
    ) -> DescribeSchemaResponseTypeDef:
        """
        Describes a schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_schema)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_schema)
        """

    def describe_solution(
        self, **kwargs: Unpack[DescribeSolutionRequestRequestTypeDef]
    ) -> DescribeSolutionResponseTypeDef:
        """
        Describes a solution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_solution)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_solution)
        """

    def describe_solution_version(
        self, **kwargs: Unpack[DescribeSolutionVersionRequestRequestTypeDef]
    ) -> DescribeSolutionVersionResponseTypeDef:
        """
        Describes a specific version of a solution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.describe_solution_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#describe_solution_version)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#generate_presigned_url)
        """

    def get_solution_metrics(
        self, **kwargs: Unpack[GetSolutionMetricsRequestRequestTypeDef]
    ) -> GetSolutionMetricsResponseTypeDef:
        """
        Gets the metrics for the specified solution version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_solution_metrics)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_solution_metrics)
        """

    def list_batch_inference_jobs(
        self, **kwargs: Unpack[ListBatchInferenceJobsRequestRequestTypeDef]
    ) -> ListBatchInferenceJobsResponseTypeDef:
        """
        Gets a list of the batch inference jobs that have been performed off of a
        solution
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_batch_inference_jobs)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_batch_inference_jobs)
        """

    def list_batch_segment_jobs(
        self, **kwargs: Unpack[ListBatchSegmentJobsRequestRequestTypeDef]
    ) -> ListBatchSegmentJobsResponseTypeDef:
        """
        Gets a list of the batch segment jobs that have been performed off of a
        solution version that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_batch_segment_jobs)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_batch_segment_jobs)
        """

    def list_campaigns(
        self, **kwargs: Unpack[ListCampaignsRequestRequestTypeDef]
    ) -> ListCampaignsResponseTypeDef:
        """
        Returns a list of campaigns that use the given solution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_campaigns)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_campaigns)
        """

    def list_data_deletion_jobs(
        self, **kwargs: Unpack[ListDataDeletionJobsRequestRequestTypeDef]
    ) -> ListDataDeletionJobsResponseTypeDef:
        """
        Returns a list of data deletion jobs for a dataset group ordered by creation
        time, with the most recent
        first.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_data_deletion_jobs)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_data_deletion_jobs)
        """

    def list_dataset_export_jobs(
        self, **kwargs: Unpack[ListDatasetExportJobsRequestRequestTypeDef]
    ) -> ListDatasetExportJobsResponseTypeDef:
        """
        Returns a list of dataset export jobs that use the given dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_dataset_export_jobs)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_dataset_export_jobs)
        """

    def list_dataset_groups(
        self, **kwargs: Unpack[ListDatasetGroupsRequestRequestTypeDef]
    ) -> ListDatasetGroupsResponseTypeDef:
        """
        Returns a list of dataset groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_dataset_groups)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_dataset_groups)
        """

    def list_dataset_import_jobs(
        self, **kwargs: Unpack[ListDatasetImportJobsRequestRequestTypeDef]
    ) -> ListDatasetImportJobsResponseTypeDef:
        """
        Returns a list of dataset import jobs that use the given dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_dataset_import_jobs)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_dataset_import_jobs)
        """

    def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Returns the list of datasets contained in the given dataset group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_datasets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_datasets)
        """

    def list_event_trackers(
        self, **kwargs: Unpack[ListEventTrackersRequestRequestTypeDef]
    ) -> ListEventTrackersResponseTypeDef:
        """
        Returns the list of event trackers associated with the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_event_trackers)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_event_trackers)
        """

    def list_filters(
        self, **kwargs: Unpack[ListFiltersRequestRequestTypeDef]
    ) -> ListFiltersResponseTypeDef:
        """
        Lists all filters that belong to a given dataset group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_filters)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_filters)
        """

    def list_metric_attribution_metrics(
        self, **kwargs: Unpack[ListMetricAttributionMetricsRequestRequestTypeDef]
    ) -> ListMetricAttributionMetricsResponseTypeDef:
        """
        Lists the metrics for the metric attribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_metric_attribution_metrics)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_metric_attribution_metrics)
        """

    def list_metric_attributions(
        self, **kwargs: Unpack[ListMetricAttributionsRequestRequestTypeDef]
    ) -> ListMetricAttributionsResponseTypeDef:
        """
        Lists metric attributions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_metric_attributions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_metric_attributions)
        """

    def list_recipes(
        self, **kwargs: Unpack[ListRecipesRequestRequestTypeDef]
    ) -> ListRecipesResponseTypeDef:
        """
        Returns a list of available recipes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_recipes)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_recipes)
        """

    def list_recommenders(
        self, **kwargs: Unpack[ListRecommendersRequestRequestTypeDef]
    ) -> ListRecommendersResponseTypeDef:
        """
        Returns a list of recommenders in a given Domain dataset group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_recommenders)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_recommenders)
        """

    def list_schemas(
        self, **kwargs: Unpack[ListSchemasRequestRequestTypeDef]
    ) -> ListSchemasResponseTypeDef:
        """
        Returns the list of schemas associated with the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_schemas)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_schemas)
        """

    def list_solution_versions(
        self, **kwargs: Unpack[ListSolutionVersionsRequestRequestTypeDef]
    ) -> ListSolutionVersionsResponseTypeDef:
        """
        Returns a list of solution versions for the given solution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_solution_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_solution_versions)
        """

    def list_solutions(
        self, **kwargs: Unpack[ListSolutionsRequestRequestTypeDef]
    ) -> ListSolutionsResponseTypeDef:
        """
        Returns a list of solutions in a given dataset group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_solutions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_solutions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Get a list of
        [tags](https://docs.aws.amazon.com/personalize/latest/dg/tagging-resources.html)
        attached to a
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#list_tags_for_resource)
        """

    def start_recommender(
        self, **kwargs: Unpack[StartRecommenderRequestRequestTypeDef]
    ) -> StartRecommenderResponseTypeDef:
        """
        Starts a recommender that is INACTIVE.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.start_recommender)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#start_recommender)
        """

    def stop_recommender(
        self, **kwargs: Unpack[StopRecommenderRequestRequestTypeDef]
    ) -> StopRecommenderResponseTypeDef:
        """
        Stops a recommender that is ACTIVE.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.stop_recommender)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#stop_recommender)
        """

    def stop_solution_version_creation(
        self, **kwargs: Unpack[StopSolutionVersionCreationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops creating a solution version that is in a state of CREATE_PENDING or
        CREATE
        IN_PROGRESS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.stop_solution_version_creation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#stop_solution_version_creation)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Add a list of tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags that are attached to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#untag_resource)
        """

    def update_campaign(
        self, **kwargs: Unpack[UpdateCampaignRequestRequestTypeDef]
    ) -> UpdateCampaignResponseTypeDef:
        """
        Updates a campaign to deploy a retrained solution version with an existing
        campaign, change your campaign's `minProvisionedTPS`, or modify your campaign's
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.update_campaign)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#update_campaign)
        """

    def update_dataset(
        self, **kwargs: Unpack[UpdateDatasetRequestRequestTypeDef]
    ) -> UpdateDatasetResponseTypeDef:
        """
        Update a dataset to replace its schema with a new or existing one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.update_dataset)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#update_dataset)
        """

    def update_metric_attribution(
        self, **kwargs: Unpack[UpdateMetricAttributionRequestRequestTypeDef]
    ) -> UpdateMetricAttributionResponseTypeDef:
        """
        Updates a metric attribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.update_metric_attribution)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#update_metric_attribution)
        """

    def update_recommender(
        self, **kwargs: Unpack[UpdateRecommenderRequestRequestTypeDef]
    ) -> UpdateRecommenderResponseTypeDef:
        """
        Updates the recommender to modify the recommender configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.update_recommender)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#update_recommender)
        """

    def update_solution(
        self, **kwargs: Unpack[UpdateSolutionRequestRequestTypeDef]
    ) -> UpdateSolutionResponseTypeDef:
        """
        Updates an Amazon Personalize solution to use a different automatic training
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.update_solution)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#update_solution)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_batch_inference_jobs"]
    ) -> ListBatchInferenceJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_batch_segment_jobs"]
    ) -> ListBatchSegmentJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_campaigns"]) -> ListCampaignsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_export_jobs"]
    ) -> ListDatasetExportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_groups"]
    ) -> ListDatasetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_import_jobs"]
    ) -> ListDatasetImportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_trackers"]
    ) -> ListEventTrackersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_filters"]) -> ListFiltersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_metric_attribution_metrics"]
    ) -> ListMetricAttributionMetricsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_metric_attributions"]
    ) -> ListMetricAttributionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_recipes"]) -> ListRecipesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recommenders"]
    ) -> ListRecommendersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schemas"]) -> ListSchemasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_solution_versions"]
    ) -> ListSolutionVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_solutions"]) -> ListSolutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize/client/#get_paginator)
        """
