"""
Type annotations for cloudfront service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/literals/)

Usage::

    ```python
    from mypy_boto3_cloudfront.literals import CachePolicyCookieBehaviorType

    data: CachePolicyCookieBehaviorType = "all"
    ```
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "CachePolicyCookieBehaviorType",
    "CachePolicyHeaderBehaviorType",
    "CachePolicyQueryStringBehaviorType",
    "CachePolicyTypeType",
    "CertificateSourceType",
    "ContinuousDeploymentPolicyTypeType",
    "DistributionDeployedWaiterName",
    "EventTypeType",
    "FormatType",
    "FrameOptionsListType",
    "FunctionRuntimeType",
    "FunctionStageType",
    "GeoRestrictionTypeType",
    "HttpVersionType",
    "ICPRecordalStatusType",
    "ImportSourceTypeType",
    "InvalidationCompletedWaiterName",
    "ItemSelectionType",
    "ListCloudFrontOriginAccessIdentitiesPaginatorName",
    "ListDistributionsPaginatorName",
    "ListInvalidationsPaginatorName",
    "ListKeyValueStoresPaginatorName",
    "ListStreamingDistributionsPaginatorName",
    "MethodType",
    "MinimumProtocolVersionType",
    "OriginAccessControlOriginTypesType",
    "OriginAccessControlSigningBehaviorsType",
    "OriginAccessControlSigningProtocolsType",
    "OriginProtocolPolicyType",
    "OriginRequestPolicyCookieBehaviorType",
    "OriginRequestPolicyHeaderBehaviorType",
    "OriginRequestPolicyQueryStringBehaviorType",
    "OriginRequestPolicyTypeType",
    "PriceClassType",
    "RealtimeMetricsSubscriptionStatusType",
    "ReferrerPolicyListType",
    "ResponseHeadersPolicyAccessControlAllowMethodsValuesType",
    "ResponseHeadersPolicyTypeType",
    "SSLSupportMethodType",
    "SslProtocolType",
    "StreamingDistributionDeployedWaiterName",
    "ViewerProtocolPolicyType",
    "CloudFrontServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "WaiterName",
)


CachePolicyCookieBehaviorType = Literal["all", "allExcept", "none", "whitelist"]
CachePolicyHeaderBehaviorType = Literal["none", "whitelist"]
CachePolicyQueryStringBehaviorType = Literal["all", "allExcept", "none", "whitelist"]
CachePolicyTypeType = Literal["custom", "managed"]
CertificateSourceType = Literal["acm", "cloudfront", "iam"]
ContinuousDeploymentPolicyTypeType = Literal["SingleHeader", "SingleWeight"]
DistributionDeployedWaiterName = Literal["distribution_deployed"]
EventTypeType = Literal["origin-request", "origin-response", "viewer-request", "viewer-response"]
FormatType = Literal["URLEncoded"]
FrameOptionsListType = Literal["DENY", "SAMEORIGIN"]
FunctionRuntimeType = Literal["cloudfront-js-1.0", "cloudfront-js-2.0"]
FunctionStageType = Literal["DEVELOPMENT", "LIVE"]
GeoRestrictionTypeType = Literal["blacklist", "none", "whitelist"]
HttpVersionType = Literal["http1.1", "http2", "http2and3", "http3"]
ICPRecordalStatusType = Literal["APPROVED", "PENDING", "SUSPENDED"]
ImportSourceTypeType = Literal["S3"]
InvalidationCompletedWaiterName = Literal["invalidation_completed"]
ItemSelectionType = Literal["all", "none", "whitelist"]
ListCloudFrontOriginAccessIdentitiesPaginatorName = Literal[
    "list_cloud_front_origin_access_identities"
]
ListDistributionsPaginatorName = Literal["list_distributions"]
ListInvalidationsPaginatorName = Literal["list_invalidations"]
ListKeyValueStoresPaginatorName = Literal["list_key_value_stores"]
ListStreamingDistributionsPaginatorName = Literal["list_streaming_distributions"]
MethodType = Literal["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
MinimumProtocolVersionType = Literal[
    "SSLv3", "TLSv1", "TLSv1.1_2016", "TLSv1.2_2018", "TLSv1.2_2019", "TLSv1.2_2021", "TLSv1_2016"
]
OriginAccessControlOriginTypesType = Literal["lambda", "mediapackagev2", "mediastore", "s3"]
OriginAccessControlSigningBehaviorsType = Literal["always", "never", "no-override"]
OriginAccessControlSigningProtocolsType = Literal["sigv4"]
OriginProtocolPolicyType = Literal["http-only", "https-only", "match-viewer"]
OriginRequestPolicyCookieBehaviorType = Literal["all", "allExcept", "none", "whitelist"]
OriginRequestPolicyHeaderBehaviorType = Literal[
    "allExcept", "allViewer", "allViewerAndWhitelistCloudFront", "none", "whitelist"
]
OriginRequestPolicyQueryStringBehaviorType = Literal["all", "allExcept", "none", "whitelist"]
OriginRequestPolicyTypeType = Literal["custom", "managed"]
PriceClassType = Literal["PriceClass_100", "PriceClass_200", "PriceClass_All"]
RealtimeMetricsSubscriptionStatusType = Literal["Disabled", "Enabled"]
ReferrerPolicyListType = Literal[
    "no-referrer",
    "no-referrer-when-downgrade",
    "origin",
    "origin-when-cross-origin",
    "same-origin",
    "strict-origin",
    "strict-origin-when-cross-origin",
    "unsafe-url",
]
ResponseHeadersPolicyAccessControlAllowMethodsValuesType = Literal[
    "ALL", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"
]
ResponseHeadersPolicyTypeType = Literal["custom", "managed"]
SSLSupportMethodType = Literal["sni-only", "static-ip", "vip"]
SslProtocolType = Literal["SSLv3", "TLSv1", "TLSv1.1", "TLSv1.2"]
StreamingDistributionDeployedWaiterName = Literal["streaming_distribution_deployed"]
ViewerProtocolPolicyType = Literal["allow-all", "https-only", "redirect-to-https"]
CloudFrontServiceName = Literal["cloudfront"]
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
    "list_cloud_front_origin_access_identities",
    "list_distributions",
    "list_invalidations",
    "list_key_value_stores",
    "list_streaming_distributions",
]
WaiterName = Literal[
    "distribution_deployed", "invalidation_completed", "streaming_distribution_deployed"
]
