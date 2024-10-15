"""
Type annotations for ssm-contacts service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ssm_contacts.client import SSMContactsClient

    session = Session()
    client: SSMContactsClient = session.client("ssm-contacts")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListContactChannelsPaginator,
    ListContactsPaginator,
    ListEngagementsPaginator,
    ListPageReceiptsPaginator,
    ListPageResolutionsPaginator,
    ListPagesByContactPaginator,
    ListPagesByEngagementPaginator,
    ListPreviewRotationShiftsPaginator,
    ListRotationOverridesPaginator,
    ListRotationShiftsPaginator,
    ListRotationsPaginator,
)
from .type_defs import (
    AcceptPageRequestRequestTypeDef,
    ActivateContactChannelRequestRequestTypeDef,
    CreateContactChannelRequestRequestTypeDef,
    CreateContactChannelResultTypeDef,
    CreateContactRequestRequestTypeDef,
    CreateContactResultTypeDef,
    CreateRotationOverrideRequestRequestTypeDef,
    CreateRotationOverrideResultTypeDef,
    CreateRotationRequestRequestTypeDef,
    CreateRotationResultTypeDef,
    DeactivateContactChannelRequestRequestTypeDef,
    DeleteContactChannelRequestRequestTypeDef,
    DeleteContactRequestRequestTypeDef,
    DeleteRotationOverrideRequestRequestTypeDef,
    DeleteRotationRequestRequestTypeDef,
    DescribeEngagementRequestRequestTypeDef,
    DescribeEngagementResultTypeDef,
    DescribePageRequestRequestTypeDef,
    DescribePageResultTypeDef,
    GetContactChannelRequestRequestTypeDef,
    GetContactChannelResultTypeDef,
    GetContactPolicyRequestRequestTypeDef,
    GetContactPolicyResultTypeDef,
    GetContactRequestRequestTypeDef,
    GetContactResultTypeDef,
    GetRotationOverrideRequestRequestTypeDef,
    GetRotationOverrideResultTypeDef,
    GetRotationRequestRequestTypeDef,
    GetRotationResultTypeDef,
    ListContactChannelsRequestRequestTypeDef,
    ListContactChannelsResultTypeDef,
    ListContactsRequestRequestTypeDef,
    ListContactsResultTypeDef,
    ListEngagementsRequestRequestTypeDef,
    ListEngagementsResultTypeDef,
    ListPageReceiptsRequestRequestTypeDef,
    ListPageReceiptsResultTypeDef,
    ListPageResolutionsRequestRequestTypeDef,
    ListPageResolutionsResultTypeDef,
    ListPagesByContactRequestRequestTypeDef,
    ListPagesByContactResultTypeDef,
    ListPagesByEngagementRequestRequestTypeDef,
    ListPagesByEngagementResultTypeDef,
    ListPreviewRotationShiftsRequestRequestTypeDef,
    ListPreviewRotationShiftsResultTypeDef,
    ListRotationOverridesRequestRequestTypeDef,
    ListRotationOverridesResultTypeDef,
    ListRotationShiftsRequestRequestTypeDef,
    ListRotationShiftsResultTypeDef,
    ListRotationsRequestRequestTypeDef,
    ListRotationsResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResultTypeDef,
    PutContactPolicyRequestRequestTypeDef,
    SendActivationCodeRequestRequestTypeDef,
    StartEngagementRequestRequestTypeDef,
    StartEngagementResultTypeDef,
    StopEngagementRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateContactChannelRequestRequestTypeDef,
    UpdateContactRequestRequestTypeDef,
    UpdateRotationRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SSMContactsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DataEncryptionException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SSMContactsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSMContactsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#exceptions)
        """

    def accept_page(self, **kwargs: Unpack[AcceptPageRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Used to acknowledge an engagement to a contact channel during an incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.accept_page)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#accept_page)
        """

    def activate_contact_channel(
        self, **kwargs: Unpack[ActivateContactChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Activates a contact's contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.activate_contact_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#activate_contact_channel)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#close)
        """

    def create_contact(
        self, **kwargs: Unpack[CreateContactRequestRequestTypeDef]
    ) -> CreateContactResultTypeDef:
        """
        Contacts are either the contacts that Incident Manager engages during an
        incident or the escalation plans that Incident Manager uses to engage contacts
        in phases during an
        incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.create_contact)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#create_contact)
        """

    def create_contact_channel(
        self, **kwargs: Unpack[CreateContactChannelRequestRequestTypeDef]
    ) -> CreateContactChannelResultTypeDef:
        """
        A contact channel is the method that Incident Manager uses to engage your
        contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.create_contact_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#create_contact_channel)
        """

    def create_rotation(
        self, **kwargs: Unpack[CreateRotationRequestRequestTypeDef]
    ) -> CreateRotationResultTypeDef:
        """
        Creates a rotation in an on-call schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.create_rotation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#create_rotation)
        """

    def create_rotation_override(
        self, **kwargs: Unpack[CreateRotationOverrideRequestRequestTypeDef]
    ) -> CreateRotationOverrideResultTypeDef:
        """
        Creates an override for a rotation in an on-call schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.create_rotation_override)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#create_rotation_override)
        """

    def deactivate_contact_channel(
        self, **kwargs: Unpack[DeactivateContactChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        To no longer receive Incident Manager engagements to a contact channel, you can
        deactivate the
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.deactivate_contact_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#deactivate_contact_channel)
        """

    def delete_contact(
        self, **kwargs: Unpack[DeleteContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        To remove a contact from Incident Manager, you can delete the contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.delete_contact)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#delete_contact)
        """

    def delete_contact_channel(
        self, **kwargs: Unpack[DeleteContactChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        To no longer receive engagements on a contact channel, you can delete the
        channel from a
        contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.delete_contact_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#delete_contact_channel)
        """

    def delete_rotation(
        self, **kwargs: Unpack[DeleteRotationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a rotation from the system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.delete_rotation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#delete_rotation)
        """

    def delete_rotation_override(
        self, **kwargs: Unpack[DeleteRotationOverrideRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing override for an on-call rotation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.delete_rotation_override)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#delete_rotation_override)
        """

    def describe_engagement(
        self, **kwargs: Unpack[DescribeEngagementRequestRequestTypeDef]
    ) -> DescribeEngagementResultTypeDef:
        """
        Incident Manager uses engagements to engage contacts and escalation plans
        during an
        incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.describe_engagement)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#describe_engagement)
        """

    def describe_page(
        self, **kwargs: Unpack[DescribePageRequestRequestTypeDef]
    ) -> DescribePageResultTypeDef:
        """
        Lists details of the engagement to a contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.describe_page)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#describe_page)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#generate_presigned_url)
        """

    def get_contact(
        self, **kwargs: Unpack[GetContactRequestRequestTypeDef]
    ) -> GetContactResultTypeDef:
        """
        Retrieves information about the specified contact or escalation plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_contact)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_contact)
        """

    def get_contact_channel(
        self, **kwargs: Unpack[GetContactChannelRequestRequestTypeDef]
    ) -> GetContactChannelResultTypeDef:
        """
        List details about a specific contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_contact_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_contact_channel)
        """

    def get_contact_policy(
        self, **kwargs: Unpack[GetContactPolicyRequestRequestTypeDef]
    ) -> GetContactPolicyResultTypeDef:
        """
        Retrieves the resource policies attached to the specified contact or escalation
        plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_contact_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_contact_policy)
        """

    def get_rotation(
        self, **kwargs: Unpack[GetRotationRequestRequestTypeDef]
    ) -> GetRotationResultTypeDef:
        """
        Retrieves information about an on-call rotation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_rotation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_rotation)
        """

    def get_rotation_override(
        self, **kwargs: Unpack[GetRotationOverrideRequestRequestTypeDef]
    ) -> GetRotationOverrideResultTypeDef:
        """
        Retrieves information about an override to an on-call rotation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_rotation_override)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_rotation_override)
        """

    def list_contact_channels(
        self, **kwargs: Unpack[ListContactChannelsRequestRequestTypeDef]
    ) -> ListContactChannelsResultTypeDef:
        """
        Lists all contact channels for the specified contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_contact_channels)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_contact_channels)
        """

    def list_contacts(
        self, **kwargs: Unpack[ListContactsRequestRequestTypeDef]
    ) -> ListContactsResultTypeDef:
        """
        Lists all contacts and escalation plans in Incident Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_contacts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_contacts)
        """

    def list_engagements(
        self, **kwargs: Unpack[ListEngagementsRequestRequestTypeDef]
    ) -> ListEngagementsResultTypeDef:
        """
        Lists all engagements that have happened in an incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_engagements)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_engagements)
        """

    def list_page_receipts(
        self, **kwargs: Unpack[ListPageReceiptsRequestRequestTypeDef]
    ) -> ListPageReceiptsResultTypeDef:
        """
        Lists all of the engagements to contact channels that have been acknowledged.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_page_receipts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_page_receipts)
        """

    def list_page_resolutions(
        self, **kwargs: Unpack[ListPageResolutionsRequestRequestTypeDef]
    ) -> ListPageResolutionsResultTypeDef:
        """
        Returns the resolution path of an engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_page_resolutions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_page_resolutions)
        """

    def list_pages_by_contact(
        self, **kwargs: Unpack[ListPagesByContactRequestRequestTypeDef]
    ) -> ListPagesByContactResultTypeDef:
        """
        Lists the engagements to a contact's contact channels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_pages_by_contact)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_pages_by_contact)
        """

    def list_pages_by_engagement(
        self, **kwargs: Unpack[ListPagesByEngagementRequestRequestTypeDef]
    ) -> ListPagesByEngagementResultTypeDef:
        """
        Lists the engagements to contact channels that occurred by engaging a contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_pages_by_engagement)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_pages_by_engagement)
        """

    def list_preview_rotation_shifts(
        self, **kwargs: Unpack[ListPreviewRotationShiftsRequestRequestTypeDef]
    ) -> ListPreviewRotationShiftsResultTypeDef:
        """
        Returns a list of shifts based on rotation configuration parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_preview_rotation_shifts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_preview_rotation_shifts)
        """

    def list_rotation_overrides(
        self, **kwargs: Unpack[ListRotationOverridesRequestRequestTypeDef]
    ) -> ListRotationOverridesResultTypeDef:
        """
        Retrieves a list of overrides currently specified for an on-call rotation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_rotation_overrides)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_rotation_overrides)
        """

    def list_rotation_shifts(
        self, **kwargs: Unpack[ListRotationShiftsRequestRequestTypeDef]
    ) -> ListRotationShiftsResultTypeDef:
        """
        Returns a list of shifts generated by an existing rotation in the system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_rotation_shifts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_rotation_shifts)
        """

    def list_rotations(
        self, **kwargs: Unpack[ListRotationsRequestRequestTypeDef]
    ) -> ListRotationsResultTypeDef:
        """
        Retrieves a list of on-call rotations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_rotations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_rotations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResultTypeDef:
        """
        Lists the tags of an escalation plan or contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#list_tags_for_resource)
        """

    def put_contact_policy(
        self, **kwargs: Unpack[PutContactPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a resource policy to the specified contact or escalation plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.put_contact_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#put_contact_policy)
        """

    def send_activation_code(
        self, **kwargs: Unpack[SendActivationCodeRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sends an activation code to a contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.send_activation_code)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#send_activation_code)
        """

    def start_engagement(
        self, **kwargs: Unpack[StartEngagementRequestRequestTypeDef]
    ) -> StartEngagementResultTypeDef:
        """
        Starts an engagement to a contact or escalation plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.start_engagement)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#start_engagement)
        """

    def stop_engagement(
        self, **kwargs: Unpack[StopEngagementRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an engagement before it finishes the final stage of the escalation plan
        or engagement
        plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.stop_engagement)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#stop_engagement)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags a contact or escalation plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#untag_resource)
        """

    def update_contact(
        self, **kwargs: Unpack[UpdateContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the contact or escalation plan specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.update_contact)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#update_contact)
        """

    def update_contact_channel(
        self, **kwargs: Unpack[UpdateContactChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a contact's contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.update_contact_channel)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#update_contact_channel)
        """

    def update_rotation(
        self, **kwargs: Unpack[UpdateRotationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the information specified for an on-call rotation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.update_rotation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#update_rotation)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_contact_channels"]
    ) -> ListContactChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_contacts"]) -> ListContactsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_engagements"]
    ) -> ListEngagementsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_page_receipts"]
    ) -> ListPageReceiptsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_page_resolutions"]
    ) -> ListPageResolutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pages_by_contact"]
    ) -> ListPagesByContactPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pages_by_engagement"]
    ) -> ListPagesByEngagementPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_preview_rotation_shifts"]
    ) -> ListPreviewRotationShiftsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rotation_overrides"]
    ) -> ListRotationOverridesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rotation_shifts"]
    ) -> ListRotationShiftsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rotations"]) -> ListRotationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/client/#get_paginator)
        """
