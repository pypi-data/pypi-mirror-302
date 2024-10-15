"""
Type annotations for cloudsearch service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudsearch.client import CloudSearchClient

    session = Session()
    client: CloudSearchClient = session.client("cloudsearch")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    BuildSuggestersRequestRequestTypeDef,
    BuildSuggestersResponseTypeDef,
    CreateDomainRequestRequestTypeDef,
    CreateDomainResponseTypeDef,
    DefineAnalysisSchemeRequestRequestTypeDef,
    DefineAnalysisSchemeResponseTypeDef,
    DefineExpressionRequestRequestTypeDef,
    DefineExpressionResponseTypeDef,
    DefineIndexFieldRequestRequestTypeDef,
    DefineIndexFieldResponseTypeDef,
    DefineSuggesterRequestRequestTypeDef,
    DefineSuggesterResponseTypeDef,
    DeleteAnalysisSchemeRequestRequestTypeDef,
    DeleteAnalysisSchemeResponseTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DeleteDomainResponseTypeDef,
    DeleteExpressionRequestRequestTypeDef,
    DeleteExpressionResponseTypeDef,
    DeleteIndexFieldRequestRequestTypeDef,
    DeleteIndexFieldResponseTypeDef,
    DeleteSuggesterRequestRequestTypeDef,
    DeleteSuggesterResponseTypeDef,
    DescribeAnalysisSchemesRequestRequestTypeDef,
    DescribeAnalysisSchemesResponseTypeDef,
    DescribeAvailabilityOptionsRequestRequestTypeDef,
    DescribeAvailabilityOptionsResponseTypeDef,
    DescribeDomainEndpointOptionsRequestRequestTypeDef,
    DescribeDomainEndpointOptionsResponseTypeDef,
    DescribeDomainsRequestRequestTypeDef,
    DescribeDomainsResponseTypeDef,
    DescribeExpressionsRequestRequestTypeDef,
    DescribeExpressionsResponseTypeDef,
    DescribeIndexFieldsRequestRequestTypeDef,
    DescribeIndexFieldsResponseTypeDef,
    DescribeScalingParametersRequestRequestTypeDef,
    DescribeScalingParametersResponseTypeDef,
    DescribeServiceAccessPoliciesRequestRequestTypeDef,
    DescribeServiceAccessPoliciesResponseTypeDef,
    DescribeSuggestersRequestRequestTypeDef,
    DescribeSuggestersResponseTypeDef,
    IndexDocumentsRequestRequestTypeDef,
    IndexDocumentsResponseTypeDef,
    ListDomainNamesResponseTypeDef,
    UpdateAvailabilityOptionsRequestRequestTypeDef,
    UpdateAvailabilityOptionsResponseTypeDef,
    UpdateDomainEndpointOptionsRequestRequestTypeDef,
    UpdateDomainEndpointOptionsResponseTypeDef,
    UpdateScalingParametersRequestRequestTypeDef,
    UpdateScalingParametersResponseTypeDef,
    UpdateServiceAccessPoliciesRequestRequestTypeDef,
    UpdateServiceAccessPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("CloudSearchClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BaseException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DisabledOperationException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CloudSearchClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudSearchClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#exceptions)
        """

    def build_suggesters(
        self, **kwargs: Unpack[BuildSuggestersRequestRequestTypeDef]
    ) -> BuildSuggestersResponseTypeDef:
        """
        Indexes the search suggestions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.build_suggesters)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#build_suggesters)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#close)
        """

    def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestRequestTypeDef]
    ) -> CreateDomainResponseTypeDef:
        """
        Creates a new search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.create_domain)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#create_domain)
        """

    def define_analysis_scheme(
        self, **kwargs: Unpack[DefineAnalysisSchemeRequestRequestTypeDef]
    ) -> DefineAnalysisSchemeResponseTypeDef:
        """
        Configures an analysis scheme that can be applied to a `text` or `text-array`
        field to define language-specific text processing
        options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.define_analysis_scheme)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#define_analysis_scheme)
        """

    def define_expression(
        self, **kwargs: Unpack[DefineExpressionRequestRequestTypeDef]
    ) -> DefineExpressionResponseTypeDef:
        """
        Configures an `Expression` for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.define_expression)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#define_expression)
        """

    def define_index_field(
        self, **kwargs: Unpack[DefineIndexFieldRequestRequestTypeDef]
    ) -> DefineIndexFieldResponseTypeDef:
        """
        Configures an `IndexField` for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.define_index_field)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#define_index_field)
        """

    def define_suggester(
        self, **kwargs: Unpack[DefineSuggesterRequestRequestTypeDef]
    ) -> DefineSuggesterResponseTypeDef:
        """
        Configures a suggester for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.define_suggester)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#define_suggester)
        """

    def delete_analysis_scheme(
        self, **kwargs: Unpack[DeleteAnalysisSchemeRequestRequestTypeDef]
    ) -> DeleteAnalysisSchemeResponseTypeDef:
        """
        Deletes an analysis scheme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.delete_analysis_scheme)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#delete_analysis_scheme)
        """

    def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]
    ) -> DeleteDomainResponseTypeDef:
        """
        Permanently deletes a search domain and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.delete_domain)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#delete_domain)
        """

    def delete_expression(
        self, **kwargs: Unpack[DeleteExpressionRequestRequestTypeDef]
    ) -> DeleteExpressionResponseTypeDef:
        """
        Removes an `Expression` from the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.delete_expression)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#delete_expression)
        """

    def delete_index_field(
        self, **kwargs: Unpack[DeleteIndexFieldRequestRequestTypeDef]
    ) -> DeleteIndexFieldResponseTypeDef:
        """
        Removes an `IndexField` from the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.delete_index_field)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#delete_index_field)
        """

    def delete_suggester(
        self, **kwargs: Unpack[DeleteSuggesterRequestRequestTypeDef]
    ) -> DeleteSuggesterResponseTypeDef:
        """
        Deletes a suggester.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.delete_suggester)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#delete_suggester)
        """

    def describe_analysis_schemes(
        self, **kwargs: Unpack[DescribeAnalysisSchemesRequestRequestTypeDef]
    ) -> DescribeAnalysisSchemesResponseTypeDef:
        """
        Gets the analysis schemes configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_analysis_schemes)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#describe_analysis_schemes)
        """

    def describe_availability_options(
        self, **kwargs: Unpack[DescribeAvailabilityOptionsRequestRequestTypeDef]
    ) -> DescribeAvailabilityOptionsResponseTypeDef:
        """
        Gets the availability options configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_availability_options)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#describe_availability_options)
        """

    def describe_domain_endpoint_options(
        self, **kwargs: Unpack[DescribeDomainEndpointOptionsRequestRequestTypeDef]
    ) -> DescribeDomainEndpointOptionsResponseTypeDef:
        """
        Returns the domain's endpoint options, specifically whether all requests to the
        domain must arrive over
        HTTPS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_domain_endpoint_options)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#describe_domain_endpoint_options)
        """

    def describe_domains(
        self, **kwargs: Unpack[DescribeDomainsRequestRequestTypeDef]
    ) -> DescribeDomainsResponseTypeDef:
        """
        Gets information about the search domains owned by this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_domains)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#describe_domains)
        """

    def describe_expressions(
        self, **kwargs: Unpack[DescribeExpressionsRequestRequestTypeDef]
    ) -> DescribeExpressionsResponseTypeDef:
        """
        Gets the expressions configured for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_expressions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#describe_expressions)
        """

    def describe_index_fields(
        self, **kwargs: Unpack[DescribeIndexFieldsRequestRequestTypeDef]
    ) -> DescribeIndexFieldsResponseTypeDef:
        """
        Gets information about the index fields configured for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_index_fields)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#describe_index_fields)
        """

    def describe_scaling_parameters(
        self, **kwargs: Unpack[DescribeScalingParametersRequestRequestTypeDef]
    ) -> DescribeScalingParametersResponseTypeDef:
        """
        Gets the scaling parameters configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_scaling_parameters)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#describe_scaling_parameters)
        """

    def describe_service_access_policies(
        self, **kwargs: Unpack[DescribeServiceAccessPoliciesRequestRequestTypeDef]
    ) -> DescribeServiceAccessPoliciesResponseTypeDef:
        """
        Gets information about the access policies that control access to the domain's
        document and search
        endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_service_access_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#describe_service_access_policies)
        """

    def describe_suggesters(
        self, **kwargs: Unpack[DescribeSuggestersRequestRequestTypeDef]
    ) -> DescribeSuggestersResponseTypeDef:
        """
        Gets the suggesters configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_suggesters)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#describe_suggesters)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#generate_presigned_url)
        """

    def index_documents(
        self, **kwargs: Unpack[IndexDocumentsRequestRequestTypeDef]
    ) -> IndexDocumentsResponseTypeDef:
        """
        Tells the search domain to start indexing its documents using the latest
        indexing
        options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.index_documents)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#index_documents)
        """

    def list_domain_names(self) -> ListDomainNamesResponseTypeDef:
        """
        Lists all search domains owned by an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.list_domain_names)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#list_domain_names)
        """

    def update_availability_options(
        self, **kwargs: Unpack[UpdateAvailabilityOptionsRequestRequestTypeDef]
    ) -> UpdateAvailabilityOptionsResponseTypeDef:
        """
        Configures the availability options for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.update_availability_options)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#update_availability_options)
        """

    def update_domain_endpoint_options(
        self, **kwargs: Unpack[UpdateDomainEndpointOptionsRequestRequestTypeDef]
    ) -> UpdateDomainEndpointOptionsResponseTypeDef:
        """
        Updates the domain's endpoint options, specifically whether all requests to the
        domain must arrive over
        HTTPS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.update_domain_endpoint_options)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#update_domain_endpoint_options)
        """

    def update_scaling_parameters(
        self, **kwargs: Unpack[UpdateScalingParametersRequestRequestTypeDef]
    ) -> UpdateScalingParametersResponseTypeDef:
        """
        Configures scaling parameters for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.update_scaling_parameters)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#update_scaling_parameters)
        """

    def update_service_access_policies(
        self, **kwargs: Unpack[UpdateServiceAccessPoliciesRequestRequestTypeDef]
    ) -> UpdateServiceAccessPoliciesResponseTypeDef:
        """
        Configures the access rules that control access to the domain's document and
        search
        endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.update_service_access_policies)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/client/#update_service_access_policies)
        """
