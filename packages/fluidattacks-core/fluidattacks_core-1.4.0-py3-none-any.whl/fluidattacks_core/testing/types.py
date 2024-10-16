# pylint: disable=invalid-name
from .fakers import (
    FindingFaker,
    GroupFaker,
    OrganizationFaker,
    VulnerabilityFaker,
)
from mypy_boto3_dynamodb.service_resource import (
    DynamoDBServiceResource,
    Table,
)
from mypy_boto3_dynamodb.type_defs import (
    TableAttributeValueTypeDef,
)
from types_aiobotocore_dynamodb.service_resource import (
    DynamoDBServiceResource as AioDynamoDBServiceResource,
    Table as AioTable,
)
from typing import (
    AsyncIterator,
    Callable,
    Iterator,
    Mapping,
    NamedTuple,
    TypeAlias,
    TypeVar,
)

T = TypeVar("T")

DynamoDBTable: TypeAlias = Table
DynamoDBResource: TypeAlias = DynamoDBServiceResource

AioDynamoDBTable: TypeAlias = AioTable
AioDynamoDBResource: TypeAlias = AioDynamoDBServiceResource

TableItem: TypeAlias = Mapping[str, TableAttributeValueTypeDef]

SetupFixture: TypeAlias = None
FunctionFixture: TypeAlias = Callable[..., T]
GeneratorFixture: TypeAlias = Iterator[T]
AsyncGeneratorFixture: TypeAlias = AsyncIterator[T]


class IntegratesDomain(NamedTuple):
    orgs: tuple[OrganizationFaker, ...]
    groups: tuple[GroupFaker, ...]
    findings: tuple[FindingFaker, ...]
    vulns: tuple[VulnerabilityFaker, ...]
