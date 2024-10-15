"""
Type annotations for cloudformation service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudformation.client import CloudFormationClient

    session = Session()
    client: CloudFormationClient = session.client("cloudformation")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeAccountLimitsPaginator,
    DescribeChangeSetPaginator,
    DescribeStackEventsPaginator,
    DescribeStacksPaginator,
    ListChangeSetsPaginator,
    ListExportsPaginator,
    ListGeneratedTemplatesPaginator,
    ListImportsPaginator,
    ListResourceScanRelatedResourcesPaginator,
    ListResourceScanResourcesPaginator,
    ListResourceScansPaginator,
    ListStackInstancesPaginator,
    ListStackResourcesPaginator,
    ListStackSetOperationResultsPaginator,
    ListStackSetOperationsPaginator,
    ListStackSetsPaginator,
    ListStacksPaginator,
    ListTypesPaginator,
)
from .type_defs import (
    ActivateTypeInputRequestTypeDef,
    ActivateTypeOutputTypeDef,
    BatchDescribeTypeConfigurationsInputRequestTypeDef,
    BatchDescribeTypeConfigurationsOutputTypeDef,
    CancelUpdateStackInputRequestTypeDef,
    ContinueUpdateRollbackInputRequestTypeDef,
    CreateChangeSetInputRequestTypeDef,
    CreateChangeSetOutputTypeDef,
    CreateGeneratedTemplateInputRequestTypeDef,
    CreateGeneratedTemplateOutputTypeDef,
    CreateStackInputRequestTypeDef,
    CreateStackInstancesInputRequestTypeDef,
    CreateStackInstancesOutputTypeDef,
    CreateStackOutputTypeDef,
    CreateStackSetInputRequestTypeDef,
    CreateStackSetOutputTypeDef,
    DeactivateTypeInputRequestTypeDef,
    DeleteChangeSetInputRequestTypeDef,
    DeleteGeneratedTemplateInputRequestTypeDef,
    DeleteStackInputRequestTypeDef,
    DeleteStackInstancesInputRequestTypeDef,
    DeleteStackInstancesOutputTypeDef,
    DeleteStackSetInputRequestTypeDef,
    DeregisterTypeInputRequestTypeDef,
    DescribeAccountLimitsInputRequestTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeChangeSetHooksInputRequestTypeDef,
    DescribeChangeSetHooksOutputTypeDef,
    DescribeChangeSetInputRequestTypeDef,
    DescribeChangeSetOutputTypeDef,
    DescribeGeneratedTemplateInputRequestTypeDef,
    DescribeGeneratedTemplateOutputTypeDef,
    DescribeOrganizationsAccessInputRequestTypeDef,
    DescribeOrganizationsAccessOutputTypeDef,
    DescribePublisherInputRequestTypeDef,
    DescribePublisherOutputTypeDef,
    DescribeResourceScanInputRequestTypeDef,
    DescribeResourceScanOutputTypeDef,
    DescribeStackDriftDetectionStatusInputRequestTypeDef,
    DescribeStackDriftDetectionStatusOutputTypeDef,
    DescribeStackEventsInputRequestTypeDef,
    DescribeStackEventsOutputTypeDef,
    DescribeStackInstanceInputRequestTypeDef,
    DescribeStackInstanceOutputTypeDef,
    DescribeStackResourceDriftsInputRequestTypeDef,
    DescribeStackResourceDriftsOutputTypeDef,
    DescribeStackResourceInputRequestTypeDef,
    DescribeStackResourceOutputTypeDef,
    DescribeStackResourcesInputRequestTypeDef,
    DescribeStackResourcesOutputTypeDef,
    DescribeStackSetInputRequestTypeDef,
    DescribeStackSetOperationInputRequestTypeDef,
    DescribeStackSetOperationOutputTypeDef,
    DescribeStackSetOutputTypeDef,
    DescribeStacksInputRequestTypeDef,
    DescribeStacksOutputTypeDef,
    DescribeTypeInputRequestTypeDef,
    DescribeTypeOutputTypeDef,
    DescribeTypeRegistrationInputRequestTypeDef,
    DescribeTypeRegistrationOutputTypeDef,
    DetectStackDriftInputRequestTypeDef,
    DetectStackDriftOutputTypeDef,
    DetectStackResourceDriftInputRequestTypeDef,
    DetectStackResourceDriftOutputTypeDef,
    DetectStackSetDriftInputRequestTypeDef,
    DetectStackSetDriftOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    EstimateTemplateCostInputRequestTypeDef,
    EstimateTemplateCostOutputTypeDef,
    ExecuteChangeSetInputRequestTypeDef,
    GetGeneratedTemplateInputRequestTypeDef,
    GetGeneratedTemplateOutputTypeDef,
    GetStackPolicyInputRequestTypeDef,
    GetStackPolicyOutputTypeDef,
    GetTemplateInputRequestTypeDef,
    GetTemplateOutputTypeDef,
    GetTemplateSummaryInputRequestTypeDef,
    GetTemplateSummaryOutputTypeDef,
    ImportStacksToStackSetInputRequestTypeDef,
    ImportStacksToStackSetOutputTypeDef,
    ListChangeSetsInputRequestTypeDef,
    ListChangeSetsOutputTypeDef,
    ListExportsInputRequestTypeDef,
    ListExportsOutputTypeDef,
    ListGeneratedTemplatesInputRequestTypeDef,
    ListGeneratedTemplatesOutputTypeDef,
    ListImportsInputRequestTypeDef,
    ListImportsOutputTypeDef,
    ListResourceScanRelatedResourcesInputRequestTypeDef,
    ListResourceScanRelatedResourcesOutputTypeDef,
    ListResourceScanResourcesInputRequestTypeDef,
    ListResourceScanResourcesOutputTypeDef,
    ListResourceScansInputRequestTypeDef,
    ListResourceScansOutputTypeDef,
    ListStackInstanceResourceDriftsInputRequestTypeDef,
    ListStackInstanceResourceDriftsOutputTypeDef,
    ListStackInstancesInputRequestTypeDef,
    ListStackInstancesOutputTypeDef,
    ListStackResourcesInputRequestTypeDef,
    ListStackResourcesOutputTypeDef,
    ListStackSetAutoDeploymentTargetsInputRequestTypeDef,
    ListStackSetAutoDeploymentTargetsOutputTypeDef,
    ListStackSetOperationResultsInputRequestTypeDef,
    ListStackSetOperationResultsOutputTypeDef,
    ListStackSetOperationsInputRequestTypeDef,
    ListStackSetOperationsOutputTypeDef,
    ListStackSetsInputRequestTypeDef,
    ListStackSetsOutputTypeDef,
    ListStacksInputRequestTypeDef,
    ListStacksOutputTypeDef,
    ListTypeRegistrationsInputRequestTypeDef,
    ListTypeRegistrationsOutputTypeDef,
    ListTypesInputRequestTypeDef,
    ListTypesOutputTypeDef,
    ListTypeVersionsInputRequestTypeDef,
    ListTypeVersionsOutputTypeDef,
    PublishTypeInputRequestTypeDef,
    PublishTypeOutputTypeDef,
    RecordHandlerProgressInputRequestTypeDef,
    RegisterPublisherInputRequestTypeDef,
    RegisterPublisherOutputTypeDef,
    RegisterTypeInputRequestTypeDef,
    RegisterTypeOutputTypeDef,
    RollbackStackInputRequestTypeDef,
    RollbackStackOutputTypeDef,
    SetStackPolicyInputRequestTypeDef,
    SetTypeConfigurationInputRequestTypeDef,
    SetTypeConfigurationOutputTypeDef,
    SetTypeDefaultVersionInputRequestTypeDef,
    SignalResourceInputRequestTypeDef,
    StartResourceScanInputRequestTypeDef,
    StartResourceScanOutputTypeDef,
    StopStackSetOperationInputRequestTypeDef,
    TestTypeInputRequestTypeDef,
    TestTypeOutputTypeDef,
    UpdateGeneratedTemplateInputRequestTypeDef,
    UpdateGeneratedTemplateOutputTypeDef,
    UpdateStackInputRequestTypeDef,
    UpdateStackInstancesInputRequestTypeDef,
    UpdateStackInstancesOutputTypeDef,
    UpdateStackOutputTypeDef,
    UpdateStackSetInputRequestTypeDef,
    UpdateStackSetOutputTypeDef,
    UpdateTerminationProtectionInputRequestTypeDef,
    UpdateTerminationProtectionOutputTypeDef,
    ValidateTemplateInputRequestTypeDef,
    ValidateTemplateOutputTypeDef,
)
from .waiter import (
    ChangeSetCreateCompleteWaiter,
    StackCreateCompleteWaiter,
    StackDeleteCompleteWaiter,
    StackExistsWaiter,
    StackImportCompleteWaiter,
    StackRollbackCompleteWaiter,
    StackUpdateCompleteWaiter,
    TypeRegistrationCompleteWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CloudFormationClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    CFNRegistryException: Type[BotocoreClientError]
    ChangeSetNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentResourcesLimitExceededException: Type[BotocoreClientError]
    CreatedButModifiedException: Type[BotocoreClientError]
    GeneratedTemplateNotFoundException: Type[BotocoreClientError]
    InsufficientCapabilitiesException: Type[BotocoreClientError]
    InvalidChangeSetStatusException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidStateTransitionException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NameAlreadyExistsException: Type[BotocoreClientError]
    OperationIdAlreadyExistsException: Type[BotocoreClientError]
    OperationInProgressException: Type[BotocoreClientError]
    OperationNotFoundException: Type[BotocoreClientError]
    OperationStatusCheckFailedException: Type[BotocoreClientError]
    ResourceScanInProgressException: Type[BotocoreClientError]
    ResourceScanLimitExceededException: Type[BotocoreClientError]
    ResourceScanNotFoundException: Type[BotocoreClientError]
    StackInstanceNotFoundException: Type[BotocoreClientError]
    StackNotFoundException: Type[BotocoreClientError]
    StackSetNotEmptyException: Type[BotocoreClientError]
    StackSetNotFoundException: Type[BotocoreClientError]
    StaleRequestException: Type[BotocoreClientError]
    TokenAlreadyExistsException: Type[BotocoreClientError]
    TypeConfigurationNotFoundException: Type[BotocoreClientError]
    TypeNotFoundException: Type[BotocoreClientError]


class CloudFormationClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudFormationClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#exceptions)
        """

    def activate_organizations_access(self) -> Dict[str, Any]:
        """
        Activate trusted access with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.activate_organizations_access)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#activate_organizations_access)
        """

    def activate_type(
        self, **kwargs: Unpack[ActivateTypeInputRequestTypeDef]
    ) -> ActivateTypeOutputTypeDef:
        """
        Activates a public third-party extension, making it available for use in stack
        templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.activate_type)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#activate_type)
        """

    def batch_describe_type_configurations(
        self, **kwargs: Unpack[BatchDescribeTypeConfigurationsInputRequestTypeDef]
    ) -> BatchDescribeTypeConfigurationsOutputTypeDef:
        """
        Returns configuration data for the specified CloudFormation extensions, from
        the CloudFormation registry for the account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.batch_describe_type_configurations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#batch_describe_type_configurations)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#can_paginate)
        """

    def cancel_update_stack(
        self, **kwargs: Unpack[CancelUpdateStackInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels an update on the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.cancel_update_stack)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#cancel_update_stack)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#close)
        """

    def continue_update_rollback(
        self, **kwargs: Unpack[ContinueUpdateRollbackInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        For a specified stack that's in the `UPDATE_ROLLBACK_FAILED` state, continues
        rolling it back to the `UPDATE_ROLLBACK_COMPLETE`
        state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.continue_update_rollback)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#continue_update_rollback)
        """

    def create_change_set(
        self, **kwargs: Unpack[CreateChangeSetInputRequestTypeDef]
    ) -> CreateChangeSetOutputTypeDef:
        """
        Creates a list of changes that will be applied to a stack so that you can
        review the changes before executing
        them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_change_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#create_change_set)
        """

    def create_generated_template(
        self, **kwargs: Unpack[CreateGeneratedTemplateInputRequestTypeDef]
    ) -> CreateGeneratedTemplateOutputTypeDef:
        """
        Creates a template from existing resources that are not already managed with
        CloudFormation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_generated_template)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#create_generated_template)
        """

    def create_stack(
        self, **kwargs: Unpack[CreateStackInputRequestTypeDef]
    ) -> CreateStackOutputTypeDef:
        """
        Creates a stack as specified in the template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#create_stack)
        """

    def create_stack_instances(
        self, **kwargs: Unpack[CreateStackInstancesInputRequestTypeDef]
    ) -> CreateStackInstancesOutputTypeDef:
        """
        Creates stack instances for the specified accounts, within the specified Amazon
        Web Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack_instances)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#create_stack_instances)
        """

    def create_stack_set(
        self, **kwargs: Unpack[CreateStackSetInputRequestTypeDef]
    ) -> CreateStackSetOutputTypeDef:
        """
        Creates a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#create_stack_set)
        """

    def deactivate_organizations_access(self) -> Dict[str, Any]:
        """
        Deactivates trusted access with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.deactivate_organizations_access)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#deactivate_organizations_access)
        """

    def deactivate_type(
        self, **kwargs: Unpack[DeactivateTypeInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deactivates a public extension that was previously activated in this account
        and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.deactivate_type)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#deactivate_type)
        """

    def delete_change_set(
        self, **kwargs: Unpack[DeleteChangeSetInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified change set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_change_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#delete_change_set)
        """

    def delete_generated_template(
        self, **kwargs: Unpack[DeleteGeneratedTemplateInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deleted a generated template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_generated_template)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#delete_generated_template)
        """

    def delete_stack(
        self, **kwargs: Unpack[DeleteStackInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_stack)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#delete_stack)
        """

    def delete_stack_instances(
        self, **kwargs: Unpack[DeleteStackInstancesInputRequestTypeDef]
    ) -> DeleteStackInstancesOutputTypeDef:
        """
        Deletes stack instances for the specified accounts, in the specified Amazon Web
        Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_stack_instances)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#delete_stack_instances)
        """

    def delete_stack_set(
        self, **kwargs: Unpack[DeleteStackSetInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_stack_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#delete_stack_set)
        """

    def deregister_type(
        self, **kwargs: Unpack[DeregisterTypeInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Marks an extension or extension version as `DEPRECATED` in the CloudFormation
        registry, removing it from active
        use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.deregister_type)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#deregister_type)
        """

    def describe_account_limits(
        self, **kwargs: Unpack[DescribeAccountLimitsInputRequestTypeDef]
    ) -> DescribeAccountLimitsOutputTypeDef:
        """
        Retrieves your account's CloudFormation limits, such as the maximum number of
        stacks that you can create in your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_account_limits)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_account_limits)
        """

    def describe_change_set(
        self, **kwargs: Unpack[DescribeChangeSetInputRequestTypeDef]
    ) -> DescribeChangeSetOutputTypeDef:
        """
        Returns the inputs for the change set and a list of changes that CloudFormation
        will make if you execute the change
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_change_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_change_set)
        """

    def describe_change_set_hooks(
        self, **kwargs: Unpack[DescribeChangeSetHooksInputRequestTypeDef]
    ) -> DescribeChangeSetHooksOutputTypeDef:
        """
        Returns hook-related information for the change set and a list of changes that
        CloudFormation makes when you run the change
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_change_set_hooks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_change_set_hooks)
        """

    def describe_generated_template(
        self, **kwargs: Unpack[DescribeGeneratedTemplateInputRequestTypeDef]
    ) -> DescribeGeneratedTemplateOutputTypeDef:
        """
        Describes a generated template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_generated_template)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_generated_template)
        """

    def describe_organizations_access(
        self, **kwargs: Unpack[DescribeOrganizationsAccessInputRequestTypeDef]
    ) -> DescribeOrganizationsAccessOutputTypeDef:
        """
        Retrieves information about the account's `OrganizationAccess` status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_organizations_access)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_organizations_access)
        """

    def describe_publisher(
        self, **kwargs: Unpack[DescribePublisherInputRequestTypeDef]
    ) -> DescribePublisherOutputTypeDef:
        """
        Returns information about a CloudFormation extension publisher.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_publisher)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_publisher)
        """

    def describe_resource_scan(
        self, **kwargs: Unpack[DescribeResourceScanInputRequestTypeDef]
    ) -> DescribeResourceScanOutputTypeDef:
        """
        Describes details of a resource scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_resource_scan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_resource_scan)
        """

    def describe_stack_drift_detection_status(
        self, **kwargs: Unpack[DescribeStackDriftDetectionStatusInputRequestTypeDef]
    ) -> DescribeStackDriftDetectionStatusOutputTypeDef:
        """
        Returns information about a stack drift detection operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_drift_detection_status)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_stack_drift_detection_status)
        """

    def describe_stack_events(
        self, **kwargs: Unpack[DescribeStackEventsInputRequestTypeDef]
    ) -> DescribeStackEventsOutputTypeDef:
        """
        Returns all stack related events for a specified stack in reverse chronological
        order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_events)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_stack_events)
        """

    def describe_stack_instance(
        self, **kwargs: Unpack[DescribeStackInstanceInputRequestTypeDef]
    ) -> DescribeStackInstanceOutputTypeDef:
        """
        Returns the stack instance that's associated with the specified StackSet,
        Amazon Web Services account, and Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_instance)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_stack_instance)
        """

    def describe_stack_resource(
        self, **kwargs: Unpack[DescribeStackResourceInputRequestTypeDef]
    ) -> DescribeStackResourceOutputTypeDef:
        """
        Returns a description of the specified resource in the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_stack_resource)
        """

    def describe_stack_resource_drifts(
        self, **kwargs: Unpack[DescribeStackResourceDriftsInputRequestTypeDef]
    ) -> DescribeStackResourceDriftsOutputTypeDef:
        """
        Returns drift information for the resources that have been checked for drift in
        the specified
        stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_resource_drifts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_stack_resource_drifts)
        """

    def describe_stack_resources(
        self, **kwargs: Unpack[DescribeStackResourcesInputRequestTypeDef]
    ) -> DescribeStackResourcesOutputTypeDef:
        """
        Returns Amazon Web Services resource descriptions for running and deleted
        stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_stack_resources)
        """

    def describe_stack_set(
        self, **kwargs: Unpack[DescribeStackSetInputRequestTypeDef]
    ) -> DescribeStackSetOutputTypeDef:
        """
        Returns the description of the specified StackSet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_stack_set)
        """

    def describe_stack_set_operation(
        self, **kwargs: Unpack[DescribeStackSetOperationInputRequestTypeDef]
    ) -> DescribeStackSetOperationOutputTypeDef:
        """
        Returns the description of the specified StackSet operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_set_operation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_stack_set_operation)
        """

    def describe_stacks(
        self, **kwargs: Unpack[DescribeStacksInputRequestTypeDef]
    ) -> DescribeStacksOutputTypeDef:
        """
        Returns the description for the specified stack; if no stack name was
        specified, then it returns the description for all the stacks
        created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stacks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_stacks)
        """

    def describe_type(
        self, **kwargs: Unpack[DescribeTypeInputRequestTypeDef]
    ) -> DescribeTypeOutputTypeDef:
        """
        Returns detailed information about an extension that has been registered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_type)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_type)
        """

    def describe_type_registration(
        self, **kwargs: Unpack[DescribeTypeRegistrationInputRequestTypeDef]
    ) -> DescribeTypeRegistrationOutputTypeDef:
        """
        Returns information about an extension's registration, including its current
        status and type and version
        identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_type_registration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#describe_type_registration)
        """

    def detect_stack_drift(
        self, **kwargs: Unpack[DetectStackDriftInputRequestTypeDef]
    ) -> DetectStackDriftOutputTypeDef:
        """
        Detects whether a stack's actual configuration differs, or has *drifted*, from
        its expected configuration, as defined in the stack template and any values
        specified as template
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.detect_stack_drift)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#detect_stack_drift)
        """

    def detect_stack_resource_drift(
        self, **kwargs: Unpack[DetectStackResourceDriftInputRequestTypeDef]
    ) -> DetectStackResourceDriftOutputTypeDef:
        """
        Returns information about whether a resource's actual configuration differs, or
        has *drifted*, from its expected configuration, as defined in the stack
        template and any values specified as template
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.detect_stack_resource_drift)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#detect_stack_resource_drift)
        """

    def detect_stack_set_drift(
        self, **kwargs: Unpack[DetectStackSetDriftInputRequestTypeDef]
    ) -> DetectStackSetDriftOutputTypeDef:
        """
        Detect drift on a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.detect_stack_set_drift)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#detect_stack_set_drift)
        """

    def estimate_template_cost(
        self, **kwargs: Unpack[EstimateTemplateCostInputRequestTypeDef]
    ) -> EstimateTemplateCostOutputTypeDef:
        """
        Returns the estimated monthly cost of a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.estimate_template_cost)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#estimate_template_cost)
        """

    def execute_change_set(
        self, **kwargs: Unpack[ExecuteChangeSetInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a stack using the input information that was provided when the
        specified change set was
        created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.execute_change_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#execute_change_set)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#generate_presigned_url)
        """

    def get_generated_template(
        self, **kwargs: Unpack[GetGeneratedTemplateInputRequestTypeDef]
    ) -> GetGeneratedTemplateOutputTypeDef:
        """
        Retrieves a generated template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_generated_template)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_generated_template)
        """

    def get_stack_policy(
        self, **kwargs: Unpack[GetStackPolicyInputRequestTypeDef]
    ) -> GetStackPolicyOutputTypeDef:
        """
        Returns the stack policy for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_stack_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_stack_policy)
        """

    def get_template(
        self, **kwargs: Unpack[GetTemplateInputRequestTypeDef]
    ) -> GetTemplateOutputTypeDef:
        """
        Returns the template body for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_template)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_template)
        """

    def get_template_summary(
        self, **kwargs: Unpack[GetTemplateSummaryInputRequestTypeDef]
    ) -> GetTemplateSummaryOutputTypeDef:
        """
        Returns information about a new or existing template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_template_summary)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_template_summary)
        """

    def import_stacks_to_stack_set(
        self, **kwargs: Unpack[ImportStacksToStackSetInputRequestTypeDef]
    ) -> ImportStacksToStackSetOutputTypeDef:
        """
        Import existing stacks into a new stack sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.import_stacks_to_stack_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#import_stacks_to_stack_set)
        """

    def list_change_sets(
        self, **kwargs: Unpack[ListChangeSetsInputRequestTypeDef]
    ) -> ListChangeSetsOutputTypeDef:
        """
        Returns the ID and status of each active change set for a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_change_sets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_change_sets)
        """

    def list_exports(
        self, **kwargs: Unpack[ListExportsInputRequestTypeDef]
    ) -> ListExportsOutputTypeDef:
        """
        Lists all exported output values in the account and Region in which you call
        this
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_exports)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_exports)
        """

    def list_generated_templates(
        self, **kwargs: Unpack[ListGeneratedTemplatesInputRequestTypeDef]
    ) -> ListGeneratedTemplatesOutputTypeDef:
        """
        Lists your generated templates in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_generated_templates)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_generated_templates)
        """

    def list_imports(
        self, **kwargs: Unpack[ListImportsInputRequestTypeDef]
    ) -> ListImportsOutputTypeDef:
        """
        Lists all stacks that are importing an exported output value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_imports)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_imports)
        """

    def list_resource_scan_related_resources(
        self, **kwargs: Unpack[ListResourceScanRelatedResourcesInputRequestTypeDef]
    ) -> ListResourceScanRelatedResourcesOutputTypeDef:
        """
        Lists the related resources for a list of resources from a resource scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_resource_scan_related_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_resource_scan_related_resources)
        """

    def list_resource_scan_resources(
        self, **kwargs: Unpack[ListResourceScanResourcesInputRequestTypeDef]
    ) -> ListResourceScanResourcesOutputTypeDef:
        """
        Lists the resources from a resource scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_resource_scan_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_resource_scan_resources)
        """

    def list_resource_scans(
        self, **kwargs: Unpack[ListResourceScansInputRequestTypeDef]
    ) -> ListResourceScansOutputTypeDef:
        """
        List the resource scans from newest to oldest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_resource_scans)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_resource_scans)
        """

    def list_stack_instance_resource_drifts(
        self, **kwargs: Unpack[ListStackInstanceResourceDriftsInputRequestTypeDef]
    ) -> ListStackInstanceResourceDriftsOutputTypeDef:
        """
        Returns drift information for resources in a stack instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_instance_resource_drifts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_stack_instance_resource_drifts)
        """

    def list_stack_instances(
        self, **kwargs: Unpack[ListStackInstancesInputRequestTypeDef]
    ) -> ListStackInstancesOutputTypeDef:
        """
        Returns summary information about stack instances that are associated with the
        specified stack
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_instances)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_stack_instances)
        """

    def list_stack_resources(
        self, **kwargs: Unpack[ListStackResourcesInputRequestTypeDef]
    ) -> ListStackResourcesOutputTypeDef:
        """
        Returns descriptions of all resources of the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_resources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_stack_resources)
        """

    def list_stack_set_auto_deployment_targets(
        self, **kwargs: Unpack[ListStackSetAutoDeploymentTargetsInputRequestTypeDef]
    ) -> ListStackSetAutoDeploymentTargetsOutputTypeDef:
        """
        Returns summary information about deployment targets for a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_set_auto_deployment_targets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_stack_set_auto_deployment_targets)
        """

    def list_stack_set_operation_results(
        self, **kwargs: Unpack[ListStackSetOperationResultsInputRequestTypeDef]
    ) -> ListStackSetOperationResultsOutputTypeDef:
        """
        Returns summary information about the results of a stack set operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_set_operation_results)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_stack_set_operation_results)
        """

    def list_stack_set_operations(
        self, **kwargs: Unpack[ListStackSetOperationsInputRequestTypeDef]
    ) -> ListStackSetOperationsOutputTypeDef:
        """
        Returns summary information about operations performed on a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_set_operations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_stack_set_operations)
        """

    def list_stack_sets(
        self, **kwargs: Unpack[ListStackSetsInputRequestTypeDef]
    ) -> ListStackSetsOutputTypeDef:
        """
        Returns summary information about stack sets that are associated with the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_sets)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_stack_sets)
        """

    def list_stacks(
        self, **kwargs: Unpack[ListStacksInputRequestTypeDef]
    ) -> ListStacksOutputTypeDef:
        """
        Returns the summary information for stacks whose status matches the specified
        StackStatusFilter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stacks)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_stacks)
        """

    def list_type_registrations(
        self, **kwargs: Unpack[ListTypeRegistrationsInputRequestTypeDef]
    ) -> ListTypeRegistrationsOutputTypeDef:
        """
        Returns a list of registration tokens for the specified extension(s).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_type_registrations)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_type_registrations)
        """

    def list_type_versions(
        self, **kwargs: Unpack[ListTypeVersionsInputRequestTypeDef]
    ) -> ListTypeVersionsOutputTypeDef:
        """
        Returns summary information about the versions of an extension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_type_versions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_type_versions)
        """

    def list_types(self, **kwargs: Unpack[ListTypesInputRequestTypeDef]) -> ListTypesOutputTypeDef:
        """
        Returns summary information about extension that have been registered with
        CloudFormation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_types)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#list_types)
        """

    def publish_type(
        self, **kwargs: Unpack[PublishTypeInputRequestTypeDef]
    ) -> PublishTypeOutputTypeDef:
        """
        Publishes the specified extension to the CloudFormation registry as a public
        extension in this
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.publish_type)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#publish_type)
        """

    def record_handler_progress(
        self, **kwargs: Unpack[RecordHandlerProgressInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Reports progress of a resource handler to CloudFormation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.record_handler_progress)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#record_handler_progress)
        """

    def register_publisher(
        self, **kwargs: Unpack[RegisterPublisherInputRequestTypeDef]
    ) -> RegisterPublisherOutputTypeDef:
        """
        Registers your account as a publisher of public extensions in the
        CloudFormation
        registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.register_publisher)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#register_publisher)
        """

    def register_type(
        self, **kwargs: Unpack[RegisterTypeInputRequestTypeDef]
    ) -> RegisterTypeOutputTypeDef:
        """
        Registers an extension with the CloudFormation service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.register_type)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#register_type)
        """

    def rollback_stack(
        self, **kwargs: Unpack[RollbackStackInputRequestTypeDef]
    ) -> RollbackStackOutputTypeDef:
        """
        When specifying `RollbackStack`, you preserve the state of previously
        provisioned resources when an operation
        fails.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.rollback_stack)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#rollback_stack)
        """

    def set_stack_policy(
        self, **kwargs: Unpack[SetStackPolicyInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets a stack policy for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.set_stack_policy)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#set_stack_policy)
        """

    def set_type_configuration(
        self, **kwargs: Unpack[SetTypeConfigurationInputRequestTypeDef]
    ) -> SetTypeConfigurationOutputTypeDef:
        """
        Specifies the configuration data for a registered CloudFormation extension, in
        the given account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.set_type_configuration)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#set_type_configuration)
        """

    def set_type_default_version(
        self, **kwargs: Unpack[SetTypeDefaultVersionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Specify the default version of an extension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.set_type_default_version)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#set_type_default_version)
        """

    def signal_resource(
        self, **kwargs: Unpack[SignalResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sends a signal to the specified resource with a success or failure status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.signal_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#signal_resource)
        """

    def start_resource_scan(
        self, **kwargs: Unpack[StartResourceScanInputRequestTypeDef]
    ) -> StartResourceScanOutputTypeDef:
        """
        Starts a scan of the resources in this account in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.start_resource_scan)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#start_resource_scan)
        """

    def stop_stack_set_operation(
        self, **kwargs: Unpack[StopStackSetOperationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an in-progress operation on a stack set and its associated stack
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.stop_stack_set_operation)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#stop_stack_set_operation)
        """

    def test_type(self, **kwargs: Unpack[TestTypeInputRequestTypeDef]) -> TestTypeOutputTypeDef:
        """
        Tests a registered extension to make sure it meets all necessary requirements
        for being published in the CloudFormation
        registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.test_type)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#test_type)
        """

    def update_generated_template(
        self, **kwargs: Unpack[UpdateGeneratedTemplateInputRequestTypeDef]
    ) -> UpdateGeneratedTemplateOutputTypeDef:
        """
        Updates a generated template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_generated_template)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#update_generated_template)
        """

    def update_stack(
        self, **kwargs: Unpack[UpdateStackInputRequestTypeDef]
    ) -> UpdateStackOutputTypeDef:
        """
        Updates a stack as specified in the template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_stack)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#update_stack)
        """

    def update_stack_instances(
        self, **kwargs: Unpack[UpdateStackInstancesInputRequestTypeDef]
    ) -> UpdateStackInstancesOutputTypeDef:
        """
        Updates the parameter values for stack instances for the specified accounts,
        within the specified Amazon Web Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_stack_instances)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#update_stack_instances)
        """

    def update_stack_set(
        self, **kwargs: Unpack[UpdateStackSetInputRequestTypeDef]
    ) -> UpdateStackSetOutputTypeDef:
        """
        Updates the stack set, and associated stack instances in the specified accounts
        and Amazon Web Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_stack_set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#update_stack_set)
        """

    def update_termination_protection(
        self, **kwargs: Unpack[UpdateTerminationProtectionInputRequestTypeDef]
    ) -> UpdateTerminationProtectionOutputTypeDef:
        """
        Updates termination protection for the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_termination_protection)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#update_termination_protection)
        """

    def validate_template(
        self, **kwargs: Unpack[ValidateTemplateInputRequestTypeDef]
    ) -> ValidateTemplateOutputTypeDef:
        """
        Validates a specified template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.validate_template)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#validate_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_account_limits"]
    ) -> DescribeAccountLimitsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_change_set"]
    ) -> DescribeChangeSetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_stack_events"]
    ) -> DescribeStackEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_stacks"]) -> DescribeStacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_change_sets"]) -> ListChangeSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_exports"]) -> ListExportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_generated_templates"]
    ) -> ListGeneratedTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_imports"]) -> ListImportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_scan_related_resources"]
    ) -> ListResourceScanRelatedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_scan_resources"]
    ) -> ListResourceScanResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_scans"]
    ) -> ListResourceScansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stack_instances"]
    ) -> ListStackInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stack_resources"]
    ) -> ListStackResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stack_set_operation_results"]
    ) -> ListStackSetOperationResultsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stack_set_operations"]
    ) -> ListStackSetOperationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_stack_sets"]) -> ListStackSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_stacks"]) -> ListStacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_types"]) -> ListTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["change_set_create_complete"]
    ) -> ChangeSetCreateCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_create_complete"]
    ) -> StackCreateCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_delete_complete"]
    ) -> StackDeleteCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["stack_exists"]) -> StackExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_import_complete"]
    ) -> StackImportCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_rollback_complete"]
    ) -> StackRollbackCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_update_complete"]
    ) -> StackUpdateCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["type_registration_complete"]
    ) -> TypeRegistrationCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/client/#get_waiter)
        """
