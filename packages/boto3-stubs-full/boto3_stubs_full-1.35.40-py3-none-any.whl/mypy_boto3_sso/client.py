"""
Type annotations for sso service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sso.client import SSOClient

    session = Session()
    client: SSOClient = session.client("sso")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListAccountRolesPaginator, ListAccountsPaginator
from .type_defs import (
    EmptyResponseMetadataTypeDef,
    GetRoleCredentialsRequestRequestTypeDef,
    GetRoleCredentialsResponseTypeDef,
    ListAccountRolesRequestRequestTypeDef,
    ListAccountRolesResponseTypeDef,
    ListAccountsRequestRequestTypeDef,
    ListAccountsResponseTypeDef,
    LogoutRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SSOClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class SSOClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSOClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#close)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#generate_presigned_url)
        """

    def get_role_credentials(
        self, **kwargs: Unpack[GetRoleCredentialsRequestRequestTypeDef]
    ) -> GetRoleCredentialsResponseTypeDef:
        """
        Returns the STS short-term credentials for a given role name that is assigned
        to the
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.get_role_credentials)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#get_role_credentials)
        """

    def list_account_roles(
        self, **kwargs: Unpack[ListAccountRolesRequestRequestTypeDef]
    ) -> ListAccountRolesResponseTypeDef:
        """
        Lists all roles that are assigned to the user for a given AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.list_account_roles)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#list_account_roles)
        """

    def list_accounts(
        self, **kwargs: Unpack[ListAccountsRequestRequestTypeDef]
    ) -> ListAccountsResponseTypeDef:
        """
        Lists all AWS accounts assigned to the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.list_accounts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#list_accounts)
        """

    def logout(self, **kwargs: Unpack[LogoutRequestRequestTypeDef]) -> EmptyResponseMetadataTypeDef:
        """
        Removes the locally stored SSO tokens from the client-side cache and sends an
        API call to the IAM Identity Center service to invalidate the corresponding
        server-side IAM Identity Center sign in
        session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.logout)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#logout)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_roles"]
    ) -> ListAccountRolesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_accounts"]) -> ListAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/client/#get_paginator)
        """
