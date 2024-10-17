from .types import (
    Aioboto3Table,
    AioCreateTableParams,
    AioDynamoDBResource,
    AioDynamoDBTable,
    CreateTableParams,
    DynamoDBResource,
    DynamoDBTable,
    IntegratesDomain,
    TableItem,
)
from fluidattacks_core.testing.constants import (
    TABLE_DEFINITION,
)
from typing import (
    cast,
)


def _populate_table_sync(
    table: DynamoDBTable,
    data: IntegratesDomain,
) -> None:
    all_items = (
        data.orgs
        + data.groups
        + data.git_roots
        + data.findings
        + data.vulns
        + data.toe_inputs
        + data.environment_urls
        + data.stakeholders
        + data.organization_access
    )
    for elem in all_items:
        table.put_item(Item=cast(TableItem, elem.build()))


async def _populate_table_async(
    table: AioDynamoDBTable,
    data: IntegratesDomain,
) -> None:
    all_items = (
        data.orgs
        + data.groups
        + data.git_roots
        + data.findings
        + data.vulns
        + data.toe_inputs
        + data.environment_urls
        + data.stakeholders
        + data.organization_access
    )
    for elem in all_items:
        await table.put_item(Item=cast(TableItem, elem.build()))


async def populate_table(
    table: DynamoDBTable | AioDynamoDBTable,
    data: IntegratesDomain,
) -> None:
    """Populates a table with a given integrates domain. Example:

    ```python
    async def test_populate_table(table):
        await populate_table(
            table=table,
            data=IntegratesDomain(
                orgs=(
                    OrganizationFaker(org_id="...", org_name="..."),
                ),
                groups=(
                    GroupFaker(org_id="...", group_name="..."),
                    GroupFaker(org_id="...", group_name="..."),
                ),
                ...
            )
        )
    """
    if isinstance(table, Aioboto3Table):
        await _populate_table_async(cast(AioDynamoDBTable, table), data)
    else:
        _populate_table_sync(cast(DynamoDBTable, table), data)


def _setup_table_sync(db_resource: DynamoDBResource) -> DynamoDBTable:
    table_def = cast(CreateTableParams, TABLE_DEFINITION)
    return db_resource.create_table(**table_def)


async def _setup_table_async(
    db_resource: AioDynamoDBResource,
) -> AioDynamoDBTable:
    table_def = cast(AioCreateTableParams, TABLE_DEFINITION)
    return await db_resource.create_table(**table_def)


async def setup_table(
    db_resource: DynamoDBResource | AioDynamoDBResource,
) -> DynamoDBTable | AioDynamoDBTable:
    """Instantiate the main `integrates_vms` table using a service resource.

    Args:
        db_resource (DynamoDBResource | AioDynamoDBResource): Resource to
        instantiate the table. It could be a sync or async resource.

    Returns:
        DynamoDBTable | AioDynamoDBTable: The instantiated table.
    """
    if isinstance(db_resource, DynamoDBResource):
        return _setup_table_sync(db_resource)
    return await _setup_table_async(db_resource)
