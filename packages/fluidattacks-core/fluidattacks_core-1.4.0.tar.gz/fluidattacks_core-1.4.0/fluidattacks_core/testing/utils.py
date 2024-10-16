from .types import (
    AioDynamoDBResource,
    AioDynamoDBTable,
    DynamoDBResource,
    DynamoDBTable,
    IntegratesDomain,
    TableItem,
)
from aioboto3.dynamodb.table import (
    CustomTableResource,
)
from fluidattacks_core.testing.constants import (
    TABLE_DEFINITION,
)
from mypy_boto3_dynamodb.type_defs import (
    CreateTableInputServiceResourceCreateTableTypeDef as CreateTableTypeDef,
)
from types_aiobotocore_dynamodb.type_defs import (
    CreateTableInputServiceResourceCreateTableTypeDef as AioCreateTableTypeDef,
)
from typing import (
    cast,
)


def _populate_table_sync(
    table: DynamoDBTable,
    data: IntegratesDomain,
) -> None:
    for org in data.orgs:
        table.put_item(Item=cast(TableItem, org.build()))

    for group in data.groups:
        table.put_item(Item=cast(TableItem, group.build()))

    for finding in data.findings:
        table.put_item(Item=cast(TableItem, finding.build()))

    for vuln in data.vulns:
        table.put_item(Item=cast(TableItem, vuln.build()))


async def _populate_table_async(
    table: AioDynamoDBTable,
    data: IntegratesDomain,
) -> None:
    for org in data.orgs:
        await table.put_item(Item=cast(TableItem, org.build()))

    for group in data.groups:
        await table.put_item(Item=cast(TableItem, group.build()))

    for finding in data.findings:
        await table.put_item(Item=cast(TableItem, finding.build()))

    for vuln in data.vulns:
        await table.put_item(Item=cast(TableItem, vuln.build()))


async def populate_table(
    table: DynamoDBTable | AioDynamoDBTable,
    data: IntegratesDomain,
) -> None:
    # CustomTableResource is the type of aioboto3 DynamoDB table, but it
    # doesn't have type hints for put_item method.
    if isinstance(table, CustomTableResource):
        await _populate_table_async(cast(AioDynamoDBTable, table), data)
    else:
        _populate_table_sync(cast(DynamoDBTable, table), data)


def _setup_table_sync(db_resource: DynamoDBResource) -> DynamoDBTable:
    table_def = cast(CreateTableTypeDef, TABLE_DEFINITION)
    return db_resource.create_table(**table_def)


async def _setup_table_async(
    db_resource: AioDynamoDBResource,
) -> AioDynamoDBTable:
    table_def = cast(AioCreateTableTypeDef, TABLE_DEFINITION)
    return await db_resource.create_table(**table_def)


async def setup_table(
    db_resource: DynamoDBResource | AioDynamoDBResource,
) -> DynamoDBTable | AioDynamoDBTable:
    if isinstance(db_resource, DynamoDBResource):
        return _setup_table_sync(db_resource)
    return await _setup_table_async(db_resource)
