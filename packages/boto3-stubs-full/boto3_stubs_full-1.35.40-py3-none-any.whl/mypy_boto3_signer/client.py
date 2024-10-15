"""
Type annotations for signer service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_signer.client import SignerClient

    session = Session()
    client: SignerClient = session.client("signer")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListSigningJobsPaginator,
    ListSigningPlatformsPaginator,
    ListSigningProfilesPaginator,
)
from .type_defs import (
    AddProfilePermissionRequestRequestTypeDef,
    AddProfilePermissionResponseTypeDef,
    CancelSigningProfileRequestRequestTypeDef,
    DescribeSigningJobRequestRequestTypeDef,
    DescribeSigningJobResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetRevocationStatusRequestRequestTypeDef,
    GetRevocationStatusResponseTypeDef,
    GetSigningPlatformRequestRequestTypeDef,
    GetSigningPlatformResponseTypeDef,
    GetSigningProfileRequestRequestTypeDef,
    GetSigningProfileResponseTypeDef,
    ListProfilePermissionsRequestRequestTypeDef,
    ListProfilePermissionsResponseTypeDef,
    ListSigningJobsRequestRequestTypeDef,
    ListSigningJobsResponseTypeDef,
    ListSigningPlatformsRequestRequestTypeDef,
    ListSigningPlatformsResponseTypeDef,
    ListSigningProfilesRequestRequestTypeDef,
    ListSigningProfilesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutSigningProfileRequestRequestTypeDef,
    PutSigningProfileResponseTypeDef,
    RemoveProfilePermissionRequestRequestTypeDef,
    RemoveProfilePermissionResponseTypeDef,
    RevokeSignatureRequestRequestTypeDef,
    RevokeSigningProfileRequestRequestTypeDef,
    SignPayloadRequestRequestTypeDef,
    SignPayloadResponseTypeDef,
    StartSigningJobRequestRequestTypeDef,
    StartSigningJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)
from .waiter import SuccessfulSigningJobWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SignerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SignerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SignerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#exceptions)
        """

    def add_profile_permission(
        self, **kwargs: Unpack[AddProfilePermissionRequestRequestTypeDef]
    ) -> AddProfilePermissionResponseTypeDef:
        """
        Adds cross-account permissions to a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.add_profile_permission)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#add_profile_permission)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#can_paginate)
        """

    def cancel_signing_profile(
        self, **kwargs: Unpack[CancelSigningProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of an `ACTIVE` signing profile to `CANCELED`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.cancel_signing_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#cancel_signing_profile)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#close)
        """

    def describe_signing_job(
        self, **kwargs: Unpack[DescribeSigningJobRequestRequestTypeDef]
    ) -> DescribeSigningJobResponseTypeDef:
        """
        Returns information about a specific code signing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.describe_signing_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#describe_signing_job)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#generate_presigned_url)
        """

    def get_revocation_status(
        self, **kwargs: Unpack[GetRevocationStatusRequestRequestTypeDef]
    ) -> GetRevocationStatusResponseTypeDef:
        """
        Retrieves the revocation status of one or more of the signing profile, signing
        job, and signing
        certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.get_revocation_status)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_revocation_status)
        """

    def get_signing_platform(
        self, **kwargs: Unpack[GetSigningPlatformRequestRequestTypeDef]
    ) -> GetSigningPlatformResponseTypeDef:
        """
        Returns information on a specific signing platform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.get_signing_platform)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_signing_platform)
        """

    def get_signing_profile(
        self, **kwargs: Unpack[GetSigningProfileRequestRequestTypeDef]
    ) -> GetSigningProfileResponseTypeDef:
        """
        Returns information on a specific signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.get_signing_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_signing_profile)
        """

    def list_profile_permissions(
        self, **kwargs: Unpack[ListProfilePermissionsRequestRequestTypeDef]
    ) -> ListProfilePermissionsResponseTypeDef:
        """
        Lists the cross-account permissions associated with a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.list_profile_permissions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_profile_permissions)
        """

    def list_signing_jobs(
        self, **kwargs: Unpack[ListSigningJobsRequestRequestTypeDef]
    ) -> ListSigningJobsResponseTypeDef:
        """
        Lists all your signing jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.list_signing_jobs)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_signing_jobs)
        """

    def list_signing_platforms(
        self, **kwargs: Unpack[ListSigningPlatformsRequestRequestTypeDef]
    ) -> ListSigningPlatformsResponseTypeDef:
        """
        Lists all signing platforms available in AWS Signer that match the request
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.list_signing_platforms)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_signing_platforms)
        """

    def list_signing_profiles(
        self, **kwargs: Unpack[ListSigningProfilesRequestRequestTypeDef]
    ) -> ListSigningProfilesResponseTypeDef:
        """
        Lists all available signing profiles in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.list_signing_profiles)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_signing_profiles)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags associated with a signing profile resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_tags_for_resource)
        """

    def put_signing_profile(
        self, **kwargs: Unpack[PutSigningProfileRequestRequestTypeDef]
    ) -> PutSigningProfileResponseTypeDef:
        """
        Creates a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.put_signing_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#put_signing_profile)
        """

    def remove_profile_permission(
        self, **kwargs: Unpack[RemoveProfilePermissionRequestRequestTypeDef]
    ) -> RemoveProfilePermissionResponseTypeDef:
        """
        Removes cross-account permissions from a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.remove_profile_permission)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#remove_profile_permission)
        """

    def revoke_signature(
        self, **kwargs: Unpack[RevokeSignatureRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of a signing job to REVOKED.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.revoke_signature)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#revoke_signature)
        """

    def revoke_signing_profile(
        self, **kwargs: Unpack[RevokeSigningProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of a signing profile to REVOKED.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.revoke_signing_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#revoke_signing_profile)
        """

    def sign_payload(
        self, **kwargs: Unpack[SignPayloadRequestRequestTypeDef]
    ) -> SignPayloadResponseTypeDef:
        """
        Signs a binary payload and returns a signature envelope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.sign_payload)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#sign_payload)
        """

    def start_signing_job(
        self, **kwargs: Unpack[StartSigningJobRequestRequestTypeDef]
    ) -> StartSigningJobResponseTypeDef:
        """
        Initiates a signing job to be performed on the code provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.start_signing_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#start_signing_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signing_jobs"]
    ) -> ListSigningJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signing_platforms"]
    ) -> ListSigningPlatformsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signing_profiles"]
    ) -> ListSigningProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_paginator)
        """

    def get_waiter(
        self, waiter_name: Literal["successful_signing_job"]
    ) -> SuccessfulSigningJobWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_waiter)
        """
