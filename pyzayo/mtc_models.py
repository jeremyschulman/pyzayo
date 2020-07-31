from typing import Optional
from datetime import time, date, datetime

from pydantic import BaseModel, Field

from pyzayo import consts

__all__ = ["CaseRecord", "ImpactRecord", "NotificationDetailRecord"]


class CaseRecord(BaseModel):
    """
    This model defines a maintencance case record returned via the API
    """

    case_id: str = Field(alias="caseId")
    case_num: str = Field(alias="caseNumber")
    urgency: str = Field(alias="urgency")
    impact: str = Field(alias="levelOfImpact")
    status: consts.CaseStatusOptions
    primary_date: date = Field(alias="primaryDate")
    primary_date_2: Optional[date] = Field(alias="x2ndPrimaryDate")
    primary_date_3: Optional[date] = Field(alias="x3rdPrimaryDate")
    from_time: time = Field(alias="fromTime")
    to_time: time = Field(alias="toTime")
    reason: str = Field(alias="reasonForMaintenance")
    location: str
    longitiude: Optional[float]
    latittude: Optional[float]


class ImpactRecord(BaseModel):
    """
    This model defines fields in the maintenance impact record (of interest, not all)
    """

    case_num: str = Field(alias="caseNumber")
    circuit_id: str = Field(alias="circuitId")
    impact: str = Field(alias="expectedImpact")
    clli_a: str = Field(alias="aLocationClli")
    clli_z: str = Field(alias="zLocationClli")


class NotificationDetailRecord(BaseModel):
    """
    This model defines the fields in the maintenance notification details record
    """

    name: str
    type: str = Field(alias="notificationType")
    date: datetime = Field(alias="lastModifiedDate")
    subject: str
    email_list: str = Field(alias="toEmailList")
    email_content: str = Field(alias="emailBody")
