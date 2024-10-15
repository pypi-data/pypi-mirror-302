"""
Type annotations for workdocs service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_workdocs.client import WorkDocsClient

    session = Session()
    client: WorkDocsClient = session.client("workdocs")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeActivitiesPaginator,
    DescribeCommentsPaginator,
    DescribeDocumentVersionsPaginator,
    DescribeFolderContentsPaginator,
    DescribeGroupsPaginator,
    DescribeNotificationSubscriptionsPaginator,
    DescribeResourcePermissionsPaginator,
    DescribeRootFoldersPaginator,
    DescribeUsersPaginator,
    SearchResourcesPaginator,
)
from .type_defs import (
    AbortDocumentVersionUploadRequestRequestTypeDef,
    ActivateUserRequestRequestTypeDef,
    ActivateUserResponseTypeDef,
    AddResourcePermissionsRequestRequestTypeDef,
    AddResourcePermissionsResponseTypeDef,
    CreateCommentRequestRequestTypeDef,
    CreateCommentResponseTypeDef,
    CreateCustomMetadataRequestRequestTypeDef,
    CreateFolderRequestRequestTypeDef,
    CreateFolderResponseTypeDef,
    CreateLabelsRequestRequestTypeDef,
    CreateNotificationSubscriptionRequestRequestTypeDef,
    CreateNotificationSubscriptionResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResponseTypeDef,
    DeactivateUserRequestRequestTypeDef,
    DeleteCommentRequestRequestTypeDef,
    DeleteCustomMetadataRequestRequestTypeDef,
    DeleteDocumentRequestRequestTypeDef,
    DeleteDocumentVersionRequestRequestTypeDef,
    DeleteFolderContentsRequestRequestTypeDef,
    DeleteFolderRequestRequestTypeDef,
    DeleteLabelsRequestRequestTypeDef,
    DeleteNotificationSubscriptionRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DescribeActivitiesRequestRequestTypeDef,
    DescribeActivitiesResponseTypeDef,
    DescribeCommentsRequestRequestTypeDef,
    DescribeCommentsResponseTypeDef,
    DescribeDocumentVersionsRequestRequestTypeDef,
    DescribeDocumentVersionsResponseTypeDef,
    DescribeFolderContentsRequestRequestTypeDef,
    DescribeFolderContentsResponseTypeDef,
    DescribeGroupsRequestRequestTypeDef,
    DescribeGroupsResponseTypeDef,
    DescribeNotificationSubscriptionsRequestRequestTypeDef,
    DescribeNotificationSubscriptionsResponseTypeDef,
    DescribeResourcePermissionsRequestRequestTypeDef,
    DescribeResourcePermissionsResponseTypeDef,
    DescribeRootFoldersRequestRequestTypeDef,
    DescribeRootFoldersResponseTypeDef,
    DescribeUsersRequestRequestTypeDef,
    DescribeUsersResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCurrentUserRequestRequestTypeDef,
    GetCurrentUserResponseTypeDef,
    GetDocumentPathRequestRequestTypeDef,
    GetDocumentPathResponseTypeDef,
    GetDocumentRequestRequestTypeDef,
    GetDocumentResponseTypeDef,
    GetDocumentVersionRequestRequestTypeDef,
    GetDocumentVersionResponseTypeDef,
    GetFolderPathRequestRequestTypeDef,
    GetFolderPathResponseTypeDef,
    GetFolderRequestRequestTypeDef,
    GetFolderResponseTypeDef,
    GetResourcesRequestRequestTypeDef,
    GetResourcesResponseTypeDef,
    InitiateDocumentVersionUploadRequestRequestTypeDef,
    InitiateDocumentVersionUploadResponseTypeDef,
    RemoveAllResourcePermissionsRequestRequestTypeDef,
    RemoveResourcePermissionRequestRequestTypeDef,
    RestoreDocumentVersionsRequestRequestTypeDef,
    SearchResourcesRequestRequestTypeDef,
    SearchResourcesResponseTypeDef,
    UpdateDocumentRequestRequestTypeDef,
    UpdateDocumentVersionRequestRequestTypeDef,
    UpdateFolderRequestRequestTypeDef,
    UpdateUserRequestRequestTypeDef,
    UpdateUserResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("WorkDocsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConflictingOperationException: Type[BotocoreClientError]
    CustomMetadataLimitExceededException: Type[BotocoreClientError]
    DeactivatingLastSystemUserException: Type[BotocoreClientError]
    DocumentLockedForCommentsException: Type[BotocoreClientError]
    DraftUploadOutOfSyncException: Type[BotocoreClientError]
    EntityAlreadyExistsException: Type[BotocoreClientError]
    EntityNotExistsException: Type[BotocoreClientError]
    FailedDependencyException: Type[BotocoreClientError]
    IllegalUserStateException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidCommentOperationException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidPasswordException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ProhibitedStateException: Type[BotocoreClientError]
    RequestedEntityTooLargeException: Type[BotocoreClientError]
    ResourceAlreadyCheckedOutException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    StorageLimitExceededException: Type[BotocoreClientError]
    StorageLimitWillExceedException: Type[BotocoreClientError]
    TooManyLabelsException: Type[BotocoreClientError]
    TooManySubscriptionsException: Type[BotocoreClientError]
    UnauthorizedOperationException: Type[BotocoreClientError]
    UnauthorizedResourceAccessException: Type[BotocoreClientError]

class WorkDocsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkDocsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#exceptions)
        """

    def abort_document_version_upload(
        self, **kwargs: Unpack[AbortDocumentVersionUploadRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Aborts the upload of the specified document version that was previously
        initiated by
        InitiateDocumentVersionUpload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.abort_document_version_upload)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#abort_document_version_upload)
        """

    def activate_user(
        self, **kwargs: Unpack[ActivateUserRequestRequestTypeDef]
    ) -> ActivateUserResponseTypeDef:
        """
        Activates the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.activate_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#activate_user)
        """

    def add_resource_permissions(
        self, **kwargs: Unpack[AddResourcePermissionsRequestRequestTypeDef]
    ) -> AddResourcePermissionsResponseTypeDef:
        """
        Creates a set of permissions for the specified folder or document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.add_resource_permissions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#add_resource_permissions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#close)
        """

    def create_comment(
        self, **kwargs: Unpack[CreateCommentRequestRequestTypeDef]
    ) -> CreateCommentResponseTypeDef:
        """
        Adds a new comment to the specified document version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_comment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#create_comment)
        """

    def create_custom_metadata(
        self, **kwargs: Unpack[CreateCustomMetadataRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds one or more custom properties to the specified resource (a folder,
        document, or
        version).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_custom_metadata)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#create_custom_metadata)
        """

    def create_folder(
        self, **kwargs: Unpack[CreateFolderRequestRequestTypeDef]
    ) -> CreateFolderResponseTypeDef:
        """
        Creates a folder with the specified name and parent folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_folder)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#create_folder)
        """

    def create_labels(self, **kwargs: Unpack[CreateLabelsRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified list of labels to the given resource (a document or folder)
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/workdocs-2016-05-01/CreateLabels).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_labels)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#create_labels)
        """

    def create_notification_subscription(
        self, **kwargs: Unpack[CreateNotificationSubscriptionRequestRequestTypeDef]
    ) -> CreateNotificationSubscriptionResponseTypeDef:
        """
        Configure Amazon WorkDocs to use Amazon SNS notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_notification_subscription)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#create_notification_subscription)
        """

    def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user in a Simple AD or Microsoft AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#create_user)
        """

    def deactivate_user(
        self, **kwargs: Unpack[DeactivateUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deactivates the specified user, which revokes the user's access to Amazon
        WorkDocs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.deactivate_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#deactivate_user)
        """

    def delete_comment(
        self, **kwargs: Unpack[DeleteCommentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified comment from the document version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_comment)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#delete_comment)
        """

    def delete_custom_metadata(
        self, **kwargs: Unpack[DeleteCustomMetadataRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes custom metadata from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_custom_metadata)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#delete_custom_metadata)
        """

    def delete_document(
        self, **kwargs: Unpack[DeleteDocumentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes the specified document and its associated metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_document)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#delete_document)
        """

    def delete_document_version(
        self, **kwargs: Unpack[DeleteDocumentVersionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specific version of a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_document_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#delete_document_version)
        """

    def delete_folder(
        self, **kwargs: Unpack[DeleteFolderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes the specified folder and its contents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_folder)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#delete_folder)
        """

    def delete_folder_contents(
        self, **kwargs: Unpack[DeleteFolderContentsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the contents of the specified folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_folder_contents)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#delete_folder_contents)
        """

    def delete_labels(self, **kwargs: Unpack[DeleteLabelsRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified list of labels from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_labels)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#delete_labels)
        """

    def delete_notification_subscription(
        self, **kwargs: Unpack[DeleteNotificationSubscriptionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified subscription from the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_notification_subscription)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#delete_notification_subscription)
        """

    def delete_user(
        self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified user from a Simple AD or Microsoft AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#delete_user)
        """

    def describe_activities(
        self, **kwargs: Unpack[DescribeActivitiesRequestRequestTypeDef]
    ) -> DescribeActivitiesResponseTypeDef:
        """
        Describes the user activities in a specified time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_activities)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#describe_activities)
        """

    def describe_comments(
        self, **kwargs: Unpack[DescribeCommentsRequestRequestTypeDef]
    ) -> DescribeCommentsResponseTypeDef:
        """
        List all the comments for the specified document version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_comments)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#describe_comments)
        """

    def describe_document_versions(
        self, **kwargs: Unpack[DescribeDocumentVersionsRequestRequestTypeDef]
    ) -> DescribeDocumentVersionsResponseTypeDef:
        """
        Retrieves the document versions for the specified document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_document_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#describe_document_versions)
        """

    def describe_folder_contents(
        self, **kwargs: Unpack[DescribeFolderContentsRequestRequestTypeDef]
    ) -> DescribeFolderContentsResponseTypeDef:
        """
        Describes the contents of the specified folder, including its documents and
        subfolders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_folder_contents)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#describe_folder_contents)
        """

    def describe_groups(
        self, **kwargs: Unpack[DescribeGroupsRequestRequestTypeDef]
    ) -> DescribeGroupsResponseTypeDef:
        """
        Describes the groups specified by the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_groups)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#describe_groups)
        """

    def describe_notification_subscriptions(
        self, **kwargs: Unpack[DescribeNotificationSubscriptionsRequestRequestTypeDef]
    ) -> DescribeNotificationSubscriptionsResponseTypeDef:
        """
        Lists the specified notification subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_notification_subscriptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#describe_notification_subscriptions)
        """

    def describe_resource_permissions(
        self, **kwargs: Unpack[DescribeResourcePermissionsRequestRequestTypeDef]
    ) -> DescribeResourcePermissionsResponseTypeDef:
        """
        Describes the permissions of a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_resource_permissions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#describe_resource_permissions)
        """

    def describe_root_folders(
        self, **kwargs: Unpack[DescribeRootFoldersRequestRequestTypeDef]
    ) -> DescribeRootFoldersResponseTypeDef:
        """
        Describes the current user's special folders; the `RootFolder` and the
        `RecycleBin`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_root_folders)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#describe_root_folders)
        """

    def describe_users(
        self, **kwargs: Unpack[DescribeUsersRequestRequestTypeDef]
    ) -> DescribeUsersResponseTypeDef:
        """
        Describes the specified users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_users)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#describe_users)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#generate_presigned_url)
        """

    def get_current_user(
        self, **kwargs: Unpack[GetCurrentUserRequestRequestTypeDef]
    ) -> GetCurrentUserResponseTypeDef:
        """
        Retrieves details of the current user for whom the authentication token was
        generated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_current_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_current_user)
        """

    def get_document(
        self, **kwargs: Unpack[GetDocumentRequestRequestTypeDef]
    ) -> GetDocumentResponseTypeDef:
        """
        Retrieves details of a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_document)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_document)
        """

    def get_document_path(
        self, **kwargs: Unpack[GetDocumentPathRequestRequestTypeDef]
    ) -> GetDocumentPathResponseTypeDef:
        """
        Retrieves the path information (the hierarchy from the root folder) for the
        requested
        document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_document_path)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_document_path)
        """

    def get_document_version(
        self, **kwargs: Unpack[GetDocumentVersionRequestRequestTypeDef]
    ) -> GetDocumentVersionResponseTypeDef:
        """
        Retrieves version metadata for the specified document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_document_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_document_version)
        """

    def get_folder(
        self, **kwargs: Unpack[GetFolderRequestRequestTypeDef]
    ) -> GetFolderResponseTypeDef:
        """
        Retrieves the metadata of the specified folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_folder)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_folder)
        """

    def get_folder_path(
        self, **kwargs: Unpack[GetFolderPathRequestRequestTypeDef]
    ) -> GetFolderPathResponseTypeDef:
        """
        Retrieves the path information (the hierarchy from the root folder) for the
        specified
        folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_folder_path)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_folder_path)
        """

    def get_resources(
        self, **kwargs: Unpack[GetResourcesRequestRequestTypeDef]
    ) -> GetResourcesResponseTypeDef:
        """
        Retrieves a collection of resources, including folders and documents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_resources)
        """

    def initiate_document_version_upload(
        self, **kwargs: Unpack[InitiateDocumentVersionUploadRequestRequestTypeDef]
    ) -> InitiateDocumentVersionUploadResponseTypeDef:
        """
        Creates a new document object and version object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.initiate_document_version_upload)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#initiate_document_version_upload)
        """

    def remove_all_resource_permissions(
        self, **kwargs: Unpack[RemoveAllResourcePermissionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes all the permissions from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.remove_all_resource_permissions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#remove_all_resource_permissions)
        """

    def remove_resource_permission(
        self, **kwargs: Unpack[RemoveResourcePermissionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the permission for the specified principal from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.remove_resource_permission)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#remove_resource_permission)
        """

    def restore_document_versions(
        self, **kwargs: Unpack[RestoreDocumentVersionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Recovers a deleted version of an Amazon WorkDocs document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.restore_document_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#restore_document_versions)
        """

    def search_resources(
        self, **kwargs: Unpack[SearchResourcesRequestRequestTypeDef]
    ) -> SearchResourcesResponseTypeDef:
        """
        Searches metadata and the content of folders, documents, document versions, and
        comments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.search_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#search_resources)
        """

    def update_document(
        self, **kwargs: Unpack[UpdateDocumentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the specified attributes of a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.update_document)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#update_document)
        """

    def update_document_version(
        self, **kwargs: Unpack[UpdateDocumentVersionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the status of the document version to ACTIVE.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.update_document_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#update_document_version)
        """

    def update_folder(
        self, **kwargs: Unpack[UpdateFolderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the specified attributes of the specified folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.update_folder)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#update_folder)
        """

    def update_user(
        self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]
    ) -> UpdateUserResponseTypeDef:
        """
        Updates the specified attributes of the specified user, and grants or revokes
        administrative privileges to the Amazon WorkDocs
        site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.update_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#update_user)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_activities"]
    ) -> DescribeActivitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_comments"]
    ) -> DescribeCommentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_document_versions"]
    ) -> DescribeDocumentVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_folder_contents"]
    ) -> DescribeFolderContentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_groups"]) -> DescribeGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_notification_subscriptions"]
    ) -> DescribeNotificationSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_resource_permissions"]
    ) -> DescribeResourcePermissionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_root_folders"]
    ) -> DescribeRootFoldersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_users"]) -> DescribeUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_resources"]
    ) -> SearchResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/client/#get_paginator)
        """
