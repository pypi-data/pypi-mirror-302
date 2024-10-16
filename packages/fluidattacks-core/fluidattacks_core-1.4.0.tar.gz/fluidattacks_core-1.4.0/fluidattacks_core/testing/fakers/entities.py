import cvss as _cvss
from datetime import (
    datetime,
)
from fluidattacks_core.testing.constants import (
    CVSS3_VALUES,
    CVSS4_VALUES,
    FIXED_DATE,
    ORG_ID,
)
from fluidattacks_core.testing.fakers.types import (
    SeverityLevelType,
)
from fluidattacks_core.testing.fakers.utils import (
    get_cvssf_score,
)
from fluidattacks_core.types.dynamo.items import (
    SeverityScore,
)
from typing import (
    Any,
)


def fake_severity_score(level: SeverityLevelType) -> SeverityScore:
    cvss3_vector = _cvss.CVSS3(CVSS3_VALUES[level])
    cvss4_vector = _cvss.CVSS4(CVSS4_VALUES[level])

    return {
        "cvssf": get_cvssf_score(cvss3_vector.temporal_score),
        "base_score": cvss3_vector.base_score,
        "temporal_score": cvss3_vector.temporal_score,
        "cvss_v3": cvss3_vector.clean_vector(),
        "threat_score": cvss3_vector.base_score,
        "cvssf_v4": get_cvssf_score(cvss4_vector.base_score),
        "cvss_v4": cvss4_vector.clean_vector(),
    }


def fake_stakeholder(
    user_email: str,
    name: str = "John Doe",
    role: str = "user",
    creation_date: str = FIXED_DATE,
) -> dict[str, Any]:
    date = datetime.fromisoformat(creation_date).isoformat()
    first_name, last_name = name.split(" ", 1)

    return {
        "role": role,
        "first_name": first_name,
        "last_name": last_name,
        "last_login_date": date,
        "registration_date": date,
        "sk": f"USER#{user_email}",
        "pk": f"USER#{user_email}",
        "sk_2": f"USER#{user_email}",
        "pk_2": "USER#all",
        "email": user_email,
        "enrolled": True,
        "legal_remember": True,
        "is_concurrent_session": False,
        "is_registered": True,
        "tours": {
            "new_group": False,
            "new_root": False,
            "new_risk_exposure": False,
            "welcome": False,
        },
        "state": {
            "modified_date": date,
            "modified_by": user_email,
            "notifications_preferences": {
                "sms": [],
                "email": [],
            },
        },
    }


def fake_stakeholder_organization_access(
    *,
    stakeholder: str,
    role: str = "user",
    grant: bool = True,
    org_id: str = ORG_ID,
    creation_date: str = FIXED_DATE,
) -> dict[str, Any]:
    date = datetime.fromisoformat(creation_date).isoformat()
    return {
        "sk": f"ORG#{org_id}",
        "pk": f"USER#{stakeholder}",
        "state": {
            "modified_by": stakeholder,
            "role": role,
            "has_access": grant,
            "modified_date": date,
        },
        "email": stakeholder,
        "organization_id": org_id,
    }
