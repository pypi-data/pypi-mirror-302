"""
Main interface for simspaceweaver service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_simspaceweaver import (
        Client,
        SimSpaceWeaverClient,
    )

    session = Session()
    client: SimSpaceWeaverClient = session.client("simspaceweaver")
    ```
"""

from .client import SimSpaceWeaverClient

Client = SimSpaceWeaverClient

__all__ = ("Client", "SimSpaceWeaverClient")
