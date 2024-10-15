"""
Type annotations for kinesisvideo service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesisvideo.client import KinesisVideoClient

    session = Session()
    client: KinesisVideoClient = session.client("kinesisvideo")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeMappedResourceConfigurationPaginator,
    ListEdgeAgentConfigurationsPaginator,
    ListSignalingChannelsPaginator,
    ListStreamsPaginator,
)
from .type_defs import (
    CreateSignalingChannelInputRequestTypeDef,
    CreateSignalingChannelOutputTypeDef,
    CreateStreamInputRequestTypeDef,
    CreateStreamOutputTypeDef,
    DeleteEdgeConfigurationInputRequestTypeDef,
    DeleteSignalingChannelInputRequestTypeDef,
    DeleteStreamInputRequestTypeDef,
    DescribeEdgeConfigurationInputRequestTypeDef,
    DescribeEdgeConfigurationOutputTypeDef,
    DescribeImageGenerationConfigurationInputRequestTypeDef,
    DescribeImageGenerationConfigurationOutputTypeDef,
    DescribeMappedResourceConfigurationInputRequestTypeDef,
    DescribeMappedResourceConfigurationOutputTypeDef,
    DescribeMediaStorageConfigurationInputRequestTypeDef,
    DescribeMediaStorageConfigurationOutputTypeDef,
    DescribeNotificationConfigurationInputRequestTypeDef,
    DescribeNotificationConfigurationOutputTypeDef,
    DescribeSignalingChannelInputRequestTypeDef,
    DescribeSignalingChannelOutputTypeDef,
    DescribeStreamInputRequestTypeDef,
    DescribeStreamOutputTypeDef,
    GetDataEndpointInputRequestTypeDef,
    GetDataEndpointOutputTypeDef,
    GetSignalingChannelEndpointInputRequestTypeDef,
    GetSignalingChannelEndpointOutputTypeDef,
    ListEdgeAgentConfigurationsInputRequestTypeDef,
    ListEdgeAgentConfigurationsOutputTypeDef,
    ListSignalingChannelsInputRequestTypeDef,
    ListSignalingChannelsOutputTypeDef,
    ListStreamsInputRequestTypeDef,
    ListStreamsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTagsForStreamInputRequestTypeDef,
    ListTagsForStreamOutputTypeDef,
    StartEdgeConfigurationUpdateInputRequestTypeDef,
    StartEdgeConfigurationUpdateOutputTypeDef,
    TagResourceInputRequestTypeDef,
    TagStreamInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UntagStreamInputRequestTypeDef,
    UpdateDataRetentionInputRequestTypeDef,
    UpdateImageGenerationConfigurationInputRequestTypeDef,
    UpdateMediaStorageConfigurationInputRequestTypeDef,
    UpdateNotificationConfigurationInputRequestTypeDef,
    UpdateSignalingChannelInputRequestTypeDef,
    UpdateStreamInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("KinesisVideoClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AccountChannelLimitExceededException: Type[BotocoreClientError]
    AccountStreamLimitExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientLimitExceededException: Type[BotocoreClientError]
    DeviceStreamLimitExceededException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidDeviceException: Type[BotocoreClientError]
    InvalidResourceFormatException: Type[BotocoreClientError]
    NoDataRetentionException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    StreamEdgeConfigurationNotFoundException: Type[BotocoreClientError]
    TagsPerResourceExceededLimitException: Type[BotocoreClientError]
    VersionMismatchException: Type[BotocoreClientError]


class KinesisVideoClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#close)
        """

    def create_signaling_channel(
        self, **kwargs: Unpack[CreateSignalingChannelInputRequestTypeDef]
    ) -> CreateSignalingChannelOutputTypeDef:
        """
        Creates a signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.create_signaling_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#create_signaling_channel)
        """

    def create_stream(
        self, **kwargs: Unpack[CreateStreamInputRequestTypeDef]
    ) -> CreateStreamOutputTypeDef:
        """
        Creates a new Kinesis video stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.create_stream)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#create_stream)
        """

    def delete_edge_configuration(
        self, **kwargs: Unpack[DeleteEdgeConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        An asynchronous API that deletes a stream's existing edge configuration, as
        well as the corresponding media from the Edge
        Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.delete_edge_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#delete_edge_configuration)
        """

    def delete_signaling_channel(
        self, **kwargs: Unpack[DeleteSignalingChannelInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.delete_signaling_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#delete_signaling_channel)
        """

    def delete_stream(self, **kwargs: Unpack[DeleteStreamInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a Kinesis video stream and the data contained in the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.delete_stream)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#delete_stream)
        """

    def describe_edge_configuration(
        self, **kwargs: Unpack[DescribeEdgeConfigurationInputRequestTypeDef]
    ) -> DescribeEdgeConfigurationOutputTypeDef:
        """
        Describes a stream's edge configuration that was set using the
        `StartEdgeConfigurationUpdate` API and the latest status of the edge agent's
        recorder and uploader
        jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.describe_edge_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#describe_edge_configuration)
        """

    def describe_image_generation_configuration(
        self, **kwargs: Unpack[DescribeImageGenerationConfigurationInputRequestTypeDef]
    ) -> DescribeImageGenerationConfigurationOutputTypeDef:
        """
        Gets the `ImageGenerationConfiguration` for a given Kinesis video stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.describe_image_generation_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#describe_image_generation_configuration)
        """

    def describe_mapped_resource_configuration(
        self, **kwargs: Unpack[DescribeMappedResourceConfigurationInputRequestTypeDef]
    ) -> DescribeMappedResourceConfigurationOutputTypeDef:
        """
        Returns the most current information about the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.describe_mapped_resource_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#describe_mapped_resource_configuration)
        """

    def describe_media_storage_configuration(
        self, **kwargs: Unpack[DescribeMediaStorageConfigurationInputRequestTypeDef]
    ) -> DescribeMediaStorageConfigurationOutputTypeDef:
        """
        Returns the most current information about the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.describe_media_storage_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#describe_media_storage_configuration)
        """

    def describe_notification_configuration(
        self, **kwargs: Unpack[DescribeNotificationConfigurationInputRequestTypeDef]
    ) -> DescribeNotificationConfigurationOutputTypeDef:
        """
        Gets the `NotificationConfiguration` for a given Kinesis video stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.describe_notification_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#describe_notification_configuration)
        """

    def describe_signaling_channel(
        self, **kwargs: Unpack[DescribeSignalingChannelInputRequestTypeDef]
    ) -> DescribeSignalingChannelOutputTypeDef:
        """
        Returns the most current information about the signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.describe_signaling_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#describe_signaling_channel)
        """

    def describe_stream(
        self, **kwargs: Unpack[DescribeStreamInputRequestTypeDef]
    ) -> DescribeStreamOutputTypeDef:
        """
        Returns the most current information about the specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.describe_stream)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#describe_stream)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#generate_presigned_url)
        """

    def get_data_endpoint(
        self, **kwargs: Unpack[GetDataEndpointInputRequestTypeDef]
    ) -> GetDataEndpointOutputTypeDef:
        """
        Gets an endpoint for a specified stream for either reading or writing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.get_data_endpoint)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#get_data_endpoint)
        """

    def get_signaling_channel_endpoint(
        self, **kwargs: Unpack[GetSignalingChannelEndpointInputRequestTypeDef]
    ) -> GetSignalingChannelEndpointOutputTypeDef:
        """
        Provides an endpoint for the specified signaling channel to send and receive
        messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.get_signaling_channel_endpoint)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#get_signaling_channel_endpoint)
        """

    def list_edge_agent_configurations(
        self, **kwargs: Unpack[ListEdgeAgentConfigurationsInputRequestTypeDef]
    ) -> ListEdgeAgentConfigurationsOutputTypeDef:
        """
        Returns an array of edge configurations associated with the specified Edge
        Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.list_edge_agent_configurations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#list_edge_agent_configurations)
        """

    def list_signaling_channels(
        self, **kwargs: Unpack[ListSignalingChannelsInputRequestTypeDef]
    ) -> ListSignalingChannelsOutputTypeDef:
        """
        Returns an array of `ChannelInfo` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.list_signaling_channels)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#list_signaling_channels)
        """

    def list_streams(
        self, **kwargs: Unpack[ListStreamsInputRequestTypeDef]
    ) -> ListStreamsOutputTypeDef:
        """
        Returns an array of `StreamInfo` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.list_streams)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#list_streams)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns a list of tags associated with the specified signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#list_tags_for_resource)
        """

    def list_tags_for_stream(
        self, **kwargs: Unpack[ListTagsForStreamInputRequestTypeDef]
    ) -> ListTagsForStreamOutputTypeDef:
        """
        Returns a list of tags associated with the specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.list_tags_for_stream)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#list_tags_for_stream)
        """

    def start_edge_configuration_update(
        self, **kwargs: Unpack[StartEdgeConfigurationUpdateInputRequestTypeDef]
    ) -> StartEdgeConfigurationUpdateOutputTypeDef:
        """
        An asynchronous API that updates a stream's existing edge configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.start_edge_configuration_update)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#start_edge_configuration_update)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to a signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#tag_resource)
        """

    def tag_stream(self, **kwargs: Unpack[TagStreamInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.tag_stream)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#tag_stream)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from a signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#untag_resource)
        """

    def untag_stream(self, **kwargs: Unpack[UntagStreamInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.untag_stream)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#untag_stream)
        """

    def update_data_retention(
        self, **kwargs: Unpack[UpdateDataRetentionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Increases or decreases the stream's data retention period by the value that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.update_data_retention)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#update_data_retention)
        """

    def update_image_generation_configuration(
        self, **kwargs: Unpack[UpdateImageGenerationConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the `StreamInfo` and `ImageProcessingConfiguration` fields.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.update_image_generation_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#update_image_generation_configuration)
        """

    def update_media_storage_configuration(
        self, **kwargs: Unpack[UpdateMediaStorageConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a `SignalingChannel` to a stream to store the media.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.update_media_storage_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#update_media_storage_configuration)
        """

    def update_notification_configuration(
        self, **kwargs: Unpack[UpdateNotificationConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the notification information for a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.update_notification_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#update_notification_configuration)
        """

    def update_signaling_channel(
        self, **kwargs: Unpack[UpdateSignalingChannelInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the existing signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.update_signaling_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#update_signaling_channel)
        """

    def update_stream(self, **kwargs: Unpack[UpdateStreamInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates stream metadata, such as the device name and media type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.update_stream)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#update_stream)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_mapped_resource_configuration"]
    ) -> DescribeMappedResourceConfigurationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_edge_agent_configurations"]
    ) -> ListEdgeAgentConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signaling_channels"]
    ) -> ListSignalingChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_streams"]) -> ListStreamsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/client/#get_paginator)
        """
