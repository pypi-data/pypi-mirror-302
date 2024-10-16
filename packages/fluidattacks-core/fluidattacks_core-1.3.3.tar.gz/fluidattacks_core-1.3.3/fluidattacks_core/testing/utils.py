from .types import (
    AioDynamoDBTable,
    IntegratesDomain,
)


async def async_populate_table(
    table: AioDynamoDBTable,
    data: IntegratesDomain,
) -> None:
    for org in data.orgs:
        await table.put_item(Item=org.build())

    for group in data.groups:
        await table.put_item(Item=group.build())

    for finding in data.findings:
        await table.put_item(Item=finding.build())

    for vuln in data.vulns:
        await table.put_item(Item=vuln.build())
