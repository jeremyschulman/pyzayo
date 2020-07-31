"""
This file contains _constants_ used by this package.
"""

from enum import Enum

# Environment variables

Env = {"client_id": "ZAYO_CLIENT_ID", "client_secret": "ZAYO_CLIENT_SECRET"}

# URL for authorizing client crendentials and obtaining an access token
ZAYO_URL_AUTH = "https://auth.testzayo.com/oauth/token"

# WARNING: base URL must end with "/"
# Reference: https://github.com/encode/httpx/issues/846

ZAYO_URL_SM = "https://api.zayo.com/services/service-management/v1/"

# WARNING: path routes from base_url MUST NOT begin with a "/" for the same resaons.
ZAYO_SM_ROUTE_MTC_CASES = "maintenance-cases"
ZAYO_SM_ROUTE_MTC_IMPACTS = "maintenance-impacts"
ZAYO_SM_ROUTE_MTC_NOTIFS_BY_CASE = "maintenance-cases/{case_num}/notifications"
ZAYO_SM_ROUTE_MTC_NOTIFS_BY_NAME = "maintenance-cases/notifications/{name}"
ZAYO_SM_ROUTE_SERVICES = "existing-services"


# The Zayo API has a maximum "top" count of 50 records
MAX_TOP_COUNT = 50
MAX_PAGED_RECORDS = 100


class NotificationTypes(Enum):
    """
    Used by the notification API endpoints
    """

    scheduled = "Scheduled"
    rescheduled = "Rescheduled"
    started = "Maintenance Started"
    stopped = "Maintenance Stopped"
    completed = "Maintenance Completed"
    cancelled = "Cancelled"


class OrderBy(Enum):
    """
    Used for any API supporting the `orderBy` criteria
    """

    date_later = "primaryDate desc"
    date_sooner = "primaryDate asc"


class CaseUrgencyOptions(str, Enum):
    """
    Used by the Cases `urgency` field
    """

    planned = "Planned"
    emergency = "Emergency"
    demand = "Demand"


class CaseStatusOptions(str, Enum):
    """
    Used by case record `status` field
    """

    new = "New"
    in_review = "MR Review"
    rejected = "MR Rejected"
    impact_fe_in_review = "Impact FE Review"
    impact_fe_complete = "Impact FE Complete"
    pending_schedule = "MR Pending Schedule"
    schedule_in_progress = "Scheduling in Progress"
    started = "Maint Started"
    stopped = "Maint Stopped"
    completed = "Maint Completed"
    rescheduled = "Rescheduled"
    cancelled = "Cancelled"
    closed = "Closed"
    on_hold_bcdr = "On-Hold BCDR"
    on_hold = "On-Hold"
    scheduled = "Scheduled"
    COVID = "COVID"


class CaseImpactOptions(Enum):
    """
    Used by Case record impact field.
    """

    potential_svc_aff = "Potential Service Affecting"
    svc_aff = "Service Affecting"


REQ_MOST_RECENT = {"paging": {"top": 1}, "orderBy": [OrderBy.date_later.value]}
REQ_OLDEST = {"paging": {"top": 1}, "orderBy": [OrderBy.date_sooner.value]}


class InventoryStatusOption(str, Enum):
    """ serivce inventory.status field options """

    active = "Active"
    pending = "Pending Change"
