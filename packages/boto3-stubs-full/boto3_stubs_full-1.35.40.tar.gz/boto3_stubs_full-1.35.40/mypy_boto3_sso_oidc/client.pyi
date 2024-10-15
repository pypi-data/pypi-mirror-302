"""
Type annotations for sso-oidc service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sso_oidc.client import SSOOIDCClient

    session = Session()
    client: SSOOIDCClient = session.client("sso-oidc")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateTokenRequestRequestTypeDef,
    CreateTokenResponseTypeDef,
    CreateTokenWithIAMRequestRequestTypeDef,
    CreateTokenWithIAMResponseTypeDef,
    RegisterClientRequestRequestTypeDef,
    RegisterClientResponseTypeDef,
    StartDeviceAuthorizationRequestRequestTypeDef,
    StartDeviceAuthorizationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("SSOOIDCClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AuthorizationPendingException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ExpiredTokenException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidClientException: Type[BotocoreClientError]
    InvalidClientMetadataException: Type[BotocoreClientError]
    InvalidGrantException: Type[BotocoreClientError]
    InvalidRedirectUriException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidRequestRegionException: Type[BotocoreClientError]
    InvalidScopeException: Type[BotocoreClientError]
    SlowDownException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]
    UnsupportedGrantTypeException: Type[BotocoreClientError]

class SSOOIDCClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSOOIDCClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/#close)
        """

    def create_token(
        self, **kwargs: Unpack[CreateTokenRequestRequestTypeDef]
    ) -> CreateTokenResponseTypeDef:
        """
        Creates and returns access and refresh tokens for clients that are
        authenticated using client
        secrets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC.Client.create_token)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/#create_token)
        """

    def create_token_with_iam(
        self, **kwargs: Unpack[CreateTokenWithIAMRequestRequestTypeDef]
    ) -> CreateTokenWithIAMResponseTypeDef:
        """
        Creates and returns access and refresh tokens for clients and applications that
        are authenticated using IAM
        entities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC.Client.create_token_with_iam)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/#create_token_with_iam)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/#generate_presigned_url)
        """

    def register_client(
        self, **kwargs: Unpack[RegisterClientRequestRequestTypeDef]
    ) -> RegisterClientResponseTypeDef:
        """
        Registers a client with IAM Identity Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC.Client.register_client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/#register_client)
        """

    def start_device_authorization(
        self, **kwargs: Unpack[StartDeviceAuthorizationRequestRequestTypeDef]
    ) -> StartDeviceAuthorizationResponseTypeDef:
        """
        Initiates device authorization by requesting a pair of verification codes from
        the authorization
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC.Client.start_device_authorization)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/client/#start_device_authorization)
        """
