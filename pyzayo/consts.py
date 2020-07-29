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
