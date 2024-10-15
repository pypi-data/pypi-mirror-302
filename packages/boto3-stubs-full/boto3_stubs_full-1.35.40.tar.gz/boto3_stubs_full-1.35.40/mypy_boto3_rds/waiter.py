"""
Type annotations for rds service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_rds.client import RDSClient
    from mypy_boto3_rds.waiter import (
        DBClusterAvailableWaiter,
        DBClusterDeletedWaiter,
        DBClusterSnapshotAvailableWaiter,
        DBClusterSnapshotDeletedWaiter,
        DBInstanceAvailableWaiter,
        DBInstanceDeletedWaiter,
        DBSnapshotAvailableWaiter,
        DBSnapshotCompletedWaiter,
        DBSnapshotDeletedWaiter,
        TenantDatabaseAvailableWaiter,
        TenantDatabaseDeletedWaiter,
    )

    session = Session()
    client: RDSClient = session.client("rds")

    db_cluster_available_waiter: DBClusterAvailableWaiter = client.get_waiter("db_cluster_available")
    db_cluster_deleted_waiter: DBClusterDeletedWaiter = client.get_waiter("db_cluster_deleted")
    db_cluster_snapshot_available_waiter: DBClusterSnapshotAvailableWaiter = client.get_waiter("db_cluster_snapshot_available")
    db_cluster_snapshot_deleted_waiter: DBClusterSnapshotDeletedWaiter = client.get_waiter("db_cluster_snapshot_deleted")
    db_instance_available_waiter: DBInstanceAvailableWaiter = client.get_waiter("db_instance_available")
    db_instance_deleted_waiter: DBInstanceDeletedWaiter = client.get_waiter("db_instance_deleted")
    db_snapshot_available_waiter: DBSnapshotAvailableWaiter = client.get_waiter("db_snapshot_available")
    db_snapshot_completed_waiter: DBSnapshotCompletedWaiter = client.get_waiter("db_snapshot_completed")
    db_snapshot_deleted_waiter: DBSnapshotDeletedWaiter = client.get_waiter("db_snapshot_deleted")
    tenant_database_available_waiter: TenantDatabaseAvailableWaiter = client.get_waiter("tenant_database_available")
    tenant_database_deleted_waiter: TenantDatabaseDeletedWaiter = client.get_waiter("tenant_database_deleted")
    ```
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeDBClustersMessageDBClusterAvailableWaitTypeDef,
    DescribeDBClustersMessageDBClusterDeletedWaitTypeDef,
    DescribeDBClusterSnapshotsMessageDBClusterSnapshotAvailableWaitTypeDef,
    DescribeDBClusterSnapshotsMessageDBClusterSnapshotDeletedWaitTypeDef,
    DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef,
    DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef,
    DescribeDBSnapshotsMessageDBSnapshotAvailableWaitTypeDef,
    DescribeDBSnapshotsMessageDBSnapshotCompletedWaitTypeDef,
    DescribeDBSnapshotsMessageDBSnapshotDeletedWaitTypeDef,
    DescribeTenantDatabasesMessageTenantDatabaseAvailableWaitTypeDef,
    DescribeTenantDatabasesMessageTenantDatabaseDeletedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DBClusterAvailableWaiter",
    "DBClusterDeletedWaiter",
    "DBClusterSnapshotAvailableWaiter",
    "DBClusterSnapshotDeletedWaiter",
    "DBInstanceAvailableWaiter",
    "DBInstanceDeletedWaiter",
    "DBSnapshotAvailableWaiter",
    "DBSnapshotCompletedWaiter",
    "DBSnapshotDeletedWaiter",
    "TenantDatabaseAvailableWaiter",
    "TenantDatabaseDeletedWaiter",
)


class DBClusterAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbclusteravailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBClustersMessageDBClusterAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbclusteravailablewaiter)
        """


class DBClusterDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbclusterdeletedwaiter)
    """

    def wait(self, **kwargs: Unpack[DescribeDBClustersMessageDBClusterDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbclusterdeletedwaiter)
        """


class DBClusterSnapshotAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbclustersnapshotavailablewaiter)
    """

    def wait(
        self,
        **kwargs: Unpack[DescribeDBClusterSnapshotsMessageDBClusterSnapshotAvailableWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbclustersnapshotavailablewaiter)
        """


class DBClusterSnapshotDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbclustersnapshotdeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBClusterSnapshotsMessageDBClusterSnapshotDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbclustersnapshotdeletedwaiter)
        """


class DBInstanceAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBInstanceAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbinstanceavailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBInstanceAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbinstanceavailablewaiter)
        """


class DBInstanceDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBInstanceDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbinstancedeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBInstanceDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbinstancedeletedwaiter)
        """


class DBSnapshotAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbsnapshotavailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBSnapshotsMessageDBSnapshotAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbsnapshotavailablewaiter)
        """


class DBSnapshotCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbsnapshotcompletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBSnapshotsMessageDBSnapshotCompletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbsnapshotcompletedwaiter)
        """


class DBSnapshotDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbsnapshotdeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBSnapshotsMessageDBSnapshotDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#dbsnapshotdeletedwaiter)
        """


class TenantDatabaseAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.TenantDatabaseAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#tenantdatabaseavailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeTenantDatabasesMessageTenantDatabaseAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.TenantDatabaseAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#tenantdatabaseavailablewaiter)
        """


class TenantDatabaseDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.TenantDatabaseDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#tenantdatabasedeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeTenantDatabasesMessageTenantDatabaseDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.TenantDatabaseDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters/#tenantdatabasedeletedwaiter)
        """
