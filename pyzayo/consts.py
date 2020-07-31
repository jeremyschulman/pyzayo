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

    most_recent = "primaryDate desc"
    least_recent = "primaryDate asc"


class CaseUrgency(Enum):
    """
    Used by the Cases `urgency` field
    """

    planned = "Planned"
    emergency = "Emergency"
    demand = "Demand"


class CaseStatus(Enum):
    """
    Used by case record `status` field
    """

    closed = "Closed"
    scheduled = "Scheduled"


class CaseImpact(Enum):
    potential_svc_aff = "Potential Service Affecting"
    svc_aff = "Service Affecting"


REQ_MOST_RECENT = {"paging": {"top": 1}, "orderBy": [OrderBy.most_recent.value]}
REQ_OLDEST = {"paging": {"top": 1}, "orderBy": [OrderBy.least_recent.value]}
