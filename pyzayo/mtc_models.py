from typing import Optional
from datetime import time, date

from pydantic import BaseModel, Field


class CaseRecord(BaseModel):
    """
    This model defines a maintencance case record returned via the API
    """

    case_id: str = Field(alias="caseId")
    case_num: str = Field(alias="caseNumber")
    urgency: str = Field(alias="urgency")
    impact: str = Field(alias="levelOfImpact")
    status: str
    primary_date: date = Field(alias="primaryDate")
    primary_date_2: Optional[date] = Field(alias="x2ndPrimaryDate")
    primary_date_3: Optional[date] = Field(alias="x3rdPrimaryDate")
    from_time: time = Field(alias="fromTime")
    to_time: time = Field(alias="toTime")
    reason: str = Field(alias="reasonForMaintenance")
    location: str
    longitiude: Optional[float]
    latittude: Optional[float]
