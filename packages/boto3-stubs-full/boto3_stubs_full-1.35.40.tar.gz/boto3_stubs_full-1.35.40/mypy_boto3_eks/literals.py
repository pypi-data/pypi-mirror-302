"""
Type annotations for eks service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/literals/)

Usage::

    ```python
    from mypy_boto3_eks.literals import AMITypesType

    data: AMITypesType = "AL2023_ARM_64_STANDARD"
    ```
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "AMITypesType",
    "AccessScopeTypeType",
    "AddonActiveWaiterName",
    "AddonDeletedWaiterName",
    "AddonIssueCodeType",
    "AddonStatusType",
    "AuthenticationModeType",
    "CapacityTypesType",
    "CategoryType",
    "ClusterActiveWaiterName",
    "ClusterDeletedWaiterName",
    "ClusterIssueCodeType",
    "ClusterStatusType",
    "ConfigStatusType",
    "ConnectorConfigProviderType",
    "DescribeAddonVersionsPaginatorName",
    "EksAnywhereSubscriptionLicenseTypeType",
    "EksAnywhereSubscriptionStatusType",
    "EksAnywhereSubscriptionTermUnitType",
    "ErrorCodeType",
    "FargateProfileActiveWaiterName",
    "FargateProfileDeletedWaiterName",
    "FargateProfileIssueCodeType",
    "FargateProfileStatusType",
    "InsightStatusValueType",
    "IpFamilyType",
    "ListAccessEntriesPaginatorName",
    "ListAccessPoliciesPaginatorName",
    "ListAddonsPaginatorName",
    "ListAssociatedAccessPoliciesPaginatorName",
    "ListClustersPaginatorName",
    "ListEksAnywhereSubscriptionsPaginatorName",
    "ListFargateProfilesPaginatorName",
    "ListIdentityProviderConfigsPaginatorName",
    "ListInsightsPaginatorName",
    "ListNodegroupsPaginatorName",
    "ListPodIdentityAssociationsPaginatorName",
    "ListUpdatesPaginatorName",
    "LogTypeType",
    "NodegroupActiveWaiterName",
    "NodegroupDeletedWaiterName",
    "NodegroupIssueCodeType",
    "NodegroupStatusType",
    "ResolveConflictsType",
    "SupportTypeType",
    "TaintEffectType",
    "UpdateParamTypeType",
    "UpdateStatusType",
    "UpdateTypeType",
    "EKSServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "WaiterName",
    "RegionName",
)


AMITypesType = Literal[
    "AL2023_ARM_64_STANDARD",
    "AL2023_x86_64_NEURON",
    "AL2023_x86_64_NVIDIA",
    "AL2023_x86_64_STANDARD",
    "AL2_ARM_64",
    "AL2_x86_64",
    "AL2_x86_64_GPU",
    "BOTTLEROCKET_ARM_64",
    "BOTTLEROCKET_ARM_64_NVIDIA",
    "BOTTLEROCKET_x86_64",
    "BOTTLEROCKET_x86_64_NVIDIA",
    "CUSTOM",
    "WINDOWS_CORE_2019_x86_64",
    "WINDOWS_CORE_2022_x86_64",
    "WINDOWS_FULL_2019_x86_64",
    "WINDOWS_FULL_2022_x86_64",
]
AccessScopeTypeType = Literal["cluster", "namespace"]
AddonActiveWaiterName = Literal["addon_active"]
AddonDeletedWaiterName = Literal["addon_deleted"]
AddonIssueCodeType = Literal[
    "AccessDenied",
    "AddonPermissionFailure",
    "AddonSubscriptionNeeded",
    "AdmissionRequestDenied",
    "ClusterUnreachable",
    "ConfigurationConflict",
    "InsufficientNumberOfReplicas",
    "InternalFailure",
    "K8sResourceNotFound",
    "UnsupportedAddonModification",
]
AddonStatusType = Literal[
    "ACTIVE",
    "CREATE_FAILED",
    "CREATING",
    "DEGRADED",
    "DELETE_FAILED",
    "DELETING",
    "UPDATE_FAILED",
    "UPDATING",
]
AuthenticationModeType = Literal["API", "API_AND_CONFIG_MAP", "CONFIG_MAP"]
CapacityTypesType = Literal["CAPACITY_BLOCK", "ON_DEMAND", "SPOT"]
CategoryType = Literal["UPGRADE_READINESS"]
ClusterActiveWaiterName = Literal["cluster_active"]
ClusterDeletedWaiterName = Literal["cluster_deleted"]
ClusterIssueCodeType = Literal[
    "AccessDenied",
    "ClusterUnreachable",
    "ConfigurationConflict",
    "Ec2SecurityGroupNotFound",
    "Ec2ServiceNotSubscribed",
    "Ec2SubnetNotFound",
    "IamRoleNotFound",
    "InsufficientFreeAddresses",
    "InternalFailure",
    "KmsGrantRevoked",
    "KmsKeyDisabled",
    "KmsKeyMarkedForDeletion",
    "KmsKeyNotFound",
    "Other",
    "ResourceLimitExceeded",
    "ResourceNotFound",
    "StsRegionalEndpointDisabled",
    "UnsupportedVersion",
    "VpcNotFound",
]
ClusterStatusType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "PENDING", "UPDATING"]
ConfigStatusType = Literal["ACTIVE", "CREATING", "DELETING"]
ConnectorConfigProviderType = Literal[
    "AKS", "ANTHOS", "EC2", "EKS_ANYWHERE", "GKE", "OPENSHIFT", "OTHER", "RANCHER", "TANZU"
]
DescribeAddonVersionsPaginatorName = Literal["describe_addon_versions"]
EksAnywhereSubscriptionLicenseTypeType = Literal["Cluster"]
EksAnywhereSubscriptionStatusType = Literal[
    "ACTIVE", "CREATING", "DELETING", "EXPIRED", "EXPIRING", "UPDATING"
]
EksAnywhereSubscriptionTermUnitType = Literal["MONTHS"]
ErrorCodeType = Literal[
    "AccessDenied",
    "AdmissionRequestDenied",
    "ClusterUnreachable",
    "ConfigurationConflict",
    "EniLimitReached",
    "InsufficientFreeAddresses",
    "InsufficientNumberOfReplicas",
    "IpNotAvailable",
    "K8sResourceNotFound",
    "NodeCreationFailure",
    "OperationNotPermitted",
    "PodEvictionFailure",
    "SecurityGroupNotFound",
    "SubnetNotFound",
    "Unknown",
    "UnsupportedAddonModification",
    "VpcIdNotFound",
]
FargateProfileActiveWaiterName = Literal["fargate_profile_active"]
FargateProfileDeletedWaiterName = Literal["fargate_profile_deleted"]
FargateProfileIssueCodeType = Literal[
    "AccessDenied", "ClusterUnreachable", "InternalFailure", "PodExecutionRoleAlreadyInUse"
]
FargateProfileStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING"
]
InsightStatusValueType = Literal["ERROR", "PASSING", "UNKNOWN", "WARNING"]
IpFamilyType = Literal["ipv4", "ipv6"]
ListAccessEntriesPaginatorName = Literal["list_access_entries"]
ListAccessPoliciesPaginatorName = Literal["list_access_policies"]
ListAddonsPaginatorName = Literal["list_addons"]
ListAssociatedAccessPoliciesPaginatorName = Literal["list_associated_access_policies"]
ListClustersPaginatorName = Literal["list_clusters"]
ListEksAnywhereSubscriptionsPaginatorName = Literal["list_eks_anywhere_subscriptions"]
ListFargateProfilesPaginatorName = Literal["list_fargate_profiles"]
ListIdentityProviderConfigsPaginatorName = Literal["list_identity_provider_configs"]
ListInsightsPaginatorName = Literal["list_insights"]
ListNodegroupsPaginatorName = Literal["list_nodegroups"]
ListPodIdentityAssociationsPaginatorName = Literal["list_pod_identity_associations"]
ListUpdatesPaginatorName = Literal["list_updates"]
LogTypeType = Literal["api", "audit", "authenticator", "controllerManager", "scheduler"]
NodegroupActiveWaiterName = Literal["nodegroup_active"]
NodegroupDeletedWaiterName = Literal["nodegroup_deleted"]
NodegroupIssueCodeType = Literal[
    "AccessDenied",
    "AmiIdNotFound",
    "AsgInstanceLaunchFailures",
    "AutoScalingGroupInstanceRefreshActive",
    "AutoScalingGroupInvalidConfiguration",
    "AutoScalingGroupNotFound",
    "AutoScalingGroupOptInRequired",
    "AutoScalingGroupRateLimitExceeded",
    "ClusterUnreachable",
    "Ec2LaunchTemplateDeletionFailure",
    "Ec2LaunchTemplateInvalidConfiguration",
    "Ec2LaunchTemplateMaxLimitExceeded",
    "Ec2LaunchTemplateNotFound",
    "Ec2LaunchTemplateVersionMaxLimitExceeded",
    "Ec2LaunchTemplateVersionMismatch",
    "Ec2SecurityGroupDeletionFailure",
    "Ec2SecurityGroupNotFound",
    "Ec2SubnetInvalidConfiguration",
    "Ec2SubnetListTooLong",
    "Ec2SubnetMissingIpv6Assignment",
    "Ec2SubnetNotFound",
    "IamInstanceProfileNotFound",
    "IamLimitExceeded",
    "IamNodeRoleNotFound",
    "IamThrottling",
    "InstanceLimitExceeded",
    "InsufficientFreeAddresses",
    "InternalFailure",
    "KubernetesLabelInvalid",
    "LimitExceeded",
    "NodeCreationFailure",
    "NodeTerminationFailure",
    "PodEvictionFailure",
    "SourceEc2LaunchTemplateNotFound",
    "Unknown",
]
NodegroupStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DEGRADED", "DELETE_FAILED", "DELETING", "UPDATING"
]
ResolveConflictsType = Literal["NONE", "OVERWRITE", "PRESERVE"]
SupportTypeType = Literal["EXTENDED", "STANDARD"]
TaintEffectType = Literal["NO_EXECUTE", "NO_SCHEDULE", "PREFER_NO_SCHEDULE"]
UpdateParamTypeType = Literal[
    "AddonVersion",
    "AuthenticationMode",
    "ClusterLogging",
    "ConfigurationValues",
    "DesiredSize",
    "EncryptionConfig",
    "EndpointPrivateAccess",
    "EndpointPublicAccess",
    "IdentityProviderConfig",
    "LabelsToAdd",
    "LabelsToRemove",
    "LaunchTemplateName",
    "LaunchTemplateVersion",
    "MaxSize",
    "MaxUnavailable",
    "MaxUnavailablePercentage",
    "MinSize",
    "PlatformVersion",
    "PodIdentityAssociations",
    "PublicAccessCidrs",
    "ReleaseVersion",
    "ResolveConflicts",
    "SecurityGroups",
    "ServiceAccountRoleArn",
    "Subnets",
    "TaintsToAdd",
    "TaintsToRemove",
    "UpgradePolicy",
    "Version",
]
UpdateStatusType = Literal["Cancelled", "Failed", "InProgress", "Successful"]
UpdateTypeType = Literal[
    "AccessConfigUpdate",
    "AddonUpdate",
    "AssociateEncryptionConfig",
    "AssociateIdentityProviderConfig",
    "ConfigUpdate",
    "DisassociateIdentityProviderConfig",
    "EndpointAccessUpdate",
    "LoggingUpdate",
    "UpgradePolicyUpdate",
    "VersionUpdate",
    "VpcConfigUpdate",
]
EKSServiceName = Literal["eks"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "amp",
    "amplify",
    "amplifybackend",
    "amplifyuibuilder",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appconfigdata",
    "appfabric",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "application-signals",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "apptest",
    "arc-zonal-shift",
    "artifact",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "b2bi",
    "backup",
    "backup-gateway",
    "batch",
    "bcm-data-exports",
    "bedrock",
    "bedrock-agent",
    "bedrock-agent-runtime",
    "bedrock-runtime",
    "billingconductor",
    "braket",
    "budgets",
    "ce",
    "chatbot",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-media-pipelines",
    "chime-sdk-meetings",
    "chime-sdk-messaging",
    "chime-sdk-voice",
    "cleanrooms",
    "cleanroomsml",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudfront-keyvaluestore",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudtrail-data",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecatalyst",
    "codecommit",
    "codeconnections",
    "codedeploy",
    "codeguru-reviewer",
    "codeguru-security",
    "codeguruprofiler",
    "codepipeline",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectcampaigns",
    "connectcases",
    "connectparticipant",
    "controlcatalog",
    "controltower",
    "cost-optimization-hub",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "datazone",
    "dax",
    "deadline",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "docdb-elastic",
    "drs",
    "ds",
    "ds-data",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "eks-auth",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "emr-serverless",
    "entityresolution",
    "es",
    "events",
    "evidently",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "freetier",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "inspector-scan",
    "inspector2",
    "internetmonitor",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotfleetwise",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iottwinmaker",
    "iotwireless",
    "ivs",
    "ivs-realtime",
    "ivschat",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kendra-ranking",
    "keyspaces",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesis-video-webrtc-storage",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "launch-wizard",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "license-manager-linux-subscriptions",
    "license-manager-user-subscriptions",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "m2",
    "machinelearning",
    "macie2",
    "mailmanager",
    "managedblockchain",
    "managedblockchain-query",
    "marketplace-agreement",
    "marketplace-catalog",
    "marketplace-deployment",
    "marketplace-entitlement",
    "marketplace-reporting",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediapackagev2",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "medical-imaging",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migration-hub-refactor-spaces",
    "migrationhub-config",
    "migrationhuborchestrator",
    "migrationhubstrategy",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "neptune-graph",
    "neptunedata",
    "network-firewall",
    "networkmanager",
    "networkmonitor",
    "nimble",
    "oam",
    "omics",
    "opensearch",
    "opensearchserverless",
    "opsworks",
    "opsworkscm",
    "organizations",
    "osis",
    "outposts",
    "panorama",
    "payment-cryptography",
    "payment-cryptography-data",
    "pca-connector-ad",
    "pca-connector-scep",
    "pcs",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "pinpoint-sms-voice-v2",
    "pipes",
    "polly",
    "pricing",
    "privatenetworks",
    "proton",
    "qapps",
    "qbusiness",
    "qconnect",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rbin",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "redshift-serverless",
    "rekognition",
    "repostspace",
    "resiliencehub",
    "resource-explorer-2",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "rolesanywhere",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53profiles",
    "route53resolver",
    "rum",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-geospatial",
    "sagemaker-metrics",
    "sagemaker-runtime",
    "savingsplans",
    "scheduler",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "securitylake",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "simspaceweaver",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "socialmessaging",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "ssm-quicksetup",
    "ssm-sap",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "supplychain",
    "support",
    "support-app",
    "swf",
    "synthetics",
    "taxsettings",
    "textract",
    "timestream-influxdb",
    "timestream-query",
    "timestream-write",
    "tnb",
    "transcribe",
    "transfer",
    "translate",
    "trustedadvisor",
    "verifiedpermissions",
    "voice-id",
    "vpc-lattice",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "workspaces-thin-client",
    "workspaces-web",
    "xray",
]
ResourceServiceName = Literal[
    "cloudformation",
    "cloudwatch",
    "dynamodb",
    "ec2",
    "glacier",
    "iam",
    "opsworks",
    "s3",
    "sns",
    "sqs",
]
PaginatorName = Literal[
    "describe_addon_versions",
    "list_access_entries",
    "list_access_policies",
    "list_addons",
    "list_associated_access_policies",
    "list_clusters",
    "list_eks_anywhere_subscriptions",
    "list_fargate_profiles",
    "list_identity_provider_configs",
    "list_insights",
    "list_nodegroups",
    "list_pod_identity_associations",
    "list_updates",
]
WaiterName = Literal[
    "addon_active",
    "addon_deleted",
    "cluster_active",
    "cluster_deleted",
    "fargate_profile_active",
    "fargate_profile_deleted",
    "nodegroup_active",
    "nodegroup_deleted",
]
RegionName = Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ap-southeast-5",
    "ca-central-1",
    "ca-west-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "il-central-1",
    "me-central-1",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
