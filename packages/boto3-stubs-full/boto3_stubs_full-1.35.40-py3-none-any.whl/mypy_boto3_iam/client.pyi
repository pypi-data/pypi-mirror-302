"""
Type annotations for iam service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iam.client import IAMClient

    session = Session()
    client: IAMClient = session.client("iam")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetAccountAuthorizationDetailsPaginator,
    GetGroupPaginator,
    ListAccessKeysPaginator,
    ListAccountAliasesPaginator,
    ListAttachedGroupPoliciesPaginator,
    ListAttachedRolePoliciesPaginator,
    ListAttachedUserPoliciesPaginator,
    ListEntitiesForPolicyPaginator,
    ListGroupPoliciesPaginator,
    ListGroupsForUserPaginator,
    ListGroupsPaginator,
    ListInstanceProfilesForRolePaginator,
    ListInstanceProfilesPaginator,
    ListInstanceProfileTagsPaginator,
    ListMFADevicesPaginator,
    ListMFADeviceTagsPaginator,
    ListOpenIDConnectProviderTagsPaginator,
    ListPoliciesPaginator,
    ListPolicyTagsPaginator,
    ListPolicyVersionsPaginator,
    ListRolePoliciesPaginator,
    ListRolesPaginator,
    ListRoleTagsPaginator,
    ListSAMLProviderTagsPaginator,
    ListServerCertificatesPaginator,
    ListServerCertificateTagsPaginator,
    ListSigningCertificatesPaginator,
    ListSSHPublicKeysPaginator,
    ListUserPoliciesPaginator,
    ListUsersPaginator,
    ListUserTagsPaginator,
    ListVirtualMFADevicesPaginator,
    SimulateCustomPolicyPaginator,
    SimulatePrincipalPolicyPaginator,
)
from .type_defs import (
    AddClientIDToOpenIDConnectProviderRequestRequestTypeDef,
    AddRoleToInstanceProfileRequestRequestTypeDef,
    AddUserToGroupRequestRequestTypeDef,
    AttachGroupPolicyRequestRequestTypeDef,
    AttachRolePolicyRequestRequestTypeDef,
    AttachUserPolicyRequestRequestTypeDef,
    ChangePasswordRequestRequestTypeDef,
    CreateAccessKeyRequestRequestTypeDef,
    CreateAccessKeyResponseTypeDef,
    CreateAccountAliasRequestRequestTypeDef,
    CreateGroupRequestRequestTypeDef,
    CreateGroupResponseTypeDef,
    CreateInstanceProfileRequestRequestTypeDef,
    CreateInstanceProfileResponseTypeDef,
    CreateLoginProfileRequestRequestTypeDef,
    CreateLoginProfileResponseTypeDef,
    CreateOpenIDConnectProviderRequestRequestTypeDef,
    CreateOpenIDConnectProviderResponseTypeDef,
    CreatePolicyRequestRequestTypeDef,
    CreatePolicyResponseTypeDef,
    CreatePolicyVersionRequestRequestTypeDef,
    CreatePolicyVersionResponseTypeDef,
    CreateRoleRequestRequestTypeDef,
    CreateRoleResponseTypeDef,
    CreateSAMLProviderRequestRequestTypeDef,
    CreateSAMLProviderResponseTypeDef,
    CreateServiceLinkedRoleRequestRequestTypeDef,
    CreateServiceLinkedRoleResponseTypeDef,
    CreateServiceSpecificCredentialRequestRequestTypeDef,
    CreateServiceSpecificCredentialResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResponseTypeDef,
    CreateVirtualMFADeviceRequestRequestTypeDef,
    CreateVirtualMFADeviceResponseTypeDef,
    DeactivateMFADeviceRequestRequestTypeDef,
    DeleteAccessKeyRequestRequestTypeDef,
    DeleteAccountAliasRequestRequestTypeDef,
    DeleteGroupPolicyRequestRequestTypeDef,
    DeleteGroupRequestRequestTypeDef,
    DeleteInstanceProfileRequestRequestTypeDef,
    DeleteLoginProfileRequestRequestTypeDef,
    DeleteOpenIDConnectProviderRequestRequestTypeDef,
    DeletePolicyRequestRequestTypeDef,
    DeletePolicyVersionRequestRequestTypeDef,
    DeleteRolePermissionsBoundaryRequestRequestTypeDef,
    DeleteRolePolicyRequestRequestTypeDef,
    DeleteRoleRequestRequestTypeDef,
    DeleteSAMLProviderRequestRequestTypeDef,
    DeleteServerCertificateRequestRequestTypeDef,
    DeleteServiceLinkedRoleRequestRequestTypeDef,
    DeleteServiceLinkedRoleResponseTypeDef,
    DeleteServiceSpecificCredentialRequestRequestTypeDef,
    DeleteSigningCertificateRequestRequestTypeDef,
    DeleteSSHPublicKeyRequestRequestTypeDef,
    DeleteUserPermissionsBoundaryRequestRequestTypeDef,
    DeleteUserPolicyRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DeleteVirtualMFADeviceRequestRequestTypeDef,
    DetachGroupPolicyRequestRequestTypeDef,
    DetachRolePolicyRequestRequestTypeDef,
    DetachUserPolicyRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableMFADeviceRequestRequestTypeDef,
    GenerateCredentialReportResponseTypeDef,
    GenerateOrganizationsAccessReportRequestRequestTypeDef,
    GenerateOrganizationsAccessReportResponseTypeDef,
    GenerateServiceLastAccessedDetailsRequestRequestTypeDef,
    GenerateServiceLastAccessedDetailsResponseTypeDef,
    GetAccessKeyLastUsedRequestRequestTypeDef,
    GetAccessKeyLastUsedResponseTypeDef,
    GetAccountAuthorizationDetailsRequestRequestTypeDef,
    GetAccountAuthorizationDetailsResponseTypeDef,
    GetAccountPasswordPolicyResponseTypeDef,
    GetAccountSummaryResponseTypeDef,
    GetContextKeysForCustomPolicyRequestRequestTypeDef,
    GetContextKeysForPolicyResponseTypeDef,
    GetContextKeysForPrincipalPolicyRequestRequestTypeDef,
    GetCredentialReportResponseTypeDef,
    GetGroupPolicyRequestRequestTypeDef,
    GetGroupPolicyResponseTypeDef,
    GetGroupRequestRequestTypeDef,
    GetGroupResponseTypeDef,
    GetInstanceProfileRequestRequestTypeDef,
    GetInstanceProfileResponseTypeDef,
    GetLoginProfileRequestRequestTypeDef,
    GetLoginProfileResponseTypeDef,
    GetMFADeviceRequestRequestTypeDef,
    GetMFADeviceResponseTypeDef,
    GetOpenIDConnectProviderRequestRequestTypeDef,
    GetOpenIDConnectProviderResponseTypeDef,
    GetOrganizationsAccessReportRequestRequestTypeDef,
    GetOrganizationsAccessReportResponseTypeDef,
    GetPolicyRequestRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetPolicyVersionRequestRequestTypeDef,
    GetPolicyVersionResponseTypeDef,
    GetRolePolicyRequestRequestTypeDef,
    GetRolePolicyResponseTypeDef,
    GetRoleRequestRequestTypeDef,
    GetRoleResponseTypeDef,
    GetSAMLProviderRequestRequestTypeDef,
    GetSAMLProviderResponseTypeDef,
    GetServerCertificateRequestRequestTypeDef,
    GetServerCertificateResponseTypeDef,
    GetServiceLastAccessedDetailsRequestRequestTypeDef,
    GetServiceLastAccessedDetailsResponseTypeDef,
    GetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef,
    GetServiceLastAccessedDetailsWithEntitiesResponseTypeDef,
    GetServiceLinkedRoleDeletionStatusRequestRequestTypeDef,
    GetServiceLinkedRoleDeletionStatusResponseTypeDef,
    GetSSHPublicKeyRequestRequestTypeDef,
    GetSSHPublicKeyResponseTypeDef,
    GetUserPolicyRequestRequestTypeDef,
    GetUserPolicyResponseTypeDef,
    GetUserRequestRequestTypeDef,
    GetUserResponseTypeDef,
    ListAccessKeysRequestRequestTypeDef,
    ListAccessKeysResponseTypeDef,
    ListAccountAliasesRequestRequestTypeDef,
    ListAccountAliasesResponseTypeDef,
    ListAttachedGroupPoliciesRequestRequestTypeDef,
    ListAttachedGroupPoliciesResponseTypeDef,
    ListAttachedRolePoliciesRequestRequestTypeDef,
    ListAttachedRolePoliciesResponseTypeDef,
    ListAttachedUserPoliciesRequestRequestTypeDef,
    ListAttachedUserPoliciesResponseTypeDef,
    ListEntitiesForPolicyRequestRequestTypeDef,
    ListEntitiesForPolicyResponseTypeDef,
    ListGroupPoliciesRequestRequestTypeDef,
    ListGroupPoliciesResponseTypeDef,
    ListGroupsForUserRequestRequestTypeDef,
    ListGroupsForUserResponseTypeDef,
    ListGroupsRequestRequestTypeDef,
    ListGroupsResponseTypeDef,
    ListInstanceProfilesForRoleRequestRequestTypeDef,
    ListInstanceProfilesForRoleResponseTypeDef,
    ListInstanceProfilesRequestRequestTypeDef,
    ListInstanceProfilesResponseTypeDef,
    ListInstanceProfileTagsRequestRequestTypeDef,
    ListInstanceProfileTagsResponseTypeDef,
    ListMFADevicesRequestRequestTypeDef,
    ListMFADevicesResponseTypeDef,
    ListMFADeviceTagsRequestRequestTypeDef,
    ListMFADeviceTagsResponseTypeDef,
    ListOpenIDConnectProvidersResponseTypeDef,
    ListOpenIDConnectProviderTagsRequestRequestTypeDef,
    ListOpenIDConnectProviderTagsResponseTypeDef,
    ListPoliciesGrantingServiceAccessRequestRequestTypeDef,
    ListPoliciesGrantingServiceAccessResponseTypeDef,
    ListPoliciesRequestRequestTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyTagsRequestRequestTypeDef,
    ListPolicyTagsResponseTypeDef,
    ListPolicyVersionsRequestRequestTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListRolePoliciesRequestRequestTypeDef,
    ListRolePoliciesResponseTypeDef,
    ListRolesRequestRequestTypeDef,
    ListRolesResponseTypeDef,
    ListRoleTagsRequestRequestTypeDef,
    ListRoleTagsResponseTypeDef,
    ListSAMLProvidersResponseTypeDef,
    ListSAMLProviderTagsRequestRequestTypeDef,
    ListSAMLProviderTagsResponseTypeDef,
    ListServerCertificatesRequestRequestTypeDef,
    ListServerCertificatesResponseTypeDef,
    ListServerCertificateTagsRequestRequestTypeDef,
    ListServerCertificateTagsResponseTypeDef,
    ListServiceSpecificCredentialsRequestRequestTypeDef,
    ListServiceSpecificCredentialsResponseTypeDef,
    ListSigningCertificatesRequestRequestTypeDef,
    ListSigningCertificatesResponseTypeDef,
    ListSSHPublicKeysRequestRequestTypeDef,
    ListSSHPublicKeysResponseTypeDef,
    ListUserPoliciesRequestRequestTypeDef,
    ListUserPoliciesResponseTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResponseTypeDef,
    ListUserTagsRequestRequestTypeDef,
    ListUserTagsResponseTypeDef,
    ListVirtualMFADevicesRequestRequestTypeDef,
    ListVirtualMFADevicesResponseTypeDef,
    PutGroupPolicyRequestRequestTypeDef,
    PutRolePermissionsBoundaryRequestRequestTypeDef,
    PutRolePolicyRequestRequestTypeDef,
    PutUserPermissionsBoundaryRequestRequestTypeDef,
    PutUserPolicyRequestRequestTypeDef,
    RemoveClientIDFromOpenIDConnectProviderRequestRequestTypeDef,
    RemoveRoleFromInstanceProfileRequestRequestTypeDef,
    RemoveUserFromGroupRequestRequestTypeDef,
    ResetServiceSpecificCredentialRequestRequestTypeDef,
    ResetServiceSpecificCredentialResponseTypeDef,
    ResyncMFADeviceRequestRequestTypeDef,
    SetDefaultPolicyVersionRequestRequestTypeDef,
    SetSecurityTokenServicePreferencesRequestRequestTypeDef,
    SimulateCustomPolicyRequestRequestTypeDef,
    SimulatePolicyResponseTypeDef,
    SimulatePrincipalPolicyRequestRequestTypeDef,
    TagInstanceProfileRequestRequestTypeDef,
    TagMFADeviceRequestRequestTypeDef,
    TagOpenIDConnectProviderRequestRequestTypeDef,
    TagPolicyRequestRequestTypeDef,
    TagRoleRequestRequestTypeDef,
    TagSAMLProviderRequestRequestTypeDef,
    TagServerCertificateRequestRequestTypeDef,
    TagUserRequestRequestTypeDef,
    UntagInstanceProfileRequestRequestTypeDef,
    UntagMFADeviceRequestRequestTypeDef,
    UntagOpenIDConnectProviderRequestRequestTypeDef,
    UntagPolicyRequestRequestTypeDef,
    UntagRoleRequestRequestTypeDef,
    UntagSAMLProviderRequestRequestTypeDef,
    UntagServerCertificateRequestRequestTypeDef,
    UntagUserRequestRequestTypeDef,
    UpdateAccessKeyRequestRequestTypeDef,
    UpdateAccountPasswordPolicyRequestRequestTypeDef,
    UpdateAssumeRolePolicyRequestRequestTypeDef,
    UpdateGroupRequestRequestTypeDef,
    UpdateLoginProfileRequestRequestTypeDef,
    UpdateOpenIDConnectProviderThumbprintRequestRequestTypeDef,
    UpdateRoleDescriptionRequestRequestTypeDef,
    UpdateRoleDescriptionResponseTypeDef,
    UpdateRoleRequestRequestTypeDef,
    UpdateSAMLProviderRequestRequestTypeDef,
    UpdateSAMLProviderResponseTypeDef,
    UpdateServerCertificateRequestRequestTypeDef,
    UpdateServiceSpecificCredentialRequestRequestTypeDef,
    UpdateSigningCertificateRequestRequestTypeDef,
    UpdateSSHPublicKeyRequestRequestTypeDef,
    UpdateUserRequestRequestTypeDef,
    UploadServerCertificateRequestRequestTypeDef,
    UploadServerCertificateResponseTypeDef,
    UploadSigningCertificateRequestRequestTypeDef,
    UploadSigningCertificateResponseTypeDef,
    UploadSSHPublicKeyRequestRequestTypeDef,
    UploadSSHPublicKeyResponseTypeDef,
)
from .waiter import (
    InstanceProfileExistsWaiter,
    PolicyExistsWaiter,
    RoleExistsWaiter,
    UserExistsWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("IAMClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    CredentialReportExpiredException: Type[BotocoreClientError]
    CredentialReportNotPresentException: Type[BotocoreClientError]
    CredentialReportNotReadyException: Type[BotocoreClientError]
    DeleteConflictException: Type[BotocoreClientError]
    DuplicateCertificateException: Type[BotocoreClientError]
    DuplicateSSHPublicKeyException: Type[BotocoreClientError]
    EntityAlreadyExistsException: Type[BotocoreClientError]
    EntityTemporarilyUnmodifiableException: Type[BotocoreClientError]
    InvalidAuthenticationCodeException: Type[BotocoreClientError]
    InvalidCertificateException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidPublicKeyException: Type[BotocoreClientError]
    InvalidUserTypeException: Type[BotocoreClientError]
    KeyPairMismatchException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedCertificateException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    NoSuchEntityException: Type[BotocoreClientError]
    OpenIdIdpCommunicationErrorException: Type[BotocoreClientError]
    PasswordPolicyViolationException: Type[BotocoreClientError]
    PolicyEvaluationException: Type[BotocoreClientError]
    PolicyNotAttachableException: Type[BotocoreClientError]
    ReportGenerationLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceNotSupportedException: Type[BotocoreClientError]
    UnmodifiableEntityException: Type[BotocoreClientError]
    UnrecognizedPublicKeyEncodingException: Type[BotocoreClientError]

class IAMClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IAMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#exceptions)
        """

    def add_client_id_to_open_id_connect_provider(
        self, **kwargs: Unpack[AddClientIDToOpenIDConnectProviderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds a new client ID (also known as audience) to the list of client IDs already
        registered for the specified IAM OpenID Connect (OIDC) provider
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.add_client_id_to_open_id_connect_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#add_client_id_to_open_id_connect_provider)
        """

    def add_role_to_instance_profile(
        self, **kwargs: Unpack[AddRoleToInstanceProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds the specified IAM role to the specified instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.add_role_to_instance_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#add_role_to_instance_profile)
        """

    def add_user_to_group(
        self, **kwargs: Unpack[AddUserToGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds the specified user to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.add_user_to_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#add_user_to_group)
        """

    def attach_group_policy(
        self, **kwargs: Unpack[AttachGroupPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches the specified managed policy to the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.attach_group_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#attach_group_policy)
        """

    def attach_role_policy(
        self, **kwargs: Unpack[AttachRolePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches the specified managed policy to the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.attach_role_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#attach_role_policy)
        """

    def attach_user_policy(
        self, **kwargs: Unpack[AttachUserPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches the specified managed policy to the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.attach_user_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#attach_user_policy)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#can_paginate)
        """

    def change_password(
        self, **kwargs: Unpack[ChangePasswordRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the password of the IAM user who is calling this operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.change_password)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#change_password)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#close)
        """

    def create_access_key(
        self, **kwargs: Unpack[CreateAccessKeyRequestRequestTypeDef]
    ) -> CreateAccessKeyResponseTypeDef:
        """
        Creates a new Amazon Web Services secret access key and corresponding Amazon
        Web Services access key ID for the specified
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_access_key)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_access_key)
        """

    def create_account_alias(
        self, **kwargs: Unpack[CreateAccountAliasRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates an alias for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_account_alias)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_account_alias)
        """

    def create_group(
        self, **kwargs: Unpack[CreateGroupRequestRequestTypeDef]
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a new group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_group)
        """

    def create_instance_profile(
        self, **kwargs: Unpack[CreateInstanceProfileRequestRequestTypeDef]
    ) -> CreateInstanceProfileResponseTypeDef:
        """
        Creates a new instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_instance_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_instance_profile)
        """

    def create_login_profile(
        self, **kwargs: Unpack[CreateLoginProfileRequestRequestTypeDef]
    ) -> CreateLoginProfileResponseTypeDef:
        """
        Creates a password for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_login_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_login_profile)
        """

    def create_open_id_connect_provider(
        self, **kwargs: Unpack[CreateOpenIDConnectProviderRequestRequestTypeDef]
    ) -> CreateOpenIDConnectProviderResponseTypeDef:
        """
        Creates an IAM entity to describe an identity provider (IdP) that supports
        `OpenID Connect (OIDC)
        <http://openid.net/connect/>`__.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_open_id_connect_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_open_id_connect_provider)
        """

    def create_policy(
        self, **kwargs: Unpack[CreatePolicyRequestRequestTypeDef]
    ) -> CreatePolicyResponseTypeDef:
        """
        Creates a new managed policy for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_policy)
        """

    def create_policy_version(
        self, **kwargs: Unpack[CreatePolicyVersionRequestRequestTypeDef]
    ) -> CreatePolicyVersionResponseTypeDef:
        """
        Creates a new version of the specified managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_policy_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_policy_version)
        """

    def create_role(
        self, **kwargs: Unpack[CreateRoleRequestRequestTypeDef]
    ) -> CreateRoleResponseTypeDef:
        """
        Creates a new role for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_role)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_role)
        """

    def create_saml_provider(
        self, **kwargs: Unpack[CreateSAMLProviderRequestRequestTypeDef]
    ) -> CreateSAMLProviderResponseTypeDef:
        """
        Creates an IAM resource that describes an identity provider (IdP) that supports
        SAML
        2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_saml_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_saml_provider)
        """

    def create_service_linked_role(
        self, **kwargs: Unpack[CreateServiceLinkedRoleRequestRequestTypeDef]
    ) -> CreateServiceLinkedRoleResponseTypeDef:
        """
        Creates an IAM role that is linked to a specific Amazon Web Services service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_service_linked_role)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_service_linked_role)
        """

    def create_service_specific_credential(
        self, **kwargs: Unpack[CreateServiceSpecificCredentialRequestRequestTypeDef]
    ) -> CreateServiceSpecificCredentialResponseTypeDef:
        """
        Generates a set of credentials consisting of a user name and password that can
        be used to access the service specified in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_service_specific_credential)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_service_specific_credential)
        """

    def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a new IAM user for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_user)
        """

    def create_virtual_mfa_device(
        self, **kwargs: Unpack[CreateVirtualMFADeviceRequestRequestTypeDef]
    ) -> CreateVirtualMFADeviceResponseTypeDef:
        """
        Creates a new virtual MFA device for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_virtual_mfa_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#create_virtual_mfa_device)
        """

    def deactivate_mfa_device(
        self, **kwargs: Unpack[DeactivateMFADeviceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deactivates the specified MFA device and removes it from association with the
        user name for which it was originally
        enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.deactivate_mfa_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#deactivate_mfa_device)
        """

    def delete_access_key(
        self, **kwargs: Unpack[DeleteAccessKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the access key pair associated with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_access_key)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_access_key)
        """

    def delete_account_alias(
        self, **kwargs: Unpack[DeleteAccountAliasRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Web Services account alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_account_alias)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_account_alias)
        """

    def delete_account_password_policy(self) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the password policy for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_account_password_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_account_password_policy)
        """

    def delete_group(
        self, **kwargs: Unpack[DeleteGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_group)
        """

    def delete_group_policy(
        self, **kwargs: Unpack[DeleteGroupPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified inline policy that is embedded in the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_group_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_group_policy)
        """

    def delete_instance_profile(
        self, **kwargs: Unpack[DeleteInstanceProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_instance_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_instance_profile)
        """

    def delete_login_profile(
        self, **kwargs: Unpack[DeleteLoginProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the password for the specified IAM user, For more information, see
        [Managing passwords for IAM
        users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_admin-change-user.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_login_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_login_profile)
        """

    def delete_open_id_connect_provider(
        self, **kwargs: Unpack[DeleteOpenIDConnectProviderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an OpenID Connect identity provider (IdP) resource object in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_open_id_connect_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_open_id_connect_provider)
        """

    def delete_policy(
        self, **kwargs: Unpack[DeletePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_policy)
        """

    def delete_policy_version(
        self, **kwargs: Unpack[DeletePolicyVersionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified version from the specified managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_policy_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_policy_version)
        """

    def delete_role(
        self, **kwargs: Unpack[DeleteRoleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_role)
        """

    def delete_role_permissions_boundary(
        self, **kwargs: Unpack[DeleteRolePermissionsBoundaryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the permissions boundary for the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role_permissions_boundary)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_role_permissions_boundary)
        """

    def delete_role_policy(
        self, **kwargs: Unpack[DeleteRolePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified inline policy that is embedded in the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_role_policy)
        """

    def delete_saml_provider(
        self, **kwargs: Unpack[DeleteSAMLProviderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a SAML provider resource in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_saml_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_saml_provider)
        """

    def delete_server_certificate(
        self, **kwargs: Unpack[DeleteServerCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified server certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_server_certificate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_server_certificate)
        """

    def delete_service_linked_role(
        self, **kwargs: Unpack[DeleteServiceLinkedRoleRequestRequestTypeDef]
    ) -> DeleteServiceLinkedRoleResponseTypeDef:
        """
        Submits a service-linked role deletion request and returns a `DeletionTaskId`,
        which you can use to check the status of the
        deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_service_linked_role)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_service_linked_role)
        """

    def delete_service_specific_credential(
        self, **kwargs: Unpack[DeleteServiceSpecificCredentialRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified service-specific credential.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_service_specific_credential)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_service_specific_credential)
        """

    def delete_signing_certificate(
        self, **kwargs: Unpack[DeleteSigningCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a signing certificate associated with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_signing_certificate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_signing_certificate)
        """

    def delete_ssh_public_key(
        self, **kwargs: Unpack[DeleteSSHPublicKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified SSH public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_ssh_public_key)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_ssh_public_key)
        """

    def delete_user(
        self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_user)
        """

    def delete_user_permissions_boundary(
        self, **kwargs: Unpack[DeleteUserPermissionsBoundaryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the permissions boundary for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_user_permissions_boundary)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_user_permissions_boundary)
        """

    def delete_user_policy(
        self, **kwargs: Unpack[DeleteUserPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified inline policy that is embedded in the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_user_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_user_policy)
        """

    def delete_virtual_mfa_device(
        self, **kwargs: Unpack[DeleteVirtualMFADeviceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a virtual MFA device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_virtual_mfa_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#delete_virtual_mfa_device)
        """

    def detach_group_policy(
        self, **kwargs: Unpack[DetachGroupPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified managed policy from the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.detach_group_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#detach_group_policy)
        """

    def detach_role_policy(
        self, **kwargs: Unpack[DetachRolePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified managed policy from the specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.detach_role_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#detach_role_policy)
        """

    def detach_user_policy(
        self, **kwargs: Unpack[DetachUserPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified managed policy from the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.detach_user_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#detach_user_policy)
        """

    def enable_mfa_device(
        self, **kwargs: Unpack[EnableMFADeviceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables the specified MFA device and associates it with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.enable_mfa_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#enable_mfa_device)
        """

    def generate_credential_report(self) -> GenerateCredentialReportResponseTypeDef:
        """
        Generates a credential report for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.generate_credential_report)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#generate_credential_report)
        """

    def generate_organizations_access_report(
        self, **kwargs: Unpack[GenerateOrganizationsAccessReportRequestRequestTypeDef]
    ) -> GenerateOrganizationsAccessReportResponseTypeDef:
        """
        Generates a report for service last accessed data for Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.generate_organizations_access_report)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#generate_organizations_access_report)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#generate_presigned_url)
        """

    def generate_service_last_accessed_details(
        self, **kwargs: Unpack[GenerateServiceLastAccessedDetailsRequestRequestTypeDef]
    ) -> GenerateServiceLastAccessedDetailsResponseTypeDef:
        """
        Generates a report that includes details about when an IAM resource (user,
        group, role, or policy) was last used in an attempt to access Amazon Web
        Services
        services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.generate_service_last_accessed_details)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#generate_service_last_accessed_details)
        """

    def get_access_key_last_used(
        self, **kwargs: Unpack[GetAccessKeyLastUsedRequestRequestTypeDef]
    ) -> GetAccessKeyLastUsedResponseTypeDef:
        """
        Retrieves information about when the specified access key was last used.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_access_key_last_used)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_access_key_last_used)
        """

    def get_account_authorization_details(
        self, **kwargs: Unpack[GetAccountAuthorizationDetailsRequestRequestTypeDef]
    ) -> GetAccountAuthorizationDetailsResponseTypeDef:
        """
        Retrieves information about all IAM users, groups, roles, and policies in your
        Amazon Web Services account, including their relationships to one
        another.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_account_authorization_details)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_account_authorization_details)
        """

    def get_account_password_policy(self) -> GetAccountPasswordPolicyResponseTypeDef:
        """
        Retrieves the password policy for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_account_password_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_account_password_policy)
        """

    def get_account_summary(self) -> GetAccountSummaryResponseTypeDef:
        """
        Retrieves information about IAM entity usage and IAM quotas in the Amazon Web
        Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_account_summary)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_account_summary)
        """

    def get_context_keys_for_custom_policy(
        self, **kwargs: Unpack[GetContextKeysForCustomPolicyRequestRequestTypeDef]
    ) -> GetContextKeysForPolicyResponseTypeDef:
        """
        Gets a list of all of the context keys referenced in the input policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_context_keys_for_custom_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_context_keys_for_custom_policy)
        """

    def get_context_keys_for_principal_policy(
        self, **kwargs: Unpack[GetContextKeysForPrincipalPolicyRequestRequestTypeDef]
    ) -> GetContextKeysForPolicyResponseTypeDef:
        """
        Gets a list of all of the context keys referenced in all the IAM policies that
        are attached to the specified IAM
        entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_context_keys_for_principal_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_context_keys_for_principal_policy)
        """

    def get_credential_report(self) -> GetCredentialReportResponseTypeDef:
        """
        Retrieves a credential report for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_credential_report)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_credential_report)
        """

    def get_group(self, **kwargs: Unpack[GetGroupRequestRequestTypeDef]) -> GetGroupResponseTypeDef:
        """
        Returns a list of IAM users that are in the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_group)
        """

    def get_group_policy(
        self, **kwargs: Unpack[GetGroupPolicyRequestRequestTypeDef]
    ) -> GetGroupPolicyResponseTypeDef:
        """
        Retrieves the specified inline policy document that is embedded in the
        specified IAM
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_group_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_group_policy)
        """

    def get_instance_profile(
        self, **kwargs: Unpack[GetInstanceProfileRequestRequestTypeDef]
    ) -> GetInstanceProfileResponseTypeDef:
        """
        Retrieves information about the specified instance profile, including the
        instance profile's path, GUID, ARN, and
        role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_instance_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_instance_profile)
        """

    def get_login_profile(
        self, **kwargs: Unpack[GetLoginProfileRequestRequestTypeDef]
    ) -> GetLoginProfileResponseTypeDef:
        """
        Retrieves the user name for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_login_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_login_profile)
        """

    def get_mfa_device(
        self, **kwargs: Unpack[GetMFADeviceRequestRequestTypeDef]
    ) -> GetMFADeviceResponseTypeDef:
        """
        Retrieves information about an MFA device for a specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_mfa_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_mfa_device)
        """

    def get_open_id_connect_provider(
        self, **kwargs: Unpack[GetOpenIDConnectProviderRequestRequestTypeDef]
    ) -> GetOpenIDConnectProviderResponseTypeDef:
        """
        Returns information about the specified OpenID Connect (OIDC) provider resource
        object in
        IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_open_id_connect_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_open_id_connect_provider)
        """

    def get_organizations_access_report(
        self, **kwargs: Unpack[GetOrganizationsAccessReportRequestRequestTypeDef]
    ) -> GetOrganizationsAccessReportResponseTypeDef:
        """
        Retrieves the service last accessed data report for Organizations that was
        previously generated using the `GenerateOrganizationsAccessReport`
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_organizations_access_report)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_organizations_access_report)
        """

    def get_policy(
        self, **kwargs: Unpack[GetPolicyRequestRequestTypeDef]
    ) -> GetPolicyResponseTypeDef:
        """
        Retrieves information about the specified managed policy, including the
        policy's default version and the total number of IAM users, groups, and roles
        to which the policy is
        attached.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_policy)
        """

    def get_policy_version(
        self, **kwargs: Unpack[GetPolicyVersionRequestRequestTypeDef]
    ) -> GetPolicyVersionResponseTypeDef:
        """
        Retrieves information about the specified version of the specified managed
        policy, including the policy
        document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_policy_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_policy_version)
        """

    def get_role(self, **kwargs: Unpack[GetRoleRequestRequestTypeDef]) -> GetRoleResponseTypeDef:
        """
        Retrieves information about the specified role, including the role's path,
        GUID, ARN, and the role's trust policy that grants permission to assume the
        role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_role)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_role)
        """

    def get_role_policy(
        self, **kwargs: Unpack[GetRolePolicyRequestRequestTypeDef]
    ) -> GetRolePolicyResponseTypeDef:
        """
        Retrieves the specified inline policy document that is embedded with the
        specified IAM
        role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_role_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_role_policy)
        """

    def get_saml_provider(
        self, **kwargs: Unpack[GetSAMLProviderRequestRequestTypeDef]
    ) -> GetSAMLProviderResponseTypeDef:
        """
        Returns the SAML provider metadocument that was uploaded when the IAM SAML
        provider resource object was created or
        updated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_saml_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_saml_provider)
        """

    def get_server_certificate(
        self, **kwargs: Unpack[GetServerCertificateRequestRequestTypeDef]
    ) -> GetServerCertificateResponseTypeDef:
        """
        Retrieves information about the specified server certificate stored in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_server_certificate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_server_certificate)
        """

    def get_service_last_accessed_details(
        self, **kwargs: Unpack[GetServiceLastAccessedDetailsRequestRequestTypeDef]
    ) -> GetServiceLastAccessedDetailsResponseTypeDef:
        """
        Retrieves a service last accessed report that was created using the
        `GenerateServiceLastAccessedDetails`
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_service_last_accessed_details)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_service_last_accessed_details)
        """

    def get_service_last_accessed_details_with_entities(
        self, **kwargs: Unpack[GetServiceLastAccessedDetailsWithEntitiesRequestRequestTypeDef]
    ) -> GetServiceLastAccessedDetailsWithEntitiesResponseTypeDef:
        """
        After you generate a group or policy report using the
        `GenerateServiceLastAccessedDetails` operation, you can use the `JobId`
        parameter in
        `GetServiceLastAccessedDetailsWithEntities`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_service_last_accessed_details_with_entities)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_service_last_accessed_details_with_entities)
        """

    def get_service_linked_role_deletion_status(
        self, **kwargs: Unpack[GetServiceLinkedRoleDeletionStatusRequestRequestTypeDef]
    ) -> GetServiceLinkedRoleDeletionStatusResponseTypeDef:
        """
        Retrieves the status of your service-linked role deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_service_linked_role_deletion_status)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_service_linked_role_deletion_status)
        """

    def get_ssh_public_key(
        self, **kwargs: Unpack[GetSSHPublicKeyRequestRequestTypeDef]
    ) -> GetSSHPublicKeyResponseTypeDef:
        """
        Retrieves the specified SSH public key, including metadata about the key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_ssh_public_key)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_ssh_public_key)
        """

    def get_user(self, **kwargs: Unpack[GetUserRequestRequestTypeDef]) -> GetUserResponseTypeDef:
        """
        Retrieves information about the specified IAM user, including the user's
        creation date, path, unique ID, and
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_user)
        """

    def get_user_policy(
        self, **kwargs: Unpack[GetUserPolicyRequestRequestTypeDef]
    ) -> GetUserPolicyResponseTypeDef:
        """
        Retrieves the specified inline policy document that is embedded in the
        specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_user_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_user_policy)
        """

    def list_access_keys(
        self, **kwargs: Unpack[ListAccessKeysRequestRequestTypeDef]
    ) -> ListAccessKeysResponseTypeDef:
        """
        Returns information about the access key IDs associated with the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_access_keys)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_access_keys)
        """

    def list_account_aliases(
        self, **kwargs: Unpack[ListAccountAliasesRequestRequestTypeDef]
    ) -> ListAccountAliasesResponseTypeDef:
        """
        Lists the account alias associated with the Amazon Web Services account (Note:
        you can have only
        one).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_account_aliases)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_account_aliases)
        """

    def list_attached_group_policies(
        self, **kwargs: Unpack[ListAttachedGroupPoliciesRequestRequestTypeDef]
    ) -> ListAttachedGroupPoliciesResponseTypeDef:
        """
        Lists all managed policies that are attached to the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_attached_group_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_attached_group_policies)
        """

    def list_attached_role_policies(
        self, **kwargs: Unpack[ListAttachedRolePoliciesRequestRequestTypeDef]
    ) -> ListAttachedRolePoliciesResponseTypeDef:
        """
        Lists all managed policies that are attached to the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_attached_role_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_attached_role_policies)
        """

    def list_attached_user_policies(
        self, **kwargs: Unpack[ListAttachedUserPoliciesRequestRequestTypeDef]
    ) -> ListAttachedUserPoliciesResponseTypeDef:
        """
        Lists all managed policies that are attached to the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_attached_user_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_attached_user_policies)
        """

    def list_entities_for_policy(
        self, **kwargs: Unpack[ListEntitiesForPolicyRequestRequestTypeDef]
    ) -> ListEntitiesForPolicyResponseTypeDef:
        """
        Lists all IAM users, groups, and roles that the specified managed policy is
        attached
        to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_entities_for_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_entities_for_policy)
        """

    def list_group_policies(
        self, **kwargs: Unpack[ListGroupPoliciesRequestRequestTypeDef]
    ) -> ListGroupPoliciesResponseTypeDef:
        """
        Lists the names of the inline policies that are embedded in the specified IAM
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_group_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_group_policies)
        """

    def list_groups(
        self, **kwargs: Unpack[ListGroupsRequestRequestTypeDef]
    ) -> ListGroupsResponseTypeDef:
        """
        Lists the IAM groups that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_groups)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_groups)
        """

    def list_groups_for_user(
        self, **kwargs: Unpack[ListGroupsForUserRequestRequestTypeDef]
    ) -> ListGroupsForUserResponseTypeDef:
        """
        Lists the IAM groups that the specified IAM user belongs to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_groups_for_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_groups_for_user)
        """

    def list_instance_profile_tags(
        self, **kwargs: Unpack[ListInstanceProfileTagsRequestRequestTypeDef]
    ) -> ListInstanceProfileTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_instance_profile_tags)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_instance_profile_tags)
        """

    def list_instance_profiles(
        self, **kwargs: Unpack[ListInstanceProfilesRequestRequestTypeDef]
    ) -> ListInstanceProfilesResponseTypeDef:
        """
        Lists the instance profiles that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_instance_profiles)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_instance_profiles)
        """

    def list_instance_profiles_for_role(
        self, **kwargs: Unpack[ListInstanceProfilesForRoleRequestRequestTypeDef]
    ) -> ListInstanceProfilesForRoleResponseTypeDef:
        """
        Lists the instance profiles that have the specified associated IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_instance_profiles_for_role)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_instance_profiles_for_role)
        """

    def list_mfa_device_tags(
        self, **kwargs: Unpack[ListMFADeviceTagsRequestRequestTypeDef]
    ) -> ListMFADeviceTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM virtual multi-factor
        authentication (MFA)
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_mfa_device_tags)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_mfa_device_tags)
        """

    def list_mfa_devices(
        self, **kwargs: Unpack[ListMFADevicesRequestRequestTypeDef]
    ) -> ListMFADevicesResponseTypeDef:
        """
        Lists the MFA devices for an IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_mfa_devices)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_mfa_devices)
        """

    def list_open_id_connect_provider_tags(
        self, **kwargs: Unpack[ListOpenIDConnectProviderTagsRequestRequestTypeDef]
    ) -> ListOpenIDConnectProviderTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified OpenID Connect
        (OIDC)-compatible identity
        provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_open_id_connect_provider_tags)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_open_id_connect_provider_tags)
        """

    def list_open_id_connect_providers(self) -> ListOpenIDConnectProvidersResponseTypeDef:
        """
        Lists information about the IAM OpenID Connect (OIDC) provider resource objects
        defined in the Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_open_id_connect_providers)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_open_id_connect_providers)
        """

    def list_policies(
        self, **kwargs: Unpack[ListPoliciesRequestRequestTypeDef]
    ) -> ListPoliciesResponseTypeDef:
        """
        Lists all the managed policies that are available in your Amazon Web Services
        account, including your own customer-defined managed policies and all Amazon
        Web Services managed
        policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_policies)
        """

    def list_policies_granting_service_access(
        self, **kwargs: Unpack[ListPoliciesGrantingServiceAccessRequestRequestTypeDef]
    ) -> ListPoliciesGrantingServiceAccessResponseTypeDef:
        """
        Retrieves a list of policies that the IAM identity (user, group, or role) can
        use to access each specified
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policies_granting_service_access)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_policies_granting_service_access)
        """

    def list_policy_tags(
        self, **kwargs: Unpack[ListPolicyTagsRequestRequestTypeDef]
    ) -> ListPolicyTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM customer managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policy_tags)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_policy_tags)
        """

    def list_policy_versions(
        self, **kwargs: Unpack[ListPolicyVersionsRequestRequestTypeDef]
    ) -> ListPolicyVersionsResponseTypeDef:
        """
        Lists information about the versions of the specified managed policy, including
        the version that is currently set as the policy's default
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policy_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_policy_versions)
        """

    def list_role_policies(
        self, **kwargs: Unpack[ListRolePoliciesRequestRequestTypeDef]
    ) -> ListRolePoliciesResponseTypeDef:
        """
        Lists the names of the inline policies that are embedded in the specified IAM
        role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_role_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_role_policies)
        """

    def list_role_tags(
        self, **kwargs: Unpack[ListRoleTagsRequestRequestTypeDef]
    ) -> ListRoleTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_role_tags)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_role_tags)
        """

    def list_roles(
        self, **kwargs: Unpack[ListRolesRequestRequestTypeDef]
    ) -> ListRolesResponseTypeDef:
        """
        Lists the IAM roles that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_roles)
        """

    def list_saml_provider_tags(
        self, **kwargs: Unpack[ListSAMLProviderTagsRequestRequestTypeDef]
    ) -> ListSAMLProviderTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified Security Assertion Markup
        Language (SAML) identity
        provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_saml_provider_tags)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_saml_provider_tags)
        """

    def list_saml_providers(self) -> ListSAMLProvidersResponseTypeDef:
        """
        Lists the SAML provider resource objects defined in IAM in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_saml_providers)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_saml_providers)
        """

    def list_server_certificate_tags(
        self, **kwargs: Unpack[ListServerCertificateTagsRequestRequestTypeDef]
    ) -> ListServerCertificateTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM server certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_server_certificate_tags)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_server_certificate_tags)
        """

    def list_server_certificates(
        self, **kwargs: Unpack[ListServerCertificatesRequestRequestTypeDef]
    ) -> ListServerCertificatesResponseTypeDef:
        """
        Lists the server certificates stored in IAM that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_server_certificates)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_server_certificates)
        """

    def list_service_specific_credentials(
        self, **kwargs: Unpack[ListServiceSpecificCredentialsRequestRequestTypeDef]
    ) -> ListServiceSpecificCredentialsResponseTypeDef:
        """
        Returns information about the service-specific credentials associated with the
        specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_service_specific_credentials)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_service_specific_credentials)
        """

    def list_signing_certificates(
        self, **kwargs: Unpack[ListSigningCertificatesRequestRequestTypeDef]
    ) -> ListSigningCertificatesResponseTypeDef:
        """
        Returns information about the signing certificates associated with the
        specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_signing_certificates)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_signing_certificates)
        """

    def list_ssh_public_keys(
        self, **kwargs: Unpack[ListSSHPublicKeysRequestRequestTypeDef]
    ) -> ListSSHPublicKeysResponseTypeDef:
        """
        Returns information about the SSH public keys associated with the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_ssh_public_keys)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_ssh_public_keys)
        """

    def list_user_policies(
        self, **kwargs: Unpack[ListUserPoliciesRequestRequestTypeDef]
    ) -> ListUserPoliciesResponseTypeDef:
        """
        Lists the names of the inline policies embedded in the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_user_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_user_policies)
        """

    def list_user_tags(
        self, **kwargs: Unpack[ListUserTagsRequestRequestTypeDef]
    ) -> ListUserTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_user_tags)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_user_tags)
        """

    def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Lists the IAM users that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_users)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_users)
        """

    def list_virtual_mfa_devices(
        self, **kwargs: Unpack[ListVirtualMFADevicesRequestRequestTypeDef]
    ) -> ListVirtualMFADevicesResponseTypeDef:
        """
        Lists the virtual MFA devices defined in the Amazon Web Services account by
        assignment
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_virtual_mfa_devices)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#list_virtual_mfa_devices)
        """

    def put_group_policy(
        self, **kwargs: Unpack[PutGroupPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_group_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#put_group_policy)
        """

    def put_role_permissions_boundary(
        self, **kwargs: Unpack[PutRolePermissionsBoundaryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates the policy that is specified as the IAM role's permissions
        boundary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_role_permissions_boundary)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#put_role_permissions_boundary)
        """

    def put_role_policy(
        self, **kwargs: Unpack[PutRolePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_role_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#put_role_policy)
        """

    def put_user_permissions_boundary(
        self, **kwargs: Unpack[PutUserPermissionsBoundaryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates the policy that is specified as the IAM user's permissions
        boundary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_user_permissions_boundary)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#put_user_permissions_boundary)
        """

    def put_user_policy(
        self, **kwargs: Unpack[PutUserPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_user_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#put_user_policy)
        """

    def remove_client_id_from_open_id_connect_provider(
        self, **kwargs: Unpack[RemoveClientIDFromOpenIDConnectProviderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified client ID (also known as audience) from the list of
        client IDs registered for the specified IAM OpenID Connect (OIDC) provider
        resource
        object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.remove_client_id_from_open_id_connect_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#remove_client_id_from_open_id_connect_provider)
        """

    def remove_role_from_instance_profile(
        self, **kwargs: Unpack[RemoveRoleFromInstanceProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified IAM role from the specified Amazon EC2 instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.remove_role_from_instance_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#remove_role_from_instance_profile)
        """

    def remove_user_from_group(
        self, **kwargs: Unpack[RemoveUserFromGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified user from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.remove_user_from_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#remove_user_from_group)
        """

    def reset_service_specific_credential(
        self, **kwargs: Unpack[ResetServiceSpecificCredentialRequestRequestTypeDef]
    ) -> ResetServiceSpecificCredentialResponseTypeDef:
        """
        Resets the password for a service-specific credential.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.reset_service_specific_credential)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#reset_service_specific_credential)
        """

    def resync_mfa_device(
        self, **kwargs: Unpack[ResyncMFADeviceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Synchronizes the specified MFA device with its IAM resource object on the
        Amazon Web Services
        servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.resync_mfa_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#resync_mfa_device)
        """

    def set_default_policy_version(
        self, **kwargs: Unpack[SetDefaultPolicyVersionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the specified version of the specified policy as the policy's default
        (operative)
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.set_default_policy_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#set_default_policy_version)
        """

    def set_security_token_service_preferences(
        self, **kwargs: Unpack[SetSecurityTokenServicePreferencesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the specified version of the global endpoint token as the token version
        used for the Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.set_security_token_service_preferences)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#set_security_token_service_preferences)
        """

    def simulate_custom_policy(
        self, **kwargs: Unpack[SimulateCustomPolicyRequestRequestTypeDef]
    ) -> SimulatePolicyResponseTypeDef:
        """
        Simulate how a set of IAM policies and optionally a resource-based policy works
        with a list of API operations and Amazon Web Services resources to determine
        the policies' effective
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.simulate_custom_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#simulate_custom_policy)
        """

    def simulate_principal_policy(
        self, **kwargs: Unpack[SimulatePrincipalPolicyRequestRequestTypeDef]
    ) -> SimulatePolicyResponseTypeDef:
        """
        Simulate how a set of IAM policies attached to an IAM entity works with a list
        of API operations and Amazon Web Services resources to determine the policies'
        effective
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.simulate_principal_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#simulate_principal_policy)
        """

    def tag_instance_profile(
        self, **kwargs: Unpack[TagInstanceProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an IAM instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_instance_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#tag_instance_profile)
        """

    def tag_mfa_device(
        self, **kwargs: Unpack[TagMFADeviceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an IAM virtual multi-factor authentication (MFA)
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_mfa_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#tag_mfa_device)
        """

    def tag_open_id_connect_provider(
        self, **kwargs: Unpack[TagOpenIDConnectProviderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an OpenID Connect (OIDC)-compatible identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_open_id_connect_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#tag_open_id_connect_provider)
        """

    def tag_policy(
        self, **kwargs: Unpack[TagPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an IAM customer managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#tag_policy)
        """

    def tag_role(
        self, **kwargs: Unpack[TagRoleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_role)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#tag_role)
        """

    def tag_saml_provider(
        self, **kwargs: Unpack[TagSAMLProviderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to a Security Assertion Markup Language (SAML) identity
        provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_saml_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#tag_saml_provider)
        """

    def tag_server_certificate(
        self, **kwargs: Unpack[TagServerCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an IAM server certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_server_certificate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#tag_server_certificate)
        """

    def tag_user(
        self, **kwargs: Unpack[TagUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#tag_user)
        """

    def untag_instance_profile(
        self, **kwargs: Unpack[UntagInstanceProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the IAM instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_instance_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#untag_instance_profile)
        """

    def untag_mfa_device(
        self, **kwargs: Unpack[UntagMFADeviceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the IAM virtual multi-factor authentication
        (MFA)
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_mfa_device)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#untag_mfa_device)
        """

    def untag_open_id_connect_provider(
        self, **kwargs: Unpack[UntagOpenIDConnectProviderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the specified OpenID Connect (OIDC)-compatible
        identity provider in
        IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_open_id_connect_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#untag_open_id_connect_provider)
        """

    def untag_policy(
        self, **kwargs: Unpack[UntagPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the customer managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#untag_policy)
        """

    def untag_role(
        self, **kwargs: Unpack[UntagRoleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_role)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#untag_role)
        """

    def untag_saml_provider(
        self, **kwargs: Unpack[UntagSAMLProviderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the specified Security Assertion Markup
        Language (SAML) identity provider in
        IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_saml_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#untag_saml_provider)
        """

    def untag_server_certificate(
        self, **kwargs: Unpack[UntagServerCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the IAM server certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_server_certificate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#untag_server_certificate)
        """

    def untag_user(
        self, **kwargs: Unpack[UntagUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#untag_user)
        """

    def update_access_key(
        self, **kwargs: Unpack[UpdateAccessKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the status of the specified access key from Active to Inactive, or vice
        versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_access_key)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_access_key)
        """

    def update_account_password_policy(
        self, **kwargs: Unpack[UpdateAccountPasswordPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the password policy settings for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_account_password_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_account_password_policy)
        """

    def update_assume_role_policy(
        self, **kwargs: Unpack[UpdateAssumeRolePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the policy that grants an IAM entity permission to assume a role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_assume_role_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_assume_role_policy)
        """

    def update_group(
        self, **kwargs: Unpack[UpdateGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name and/or the path of the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_group)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_group)
        """

    def update_login_profile(
        self, **kwargs: Unpack[UpdateLoginProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the password for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_login_profile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_login_profile)
        """

    def update_open_id_connect_provider_thumbprint(
        self, **kwargs: Unpack[UpdateOpenIDConnectProviderThumbprintRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Replaces the existing list of server certificate thumbprints associated with an
        OpenID Connect (OIDC) provider resource object with a new list of
        thumbprints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_open_id_connect_provider_thumbprint)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_open_id_connect_provider_thumbprint)
        """

    def update_role(self, **kwargs: Unpack[UpdateRoleRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the description or maximum session duration setting of a role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_role)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_role)
        """

    def update_role_description(
        self, **kwargs: Unpack[UpdateRoleDescriptionRequestRequestTypeDef]
    ) -> UpdateRoleDescriptionResponseTypeDef:
        """
        Use  UpdateRole instead.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_role_description)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_role_description)
        """

    def update_saml_provider(
        self, **kwargs: Unpack[UpdateSAMLProviderRequestRequestTypeDef]
    ) -> UpdateSAMLProviderResponseTypeDef:
        """
        Updates the metadata document for an existing SAML provider resource object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_saml_provider)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_saml_provider)
        """

    def update_server_certificate(
        self, **kwargs: Unpack[UpdateServerCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name and/or the path of the specified server certificate stored in
        IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_server_certificate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_server_certificate)
        """

    def update_service_specific_credential(
        self, **kwargs: Unpack[UpdateServiceSpecificCredentialRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the status of a service-specific credential to `Active` or `Inactive`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_service_specific_credential)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_service_specific_credential)
        """

    def update_signing_certificate(
        self, **kwargs: Unpack[UpdateSigningCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the status of the specified user signing certificate from active to
        disabled, or vice
        versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_signing_certificate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_signing_certificate)
        """

    def update_ssh_public_key(
        self, **kwargs: Unpack[UpdateSSHPublicKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the status of an IAM user's SSH public key to active or inactive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_ssh_public_key)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_ssh_public_key)
        """

    def update_user(
        self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name and/or the path of the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_user)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#update_user)
        """

    def upload_server_certificate(
        self, **kwargs: Unpack[UploadServerCertificateRequestRequestTypeDef]
    ) -> UploadServerCertificateResponseTypeDef:
        """
        Uploads a server certificate entity for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.upload_server_certificate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#upload_server_certificate)
        """

    def upload_signing_certificate(
        self, **kwargs: Unpack[UploadSigningCertificateRequestRequestTypeDef]
    ) -> UploadSigningCertificateResponseTypeDef:
        """
        Uploads an X.509 signing certificate and associates it with the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.upload_signing_certificate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#upload_signing_certificate)
        """

    def upload_ssh_public_key(
        self, **kwargs: Unpack[UploadSSHPublicKeyRequestRequestTypeDef]
    ) -> UploadSSHPublicKeyResponseTypeDef:
        """
        Uploads an SSH public key and associates it with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.upload_ssh_public_key)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#upload_ssh_public_key)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_account_authorization_details"]
    ) -> GetAccountAuthorizationDetailsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_group"]) -> GetGroupPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_access_keys"]) -> ListAccessKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_aliases"]
    ) -> ListAccountAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_group_policies"]
    ) -> ListAttachedGroupPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_role_policies"]
    ) -> ListAttachedRolePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_user_policies"]
    ) -> ListAttachedUserPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_entities_for_policy"]
    ) -> ListEntitiesForPolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_policies"]
    ) -> ListGroupPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_groups_for_user"]
    ) -> ListGroupsForUserPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_profile_tags"]
    ) -> ListInstanceProfileTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_profiles"]
    ) -> ListInstanceProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_profiles_for_role"]
    ) -> ListInstanceProfilesForRolePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_mfa_device_tags"]
    ) -> ListMFADeviceTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_mfa_devices"]) -> ListMFADevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_open_id_connect_provider_tags"]
    ) -> ListOpenIDConnectProviderTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policy_tags"]) -> ListPolicyTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_versions"]
    ) -> ListPolicyVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_role_policies"]
    ) -> ListRolePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_role_tags"]) -> ListRoleTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_roles"]) -> ListRolesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_saml_provider_tags"]
    ) -> ListSAMLProviderTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ssh_public_keys"]
    ) -> ListSSHPublicKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_server_certificate_tags"]
    ) -> ListServerCertificateTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_server_certificates"]
    ) -> ListServerCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signing_certificates"]
    ) -> ListSigningCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_user_policies"]
    ) -> ListUserPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_user_tags"]) -> ListUserTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_mfa_devices"]
    ) -> ListVirtualMFADevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["simulate_custom_policy"]
    ) -> SimulateCustomPolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["simulate_principal_policy"]
    ) -> SimulatePrincipalPolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["instance_profile_exists"]
    ) -> InstanceProfileExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["policy_exists"]) -> PolicyExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["role_exists"]) -> RoleExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["user_exists"]) -> UserExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam/client/#get_waiter)
        """
