"""
Type annotations for lexv2-models service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_lexv2_models.client import LexModelsV2Client
    from mypy_boto3_lexv2_models.waiter import (
        BotAliasAvailableWaiter,
        BotAvailableWaiter,
        BotExportCompletedWaiter,
        BotImportCompletedWaiter,
        BotLocaleBuiltWaiter,
        BotLocaleCreatedWaiter,
        BotLocaleExpressTestingAvailableWaiter,
        BotVersionAvailableWaiter,
    )

    session = Session()
    client: LexModelsV2Client = session.client("lexv2-models")

    bot_alias_available_waiter: BotAliasAvailableWaiter = client.get_waiter("bot_alias_available")
    bot_available_waiter: BotAvailableWaiter = client.get_waiter("bot_available")
    bot_export_completed_waiter: BotExportCompletedWaiter = client.get_waiter("bot_export_completed")
    bot_import_completed_waiter: BotImportCompletedWaiter = client.get_waiter("bot_import_completed")
    bot_locale_built_waiter: BotLocaleBuiltWaiter = client.get_waiter("bot_locale_built")
    bot_locale_created_waiter: BotLocaleCreatedWaiter = client.get_waiter("bot_locale_created")
    bot_locale_express_testing_available_waiter: BotLocaleExpressTestingAvailableWaiter = client.get_waiter("bot_locale_express_testing_available")
    bot_version_available_waiter: BotVersionAvailableWaiter = client.get_waiter("bot_version_available")
    ```
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeBotAliasRequestBotAliasAvailableWaitTypeDef,
    DescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef,
    DescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef,
    DescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef,
    DescribeBotRequestBotAvailableWaitTypeDef,
    DescribeBotVersionRequestBotVersionAvailableWaitTypeDef,
    DescribeExportRequestBotExportCompletedWaitTypeDef,
    DescribeImportRequestBotImportCompletedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "BotAliasAvailableWaiter",
    "BotAvailableWaiter",
    "BotExportCompletedWaiter",
    "BotImportCompletedWaiter",
    "BotLocaleBuiltWaiter",
    "BotLocaleCreatedWaiter",
    "BotLocaleExpressTestingAvailableWaiter",
    "BotVersionAvailableWaiter",
)

class BotAliasAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotAliasAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botaliasavailablewaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeBotAliasRequestBotAliasAvailableWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotAliasAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botaliasavailablewaiter)
        """

class BotAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botavailablewaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeBotRequestBotAvailableWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botavailablewaiter)
        """

class BotExportCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotExportCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botexportcompletedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeExportRequestBotExportCompletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotExportCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botexportcompletedwaiter)
        """

class BotImportCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotImportCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botimportcompletedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeImportRequestBotImportCompletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotImportCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botimportcompletedwaiter)
        """

class BotLocaleBuiltWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleBuilt)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botlocalebuiltwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleBuilt.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botlocalebuiltwaiter)
        """

class BotLocaleCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botlocalecreatedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botlocalecreatedwaiter)
        """

class BotLocaleExpressTestingAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleExpressTestingAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botlocaleexpresstestingavailablewaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleExpressTestingAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botlocaleexpresstestingavailablewaiter)
        """

class BotVersionAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotVersionAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botversionavailablewaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeBotVersionRequestBotVersionAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotVersionAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/waiters/#botversionavailablewaiter)
        """
