from enum import Enum


class Tickets_results(Enum):

    NO_ACTIVE_TICKETS = "no_active_tickets"
    NOT_OWNER = "not_owner"
    INVALID_STATUS = "invalid_status"
    ERROR = "error"
    NO_AVAILABLE = "no_support_available"
    NOT_SUPPORT_FOUND = "support_not_found"
    SAME_OWNER = "same_owner"
    NOT_FOUND_NO_AVAILABLE = "no_support_available"

    SUCCESS = "success"
    NOT_FOUND = "not_found"

    INVALID_OPTION = "option_invalid"
