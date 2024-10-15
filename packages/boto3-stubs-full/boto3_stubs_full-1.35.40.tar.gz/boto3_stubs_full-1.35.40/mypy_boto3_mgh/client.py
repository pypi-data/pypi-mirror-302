"""
Type annotations for mgh service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mgh.client import MigrationHubClient

    session = Session()
    client: MigrationHubClient = session.client("mgh")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListApplicationStatesPaginator,
    ListCreatedArtifactsPaginator,
    ListDiscoveredResourcesPaginator,
    ListMigrationTasksPaginator,
    ListProgressUpdateStreamsPaginator,
)
from .type_defs import (
    AssociateCreatedArtifactRequestRequestTypeDef,
    AssociateDiscoveredResourceRequestRequestTypeDef,
    CreateProgressUpdateStreamRequestRequestTypeDef,
    DeleteProgressUpdateStreamRequestRequestTypeDef,
    DescribeApplicationStateRequestRequestTypeDef,
    DescribeApplicationStateResultTypeDef,
    DescribeMigrationTaskRequestRequestTypeDef,
    DescribeMigrationTaskResultTypeDef,
    DisassociateCreatedArtifactRequestRequestTypeDef,
    DisassociateDiscoveredResourceRequestRequestTypeDef,
    ImportMigrationTaskRequestRequestTypeDef,
    ListApplicationStatesRequestRequestTypeDef,
    ListApplicationStatesResultTypeDef,
    ListCreatedArtifactsRequestRequestTypeDef,
    ListCreatedArtifactsResultTypeDef,
    ListDiscoveredResourcesRequestRequestTypeDef,
    ListDiscoveredResourcesResultTypeDef,
    ListMigrationTasksRequestRequestTypeDef,
    ListMigrationTasksResultTypeDef,
    ListProgressUpdateStreamsRequestRequestTypeDef,
    ListProgressUpdateStreamsResultTypeDef,
    NotifyApplicationStateRequestRequestTypeDef,
    NotifyMigrationTaskStateRequestRequestTypeDef,
    PutResourceAttributesRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("MigrationHubClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DryRunOperation: Type[BotocoreClientError]
    HomeRegionNotSetException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    PolicyErrorException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedOperation: Type[BotocoreClientError]


class MigrationHubClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MigrationHubClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#exceptions)
        """

    def associate_created_artifact(
        self, **kwargs: Unpack[AssociateCreatedArtifactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a created artifact of an AWS cloud resource, the target receiving
        the migration, with the migration task performed by a migration
        tool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.associate_created_artifact)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#associate_created_artifact)
        """

    def associate_discovered_resource(
        self, **kwargs: Unpack[AssociateDiscoveredResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a discovered resource ID from Application Discovery Service with a
        migration
        task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.associate_discovered_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#associate_discovered_resource)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#close)
        """

    def create_progress_update_stream(
        self, **kwargs: Unpack[CreateProgressUpdateStreamRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a progress update stream which is an AWS resource used for access
        control as well as a namespace for migration task names that is implicitly
        linked to your AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.create_progress_update_stream)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#create_progress_update_stream)
        """

    def delete_progress_update_stream(
        self, **kwargs: Unpack[DeleteProgressUpdateStreamRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a progress update stream, including all of its tasks, which was
        previously created as an AWS resource used for access
        control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.delete_progress_update_stream)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#delete_progress_update_stream)
        """

    def describe_application_state(
        self, **kwargs: Unpack[DescribeApplicationStateRequestRequestTypeDef]
    ) -> DescribeApplicationStateResultTypeDef:
        """
        Gets the migration status of an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.describe_application_state)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#describe_application_state)
        """

    def describe_migration_task(
        self, **kwargs: Unpack[DescribeMigrationTaskRequestRequestTypeDef]
    ) -> DescribeMigrationTaskResultTypeDef:
        """
        Retrieves a list of all attributes associated with a specific migration task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.describe_migration_task)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#describe_migration_task)
        """

    def disassociate_created_artifact(
        self, **kwargs: Unpack[DisassociateCreatedArtifactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a created artifact of an AWS resource with a migration task
        performed by a migration tool that was previously
        associated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.disassociate_created_artifact)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#disassociate_created_artifact)
        """

    def disassociate_discovered_resource(
        self, **kwargs: Unpack[DisassociateDiscoveredResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociate an Application Discovery Service discovered resource from a
        migration
        task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.disassociate_discovered_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#disassociate_discovered_resource)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#generate_presigned_url)
        """

    def import_migration_task(
        self, **kwargs: Unpack[ImportMigrationTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers a new migration task which represents a server, database, etc., being
        migrated to AWS by a migration
        tool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.import_migration_task)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#import_migration_task)
        """

    def list_application_states(
        self, **kwargs: Unpack[ListApplicationStatesRequestRequestTypeDef]
    ) -> ListApplicationStatesResultTypeDef:
        """
        Lists all the migration statuses for your applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.list_application_states)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#list_application_states)
        """

    def list_created_artifacts(
        self, **kwargs: Unpack[ListCreatedArtifactsRequestRequestTypeDef]
    ) -> ListCreatedArtifactsResultTypeDef:
        """
        Lists the created artifacts attached to a given migration task in an update
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.list_created_artifacts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#list_created_artifacts)
        """

    def list_discovered_resources(
        self, **kwargs: Unpack[ListDiscoveredResourcesRequestRequestTypeDef]
    ) -> ListDiscoveredResourcesResultTypeDef:
        """
        Lists discovered resources associated with the given `MigrationTask`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.list_discovered_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#list_discovered_resources)
        """

    def list_migration_tasks(
        self, **kwargs: Unpack[ListMigrationTasksRequestRequestTypeDef]
    ) -> ListMigrationTasksResultTypeDef:
        """
        Lists all, or filtered by resource name, migration tasks associated with the
        user account making this
        call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.list_migration_tasks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#list_migration_tasks)
        """

    def list_progress_update_streams(
        self, **kwargs: Unpack[ListProgressUpdateStreamsRequestRequestTypeDef]
    ) -> ListProgressUpdateStreamsResultTypeDef:
        """
        Lists progress update streams associated with the user account making this call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.list_progress_update_streams)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#list_progress_update_streams)
        """

    def notify_application_state(
        self, **kwargs: Unpack[NotifyApplicationStateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the migration state of an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.notify_application_state)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#notify_application_state)
        """

    def notify_migration_task_state(
        self, **kwargs: Unpack[NotifyMigrationTaskStateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Notifies Migration Hub of the current status, progress, or other detail
        regarding a migration
        task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.notify_migration_task_state)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#notify_migration_task_state)
        """

    def put_resource_attributes(
        self, **kwargs: Unpack[PutResourceAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Provides identifying details of the resource being migrated so that it can be
        associated in the Application Discovery Service
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.put_resource_attributes)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#put_resource_attributes)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_states"]
    ) -> ListApplicationStatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_created_artifacts"]
    ) -> ListCreatedArtifactsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_discovered_resources"]
    ) -> ListDiscoveredResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_migration_tasks"]
    ) -> ListMigrationTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_progress_update_streams"]
    ) -> ListProgressUpdateStreamsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgh/client/#get_paginator)
        """
