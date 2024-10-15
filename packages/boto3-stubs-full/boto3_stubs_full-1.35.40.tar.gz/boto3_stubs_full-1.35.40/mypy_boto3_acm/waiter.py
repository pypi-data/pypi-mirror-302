"""
Type annotations for acm service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_acm.client import ACMClient
    from mypy_boto3_acm.waiter import (
        CertificateValidatedWaiter,
    )

    session = Session()
    client: ACMClient = session.client("acm")

    certificate_validated_waiter: CertificateValidatedWaiter = client.get_waiter("certificate_validated")
    ```
"""

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeCertificateRequestCertificateValidatedWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("CertificateValidatedWaiter",)


class CertificateValidatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Waiter.CertificateValidated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/waiters/#certificatevalidatedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeCertificateRequestCertificateValidatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Waiter.CertificateValidated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/waiters/#certificatevalidatedwaiter)
        """
