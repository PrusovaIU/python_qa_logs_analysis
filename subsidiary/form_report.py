from .log_record import LogRecord, RequestType
from typing import Tuple, List


LOGS_TYPE = Tuple[LogRecord]


def count_record_by_request_type(logs: LOGS_TYPE, required_type: int) -> int:
    suitable_logs: List[LogRecord] = [log for log in logs if log.request_type == required_type]
    return len(suitable_logs)


def form(logs: LOGS_TYPE) -> str:
    all_logs_amount = len(logs)
    get_logs_amount = count_record_by_request_type(logs, RequestType.GET)
    post_logs_amount = count_record_by_request_type(logs, RequestType.POST)
    put_logs_amount = count_record_by_request_type(logs, RequestType.PUT)
    delete_logs_amount = count_record_by_request_type(logs, RequestType.DELETE)


