"""
Type annotations for entityresolution service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_entityresolution.client import EntityResolutionClient

    session = Session()
    client: EntityResolutionClient = session.client("entityresolution")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListIdMappingJobsPaginator,
    ListIdMappingWorkflowsPaginator,
    ListIdNamespacesPaginator,
    ListMatchingJobsPaginator,
    ListMatchingWorkflowsPaginator,
    ListProviderServicesPaginator,
    ListSchemaMappingsPaginator,
)
from .type_defs import (
    AddPolicyStatementInputRequestTypeDef,
    AddPolicyStatementOutputTypeDef,
    BatchDeleteUniqueIdInputRequestTypeDef,
    BatchDeleteUniqueIdOutputTypeDef,
    CreateIdMappingWorkflowInputRequestTypeDef,
    CreateIdMappingWorkflowOutputTypeDef,
    CreateIdNamespaceInputRequestTypeDef,
    CreateIdNamespaceOutputTypeDef,
    CreateMatchingWorkflowInputRequestTypeDef,
    CreateMatchingWorkflowOutputTypeDef,
    CreateSchemaMappingInputRequestTypeDef,
    CreateSchemaMappingOutputTypeDef,
    DeleteIdMappingWorkflowInputRequestTypeDef,
    DeleteIdMappingWorkflowOutputTypeDef,
    DeleteIdNamespaceInputRequestTypeDef,
    DeleteIdNamespaceOutputTypeDef,
    DeleteMatchingWorkflowInputRequestTypeDef,
    DeleteMatchingWorkflowOutputTypeDef,
    DeletePolicyStatementInputRequestTypeDef,
    DeletePolicyStatementOutputTypeDef,
    DeleteSchemaMappingInputRequestTypeDef,
    DeleteSchemaMappingOutputTypeDef,
    GetIdMappingJobInputRequestTypeDef,
    GetIdMappingJobOutputTypeDef,
    GetIdMappingWorkflowInputRequestTypeDef,
    GetIdMappingWorkflowOutputTypeDef,
    GetIdNamespaceInputRequestTypeDef,
    GetIdNamespaceOutputTypeDef,
    GetMatchIdInputRequestTypeDef,
    GetMatchIdOutputTypeDef,
    GetMatchingJobInputRequestTypeDef,
    GetMatchingJobOutputTypeDef,
    GetMatchingWorkflowInputRequestTypeDef,
    GetMatchingWorkflowOutputTypeDef,
    GetPolicyInputRequestTypeDef,
    GetPolicyOutputTypeDef,
    GetProviderServiceInputRequestTypeDef,
    GetProviderServiceOutputTypeDef,
    GetSchemaMappingInputRequestTypeDef,
    GetSchemaMappingOutputTypeDef,
    ListIdMappingJobsInputRequestTypeDef,
    ListIdMappingJobsOutputTypeDef,
    ListIdMappingWorkflowsInputRequestTypeDef,
    ListIdMappingWorkflowsOutputTypeDef,
    ListIdNamespacesInputRequestTypeDef,
    ListIdNamespacesOutputTypeDef,
    ListMatchingJobsInputRequestTypeDef,
    ListMatchingJobsOutputTypeDef,
    ListMatchingWorkflowsInputRequestTypeDef,
    ListMatchingWorkflowsOutputTypeDef,
    ListProviderServicesInputRequestTypeDef,
    ListProviderServicesOutputTypeDef,
    ListSchemaMappingsInputRequestTypeDef,
    ListSchemaMappingsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    PutPolicyInputRequestTypeDef,
    PutPolicyOutputTypeDef,
    StartIdMappingJobInputRequestTypeDef,
    StartIdMappingJobOutputTypeDef,
    StartMatchingJobInputRequestTypeDef,
    StartMatchingJobOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateIdMappingWorkflowInputRequestTypeDef,
    UpdateIdMappingWorkflowOutputTypeDef,
    UpdateIdNamespaceInputRequestTypeDef,
    UpdateIdNamespaceOutputTypeDef,
    UpdateMatchingWorkflowInputRequestTypeDef,
    UpdateMatchingWorkflowOutputTypeDef,
    UpdateSchemaMappingInputRequestTypeDef,
    UpdateSchemaMappingOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("EntityResolutionClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ExceedsLimitException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class EntityResolutionClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EntityResolutionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#exceptions)
        """

    def add_policy_statement(
        self, **kwargs: Unpack[AddPolicyStatementInputRequestTypeDef]
    ) -> AddPolicyStatementOutputTypeDef:
        """
        Adds a policy statement object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.add_policy_statement)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#add_policy_statement)
        """

    def batch_delete_unique_id(
        self, **kwargs: Unpack[BatchDeleteUniqueIdInputRequestTypeDef]
    ) -> BatchDeleteUniqueIdOutputTypeDef:
        """
        Deletes multiple unique IDs in a matching workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.batch_delete_unique_id)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#batch_delete_unique_id)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#close)
        """

    def create_id_mapping_workflow(
        self, **kwargs: Unpack[CreateIdMappingWorkflowInputRequestTypeDef]
    ) -> CreateIdMappingWorkflowOutputTypeDef:
        """
        Creates an `IdMappingWorkflow` object which stores the configuration of the
        data processing job to be
        run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.create_id_mapping_workflow)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#create_id_mapping_workflow)
        """

    def create_id_namespace(
        self, **kwargs: Unpack[CreateIdNamespaceInputRequestTypeDef]
    ) -> CreateIdNamespaceOutputTypeDef:
        """
        Creates an ID namespace object which will help customers provide metadata
        explaining their dataset and how to use
        it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.create_id_namespace)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#create_id_namespace)
        """

    def create_matching_workflow(
        self, **kwargs: Unpack[CreateMatchingWorkflowInputRequestTypeDef]
    ) -> CreateMatchingWorkflowOutputTypeDef:
        """
        Creates a `MatchingWorkflow` object which stores the configuration of the data
        processing job to be
        run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.create_matching_workflow)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#create_matching_workflow)
        """

    def create_schema_mapping(
        self, **kwargs: Unpack[CreateSchemaMappingInputRequestTypeDef]
    ) -> CreateSchemaMappingOutputTypeDef:
        """
        Creates a schema mapping, which defines the schema of the input customer
        records
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.create_schema_mapping)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#create_schema_mapping)
        """

    def delete_id_mapping_workflow(
        self, **kwargs: Unpack[DeleteIdMappingWorkflowInputRequestTypeDef]
    ) -> DeleteIdMappingWorkflowOutputTypeDef:
        """
        Deletes the `IdMappingWorkflow` with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.delete_id_mapping_workflow)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_id_mapping_workflow)
        """

    def delete_id_namespace(
        self, **kwargs: Unpack[DeleteIdNamespaceInputRequestTypeDef]
    ) -> DeleteIdNamespaceOutputTypeDef:
        """
        Deletes the `IdNamespace` with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.delete_id_namespace)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_id_namespace)
        """

    def delete_matching_workflow(
        self, **kwargs: Unpack[DeleteMatchingWorkflowInputRequestTypeDef]
    ) -> DeleteMatchingWorkflowOutputTypeDef:
        """
        Deletes the `MatchingWorkflow` with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.delete_matching_workflow)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_matching_workflow)
        """

    def delete_policy_statement(
        self, **kwargs: Unpack[DeletePolicyStatementInputRequestTypeDef]
    ) -> DeletePolicyStatementOutputTypeDef:
        """
        Deletes the policy statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.delete_policy_statement)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_policy_statement)
        """

    def delete_schema_mapping(
        self, **kwargs: Unpack[DeleteSchemaMappingInputRequestTypeDef]
    ) -> DeleteSchemaMappingOutputTypeDef:
        """
        Deletes the `SchemaMapping` with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.delete_schema_mapping)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#delete_schema_mapping)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#generate_presigned_url)
        """

    def get_id_mapping_job(
        self, **kwargs: Unpack[GetIdMappingJobInputRequestTypeDef]
    ) -> GetIdMappingJobOutputTypeDef:
        """
        Gets the status, metrics, and errors (if there are any) that are associated
        with a
        job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_id_mapping_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_id_mapping_job)
        """

    def get_id_mapping_workflow(
        self, **kwargs: Unpack[GetIdMappingWorkflowInputRequestTypeDef]
    ) -> GetIdMappingWorkflowOutputTypeDef:
        """
        Returns the `IdMappingWorkflow` with a given name, if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_id_mapping_workflow)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_id_mapping_workflow)
        """

    def get_id_namespace(
        self, **kwargs: Unpack[GetIdNamespaceInputRequestTypeDef]
    ) -> GetIdNamespaceOutputTypeDef:
        """
        Returns the `IdNamespace` with a given name, if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_id_namespace)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_id_namespace)
        """

    def get_match_id(
        self, **kwargs: Unpack[GetMatchIdInputRequestTypeDef]
    ) -> GetMatchIdOutputTypeDef:
        """
        Returns the corresponding Match ID of a customer record if the record has been
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_match_id)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_match_id)
        """

    def get_matching_job(
        self, **kwargs: Unpack[GetMatchingJobInputRequestTypeDef]
    ) -> GetMatchingJobOutputTypeDef:
        """
        Gets the status, metrics, and errors (if there are any) that are associated
        with a
        job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_matching_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_matching_job)
        """

    def get_matching_workflow(
        self, **kwargs: Unpack[GetMatchingWorkflowInputRequestTypeDef]
    ) -> GetMatchingWorkflowOutputTypeDef:
        """
        Returns the `MatchingWorkflow` with a given name, if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_matching_workflow)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_matching_workflow)
        """

    def get_policy(self, **kwargs: Unpack[GetPolicyInputRequestTypeDef]) -> GetPolicyOutputTypeDef:
        """
        Returns the resource-based policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_policy)
        """

    def get_provider_service(
        self, **kwargs: Unpack[GetProviderServiceInputRequestTypeDef]
    ) -> GetProviderServiceOutputTypeDef:
        """
        Returns the `ProviderService` of a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_provider_service)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_provider_service)
        """

    def get_schema_mapping(
        self, **kwargs: Unpack[GetSchemaMappingInputRequestTypeDef]
    ) -> GetSchemaMappingOutputTypeDef:
        """
        Returns the SchemaMapping of a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_schema_mapping)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_schema_mapping)
        """

    def list_id_mapping_jobs(
        self, **kwargs: Unpack[ListIdMappingJobsInputRequestTypeDef]
    ) -> ListIdMappingJobsOutputTypeDef:
        """
        Lists all ID mapping jobs for a given workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_id_mapping_jobs)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_id_mapping_jobs)
        """

    def list_id_mapping_workflows(
        self, **kwargs: Unpack[ListIdMappingWorkflowsInputRequestTypeDef]
    ) -> ListIdMappingWorkflowsOutputTypeDef:
        """
        Returns a list of all the `IdMappingWorkflows` that have been created for an
        Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_id_mapping_workflows)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_id_mapping_workflows)
        """

    def list_id_namespaces(
        self, **kwargs: Unpack[ListIdNamespacesInputRequestTypeDef]
    ) -> ListIdNamespacesOutputTypeDef:
        """
        Returns a list of all ID namespaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_id_namespaces)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_id_namespaces)
        """

    def list_matching_jobs(
        self, **kwargs: Unpack[ListMatchingJobsInputRequestTypeDef]
    ) -> ListMatchingJobsOutputTypeDef:
        """
        Lists all jobs for a given workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_matching_jobs)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_matching_jobs)
        """

    def list_matching_workflows(
        self, **kwargs: Unpack[ListMatchingWorkflowsInputRequestTypeDef]
    ) -> ListMatchingWorkflowsOutputTypeDef:
        """
        Returns a list of all the `MatchingWorkflows` that have been created for an
        Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_matching_workflows)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_matching_workflows)
        """

    def list_provider_services(
        self, **kwargs: Unpack[ListProviderServicesInputRequestTypeDef]
    ) -> ListProviderServicesOutputTypeDef:
        """
        Returns a list of all the `ProviderServices` that are available in this Amazon
        Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_provider_services)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_provider_services)
        """

    def list_schema_mappings(
        self, **kwargs: Unpack[ListSchemaMappingsInputRequestTypeDef]
    ) -> ListSchemaMappingsOutputTypeDef:
        """
        Returns a list of all the `SchemaMappings` that have been created for an Amazon
        Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_schema_mappings)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_schema_mappings)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Displays the tags associated with an Entity Resolution resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#list_tags_for_resource)
        """

    def put_policy(self, **kwargs: Unpack[PutPolicyInputRequestTypeDef]) -> PutPolicyOutputTypeDef:
        """
        Updates the resource-based policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.put_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#put_policy)
        """

    def start_id_mapping_job(
        self, **kwargs: Unpack[StartIdMappingJobInputRequestTypeDef]
    ) -> StartIdMappingJobOutputTypeDef:
        """
        Starts the `IdMappingJob` of a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.start_id_mapping_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#start_id_mapping_job)
        """

    def start_matching_job(
        self, **kwargs: Unpack[StartMatchingJobInputRequestTypeDef]
    ) -> StartMatchingJobOutputTypeDef:
        """
        Starts the `MatchingJob` of a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.start_matching_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#start_matching_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified Entity Resolution
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified Entity Resolution resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#untag_resource)
        """

    def update_id_mapping_workflow(
        self, **kwargs: Unpack[UpdateIdMappingWorkflowInputRequestTypeDef]
    ) -> UpdateIdMappingWorkflowOutputTypeDef:
        """
        Updates an existing `IdMappingWorkflow`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.update_id_mapping_workflow)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#update_id_mapping_workflow)
        """

    def update_id_namespace(
        self, **kwargs: Unpack[UpdateIdNamespaceInputRequestTypeDef]
    ) -> UpdateIdNamespaceOutputTypeDef:
        """
        Updates an existing ID namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.update_id_namespace)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#update_id_namespace)
        """

    def update_matching_workflow(
        self, **kwargs: Unpack[UpdateMatchingWorkflowInputRequestTypeDef]
    ) -> UpdateMatchingWorkflowOutputTypeDef:
        """
        Updates an existing `MatchingWorkflow`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.update_matching_workflow)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#update_matching_workflow)
        """

    def update_schema_mapping(
        self, **kwargs: Unpack[UpdateSchemaMappingInputRequestTypeDef]
    ) -> UpdateSchemaMappingOutputTypeDef:
        """
        Updates a schema mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.update_schema_mapping)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#update_schema_mapping)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_id_mapping_jobs"]
    ) -> ListIdMappingJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_id_mapping_workflows"]
    ) -> ListIdMappingWorkflowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_id_namespaces"]
    ) -> ListIdNamespacesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_matching_jobs"]
    ) -> ListMatchingJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_matching_workflows"]
    ) -> ListMatchingWorkflowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provider_services"]
    ) -> ListProviderServicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_schema_mappings"]
    ) -> ListSchemaMappingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/client/#get_paginator)
        """
