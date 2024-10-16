TABLE_NAME = "integrates_vms"
FINDING_ID = "e18c0923-a860-4ade-ba8a-33641dd80cfc"
ROOT_ID = "89d3c365-e216-42a4-9074-c724d2eb4db1"
GROUP_NAME = "unittesting"
ORG_NAME = "okada"
ORG_ID = "38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
FIXED_DATE = "2024-09-19T10:00:00.000000"
CREATED_BY = "unknown@fluidattacks.com"

CVSS3_VALUES = {
    "low": (
        "CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:L/E:P/RL:O/RC:R/CR:H/MAV:A"
        "/MAC:H/MPR:N/MUI:R/MS:U/MC:L/MA:L"
    ),
    "medium": (
        "CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N/E:P/RL:O/RC:U/IR:H/MAV:A"
        "/MAC:L/MPR:L/MUI:N/MS:U/MI:L"
    ),
    "high": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L/MAV:N/MAC:L/MUI:N",
    "critical": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:U/RL:O/RC:C",
}

CVSS4_VALUES = {
    "low": (
        "CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:P/VC:L/VI:N/VA:L/SC:N/SI:N"
        "/SA:N/E:P/CR:H/MAV:A/MAC:H/MPR:N/MUI:P/MVC:L/MVA:L"
    ),
    "medium": (
        "CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/MAV:A"
        "/MAC:L/MPR:L/MUI:N/MVI:L/MSC:N/MSI:N/MSA:N/IR:H/E:P"
    ),
    "high": (
        "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N/MAC:L"
        "/MUI:N"
    ),
    "critical": (
        "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:U"
    ),
}

TABLE_DEFINITION = {
    "TableName": TABLE_NAME,
    "KeySchema": [
        {"AttributeName": "pk", "KeyType": "HASH"},
        {"AttributeName": "sk", "KeyType": "RANGE"},
    ],
    "AttributeDefinitions": [
        {"AttributeName": "sk", "AttributeType": "S"},
        {"AttributeName": "pk", "AttributeType": "S"},
        {"AttributeName": "pk_2", "AttributeType": "S"},
        {"AttributeName": "sk_2", "AttributeType": "S"},
        {"AttributeName": "pk_5", "AttributeType": "S"},
        {"AttributeName": "sk_5", "AttributeType": "S"},
        {"AttributeName": "pk_6", "AttributeType": "S"},
        {"AttributeName": "sk_6", "AttributeType": "S"},
    ],
    "BillingMode": "PAY_PER_REQUEST",
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "inverted_index",
            "KeySchema": [
                {"AttributeName": "sk", "KeyType": "HASH"},
                {"AttributeName": "pk", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        },
        {
            "IndexName": "gsi_2",
            "KeySchema": [
                {"AttributeName": "pk_2", "KeyType": "HASH"},
                {"AttributeName": "sk_2", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        },
        {
            "IndexName": "gsi_5",
            "KeySchema": [
                {"AttributeName": "pk_5", "KeyType": "HASH"},
                {"AttributeName": "sk_5", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        },
        {
            "IndexName": "gsi_6",
            "KeySchema": [
                {"AttributeName": "pk_6", "KeyType": "HASH"},
                {"AttributeName": "sk_6", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        },
    ],
    "StreamSpecification": {
        "StreamEnabled": True,
        "StreamViewType": "NEW_AND_OLD_IMAGES",
    },
}
