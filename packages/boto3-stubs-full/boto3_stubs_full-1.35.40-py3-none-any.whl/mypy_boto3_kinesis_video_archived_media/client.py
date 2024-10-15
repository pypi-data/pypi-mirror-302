"""
Type annotations for kinesis-video-archived-media service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient

    session = Session()
    client: KinesisVideoArchivedMediaClient = session.client("kinesis-video-archived-media")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import GetImagesPaginator, ListFragmentsPaginator
from .type_defs import (
    GetClipInputRequestTypeDef,
    GetClipOutputTypeDef,
    GetDASHStreamingSessionURLInputRequestTypeDef,
    GetDASHStreamingSessionURLOutputTypeDef,
    GetHLSStreamingSessionURLInputRequestTypeDef,
    GetHLSStreamingSessionURLOutputTypeDef,
    GetImagesInputRequestTypeDef,
    GetImagesOutputTypeDef,
    GetMediaForFragmentListInputRequestTypeDef,
    GetMediaForFragmentListOutputTypeDef,
    ListFragmentsInputRequestTypeDef,
    ListFragmentsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("KinesisVideoArchivedMediaClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClientLimitExceededException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidCodecPrivateDataException: Type[BotocoreClientError]
    InvalidMediaFrameException: Type[BotocoreClientError]
    MissingCodecPrivateDataException: Type[BotocoreClientError]
    NoDataRetentionException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    UnsupportedStreamMediaTypeException: Type[BotocoreClientError]


class KinesisVideoArchivedMediaClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoArchivedMediaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#close)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#generate_presigned_url)
        """

    def get_clip(self, **kwargs: Unpack[GetClipInputRequestTypeDef]) -> GetClipOutputTypeDef:
        """
        Downloads an MP4 file (clip) containing the archived, on-demand media from the
        specified video stream over the specified time
        range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_clip)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#get_clip)
        """

    def get_dash_streaming_session_url(
        self, **kwargs: Unpack[GetDASHStreamingSessionURLInputRequestTypeDef]
    ) -> GetDASHStreamingSessionURLOutputTypeDef:
        """
        Retrieves an MPEG Dynamic Adaptive Streaming over HTTP (DASH) URL for the
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_dash_streaming_session_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#get_dash_streaming_session_url)
        """

    def get_hls_streaming_session_url(
        self, **kwargs: Unpack[GetHLSStreamingSessionURLInputRequestTypeDef]
    ) -> GetHLSStreamingSessionURLOutputTypeDef:
        """
        Retrieves an HTTP Live Streaming (HLS) URL for the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_hls_streaming_session_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#get_hls_streaming_session_url)
        """

    def get_images(self, **kwargs: Unpack[GetImagesInputRequestTypeDef]) -> GetImagesOutputTypeDef:
        """
        Retrieves a list of images corresponding to each timestamp for a given time
        range, sampling interval, and image format
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_images)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#get_images)
        """

    def get_media_for_fragment_list(
        self, **kwargs: Unpack[GetMediaForFragmentListInputRequestTypeDef]
    ) -> GetMediaForFragmentListOutputTypeDef:
        """
        Gets media for a list of fragments (specified by fragment number) from the
        archived data in an Amazon Kinesis video
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_media_for_fragment_list)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#get_media_for_fragment_list)
        """

    def list_fragments(
        self, **kwargs: Unpack[ListFragmentsInputRequestTypeDef]
    ) -> ListFragmentsOutputTypeDef:
        """
        Returns a list of  Fragment objects from the specified stream and timestamp
        range within the archived
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.list_fragments)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#list_fragments)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_images"]) -> GetImagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fragments"]) -> ListFragmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client/#get_paginator)
        """
