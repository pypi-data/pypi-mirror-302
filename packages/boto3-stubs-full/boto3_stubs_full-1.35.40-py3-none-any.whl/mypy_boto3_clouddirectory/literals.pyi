"""
Type annotations for clouddirectory service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/literals/)

Usage::

    ```python
    from mypy_boto3_clouddirectory.literals import BatchReadExceptionTypeType

    data: BatchReadExceptionTypeType = "AccessDeniedException"
    ```
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "BatchReadExceptionTypeType",
    "ConsistencyLevelType",
    "DirectoryStateType",
    "FacetAttributeTypeType",
    "FacetStyleType",
    "ListAppliedSchemaArnsPaginatorName",
    "ListAttachedIndicesPaginatorName",
    "ListDevelopmentSchemaArnsPaginatorName",
    "ListDirectoriesPaginatorName",
    "ListFacetAttributesPaginatorName",
    "ListFacetNamesPaginatorName",
    "ListIncomingTypedLinksPaginatorName",
    "ListIndexPaginatorName",
    "ListManagedSchemaArnsPaginatorName",
    "ListObjectAttributesPaginatorName",
    "ListObjectParentPathsPaginatorName",
    "ListObjectPoliciesPaginatorName",
    "ListOutgoingTypedLinksPaginatorName",
    "ListPolicyAttachmentsPaginatorName",
    "ListPublishedSchemaArnsPaginatorName",
    "ListTagsForResourcePaginatorName",
    "ListTypedLinkFacetAttributesPaginatorName",
    "ListTypedLinkFacetNamesPaginatorName",
    "LookupPolicyPaginatorName",
    "ObjectTypeType",
    "RangeModeType",
    "RequiredAttributeBehaviorType",
    "RuleTypeType",
    "UpdateActionTypeType",
    "CloudDirectoryServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "RegionName",
)

BatchReadExceptionTypeType = Literal[
    "AccessDeniedException",
    "CannotListParentOfRootException",
    "DirectoryNotEnabledException",
    "FacetValidationException",
    "InternalServiceException",
    "InvalidArnException",
    "InvalidNextTokenException",
    "LimitExceededException",
    "NotIndexException",
    "NotNodeException",
    "NotPolicyException",
    "ResourceNotFoundException",
    "ValidationException",
]
ConsistencyLevelType = Literal["EVENTUAL", "SERIALIZABLE"]
DirectoryStateType = Literal["DELETED", "DISABLED", "ENABLED"]
FacetAttributeTypeType = Literal["BINARY", "BOOLEAN", "DATETIME", "NUMBER", "STRING", "VARIANT"]
FacetStyleType = Literal["DYNAMIC", "STATIC"]
ListAppliedSchemaArnsPaginatorName = Literal["list_applied_schema_arns"]
ListAttachedIndicesPaginatorName = Literal["list_attached_indices"]
ListDevelopmentSchemaArnsPaginatorName = Literal["list_development_schema_arns"]
ListDirectoriesPaginatorName = Literal["list_directories"]
ListFacetAttributesPaginatorName = Literal["list_facet_attributes"]
ListFacetNamesPaginatorName = Literal["list_facet_names"]
ListIncomingTypedLinksPaginatorName = Literal["list_incoming_typed_links"]
ListIndexPaginatorName = Literal["list_index"]
ListManagedSchemaArnsPaginatorName = Literal["list_managed_schema_arns"]
ListObjectAttributesPaginatorName = Literal["list_object_attributes"]
ListObjectParentPathsPaginatorName = Literal["list_object_parent_paths"]
ListObjectPoliciesPaginatorName = Literal["list_object_policies"]
ListOutgoingTypedLinksPaginatorName = Literal["list_outgoing_typed_links"]
ListPolicyAttachmentsPaginatorName = Literal["list_policy_attachments"]
ListPublishedSchemaArnsPaginatorName = Literal["list_published_schema_arns"]
ListTagsForResourcePaginatorName = Literal["list_tags_for_resource"]
ListTypedLinkFacetAttributesPaginatorName = Literal["list_typed_link_facet_attributes"]
ListTypedLinkFacetNamesPaginatorName = Literal["list_typed_link_facet_names"]
LookupPolicyPaginatorName = Literal["lookup_policy"]
ObjectTypeType = Literal["INDEX", "LEAF_NODE", "NODE", "POLICY"]
RangeModeType = Literal["EXCLUSIVE", "FIRST", "INCLUSIVE", "LAST", "LAST_BEFORE_MISSING_VALUES"]
RequiredAttributeBehaviorType = Literal["NOT_REQUIRED", "REQUIRED_ALWAYS"]
RuleTypeType = Literal["BINARY_LENGTH", "NUMBER_COMPARISON", "STRING_FROM_SET", "STRING_LENGTH"]
UpdateActionTypeType = Literal["CREATE_OR_UPDATE", "DELETE"]
CloudDirectoryServiceName = Literal["clouddirectory"]
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
    "list_applied_schema_arns",
    "list_attached_indices",
    "list_development_schema_arns",
    "list_directories",
    "list_facet_attributes",
    "list_facet_names",
    "list_incoming_typed_links",
    "list_index",
    "list_managed_schema_arns",
    "list_object_attributes",
    "list_object_parent_paths",
    "list_object_policies",
    "list_outgoing_typed_links",
    "list_policy_attachments",
    "list_published_schema_arns",
    "list_tags_for_resource",
    "list_typed_link_facet_attributes",
    "list_typed_link_facet_names",
    "lookup_policy",
]
RegionName = Literal[
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "us-east-1",
    "us-east-2",
    "us-west-2",
]
