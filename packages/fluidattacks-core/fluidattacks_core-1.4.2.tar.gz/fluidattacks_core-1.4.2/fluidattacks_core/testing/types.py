# pylint: disable=invalid-name
from aioboto3.dynamodb.table import (
    CustomTableResource,
)
from boto3.dynamodb.table import (
    TableResource,
)
from fluidattacks_core.testing.fakers.builders import (
    EnvironmentUrlFaker,
    FindingFaker,
    GitRootFaker,
    GroupFaker,
    OrganizationAccessFaker,
    OrganizationFaker,
    StakeholderFaker,
    ToeInputFaker,
    VulnerabilityFaker,
)
from mypy_boto3_dynamodb.service_resource import (
    DynamoDBServiceResource,
    Table,
)
from mypy_boto3_dynamodb.type_defs import (
    CreateTableInputServiceResourceCreateTableTypeDef as CreateTable,
    TableAttributeValueTypeDef as TableAttribute,
)
from types_aiobotocore_dynamodb.service_resource import (
    DynamoDBServiceResource as AioDynamoDBServiceResource,
    Table as AioTable,
)
from types_aiobotocore_dynamodb.type_defs import (
    CreateTableInputServiceResourceCreateTableTypeDef as AioCreateTable,
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

Boto3Table: TypeAlias = TableResource
Aioboto3Table: TypeAlias = CustomTableResource

DynamoDBTable: TypeAlias = Table
DynamoDBResource: TypeAlias = DynamoDBServiceResource
CreateTableParams: TypeAlias = CreateTable

AioDynamoDBTable: TypeAlias = AioTable
AioDynamoDBResource: TypeAlias = AioDynamoDBServiceResource
AioCreateTableParams: TypeAlias = AioCreateTable

TableItem: TypeAlias = Mapping[str, TableAttribute]

SetupFixture: TypeAlias = None
FunctionFixture: TypeAlias = Callable[..., T]
GeneratorFixture: TypeAlias = Iterator[T]
AsyncGeneratorFixture: TypeAlias = AsyncIterator[T]


class IntegratesDomain(NamedTuple):
    orgs: tuple[OrganizationFaker, ...] = tuple()
    groups: tuple[GroupFaker, ...] = tuple()
    git_roots: tuple[GitRootFaker, ...] = tuple()
    environment_urls: tuple[EnvironmentUrlFaker, ...] = tuple()
    toe_inputs: tuple[ToeInputFaker, ...] = tuple()
    findings: tuple[FindingFaker, ...] = tuple()
    vulns: tuple[VulnerabilityFaker, ...] = tuple()
    stakeholders: tuple[StakeholderFaker, ...] = tuple()
    organization_access: tuple[OrganizationAccessFaker, ...] = tuple()
