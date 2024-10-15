"""
Type annotations for ivschat service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ivschat.client import IvschatClient

    session = Session()
    client: IvschatClient = session.client("ivschat")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateChatTokenRequestRequestTypeDef,
    CreateChatTokenResponseTypeDef,
    CreateLoggingConfigurationRequestRequestTypeDef,
    CreateLoggingConfigurationResponseTypeDef,
    CreateRoomRequestRequestTypeDef,
    CreateRoomResponseTypeDef,
    DeleteLoggingConfigurationRequestRequestTypeDef,
    DeleteMessageRequestRequestTypeDef,
    DeleteMessageResponseTypeDef,
    DeleteRoomRequestRequestTypeDef,
    DisconnectUserRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetLoggingConfigurationRequestRequestTypeDef,
    GetLoggingConfigurationResponseTypeDef,
    GetRoomRequestRequestTypeDef,
    GetRoomResponseTypeDef,
    ListLoggingConfigurationsRequestRequestTypeDef,
    ListLoggingConfigurationsResponseTypeDef,
    ListRoomsRequestRequestTypeDef,
    ListRoomsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SendEventRequestRequestTypeDef,
    SendEventResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateLoggingConfigurationRequestRequestTypeDef,
    UpdateLoggingConfigurationResponseTypeDef,
    UpdateRoomRequestRequestTypeDef,
    UpdateRoomResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("IvschatClient",)

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
    PendingVerification: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class IvschatClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IvschatClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#close)
        """

    def create_chat_token(
        self, **kwargs: Unpack[CreateChatTokenRequestRequestTypeDef]
    ) -> CreateChatTokenResponseTypeDef:
        """
        Creates an encrypted token that is used by a chat participant to establish an
        individual WebSocket chat connection to a
        room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.create_chat_token)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#create_chat_token)
        """

    def create_logging_configuration(
        self, **kwargs: Unpack[CreateLoggingConfigurationRequestRequestTypeDef]
    ) -> CreateLoggingConfigurationResponseTypeDef:
        """
        Creates a logging configuration that allows clients to store and record sent
        messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.create_logging_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#create_logging_configuration)
        """

    def create_room(
        self, **kwargs: Unpack[CreateRoomRequestRequestTypeDef]
    ) -> CreateRoomResponseTypeDef:
        """
        Creates a room that allows clients to connect and pass messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.create_room)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#create_room)
        """

    def delete_logging_configuration(
        self, **kwargs: Unpack[DeleteLoggingConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.delete_logging_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#delete_logging_configuration)
        """

    def delete_message(
        self, **kwargs: Unpack[DeleteMessageRequestRequestTypeDef]
    ) -> DeleteMessageResponseTypeDef:
        """
        Sends an event to a specific room which directs clients to delete a specific
        message; that is, unrender it from view and delete it from the client's chat
        history.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.delete_message)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#delete_message)
        """

    def delete_room(
        self, **kwargs: Unpack[DeleteRoomRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.delete_room)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#delete_room)
        """

    def disconnect_user(
        self, **kwargs: Unpack[DisconnectUserRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disconnects all connections using a specified user ID from a room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.disconnect_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#disconnect_user)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#generate_presigned_url)
        """

    def get_logging_configuration(
        self, **kwargs: Unpack[GetLoggingConfigurationRequestRequestTypeDef]
    ) -> GetLoggingConfigurationResponseTypeDef:
        """
        Gets the specified logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.get_logging_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#get_logging_configuration)
        """

    def get_room(self, **kwargs: Unpack[GetRoomRequestRequestTypeDef]) -> GetRoomResponseTypeDef:
        """
        Gets the specified room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.get_room)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#get_room)
        """

    def list_logging_configurations(
        self, **kwargs: Unpack[ListLoggingConfigurationsRequestRequestTypeDef]
    ) -> ListLoggingConfigurationsResponseTypeDef:
        """
        Gets summary information about all your logging configurations in the AWS
        region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.list_logging_configurations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#list_logging_configurations)
        """

    def list_rooms(
        self, **kwargs: Unpack[ListRoomsRequestRequestTypeDef]
    ) -> ListRoomsResponseTypeDef:
        """
        Gets summary information about all your rooms in the AWS region where the API
        request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.list_rooms)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#list_rooms)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets information about AWS tags for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#list_tags_for_resource)
        """

    def send_event(
        self, **kwargs: Unpack[SendEventRequestRequestTypeDef]
    ) -> SendEventResponseTypeDef:
        """
        Sends an event to a room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.send_event)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#send_event)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or updates tags for the AWS resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from the resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#untag_resource)
        """

    def update_logging_configuration(
        self, **kwargs: Unpack[UpdateLoggingConfigurationRequestRequestTypeDef]
    ) -> UpdateLoggingConfigurationResponseTypeDef:
        """
        Updates a specified logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.update_logging_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#update_logging_configuration)
        """

    def update_room(
        self, **kwargs: Unpack[UpdateRoomRequestRequestTypeDef]
    ) -> UpdateRoomResponseTypeDef:
        """
        Updates a room's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client.update_room)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#update_room)
        """
