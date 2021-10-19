from .log_record import LogRecord, RequestType
from collections import ItemsView
from ipaddress import IPv4Address
from time import strftime
from typing import Tuple, List, Dict


LOGS_TYPE = Tuple[LogRecord]


def count_record_by_request_type(logs: LOGS_TYPE, required_type: int) -> int:
    suitable_logs: List[LogRecord] = [log for log in logs if log.request_type == required_type]
    return len(suitable_logs)


def summarize_record_by_client(logs: LOGS_TYPE) -> Dict[IPv4Address, int]:
    amounts: Dict[IPv4Address, int] = dict()
    for log in logs:
        client = log.client_ip
        client_amount = amounts.get(client, 0)
        amounts[client] = client_amount + 1
    return amounts


def get_top_clients(logs: LOGS_TYPE) -> str:
    amount_logs_by_client: Dict[IPv4Address, int] = summarize_record_by_client(logs)
    sorted_logs_by_client: ItemsView[IPv4Address, int] = sorted(amount_logs_by_client.items(),
                                                                key=lambda _item: _item[1], reverse=True)
    top_clients_list: List[str] = list()
    for item in sorted_logs_by_client[:3]:
        top_clients_list.append(f"\t{str(item[0])}: {item[1]} requests")
    return str('\n').join(top_clients_list)


def get_top_requests(logs: LOGS_TYPE) -> str:
    sorted_logs_by_duration = sorted(logs, key=lambda log: log.duration, reverse=True)
    top_request_list: List[str] = list()
    for log in sorted_logs_by_duration[:3]:
        top_request_list.append(f"\tTYPE: {log.request_type_name} URL: {log.url} IP: {log.client_ip} "
                                f"TIME: {strftime('%d-%m-%Y %H:%M:%S')} DURATION: {log.request_duration}")
    return str('\n').join(top_request_list)


def form(logs: LOGS_TYPE) -> str:
    all_logs_amount = len(logs)
    get_logs_amount = count_record_by_request_type(logs, RequestType.GET)
    post_logs_amount = count_record_by_request_type(logs, RequestType.POST)
    put_logs_amount = count_record_by_request_type(logs, RequestType.PUT)
    delete_logs_amount = count_record_by_request_type(logs, RequestType.DELETE)

    top_clients = get_top_clients(logs)
    top_requests = get_top_requests(logs)

    report_str = f"Logs amount: {all_logs_amount}\n" \
                 f"Logs amount by requests type:\n" \
                 f"\tGET: {get_logs_amount}\n" \
                 f"\tPOST: {post_logs_amount}\n" \
                 f"\tPUT: {put_logs_amount}\n" \
                 f"\tDELETE: {delete_logs_amount}\n" \
                 f"\n" \
                 f"TOP3 clients:\n" \
                 f"{top_clients}\n" \
                 f"\n" \
                 f"TOP3 requests:\n" \
                 f"{top_requests}"

    report_dict = {
        "logs_amount": {
            "all": all_logs_amount,
            "GET": get_logs_amount,
            "POST": post_logs_amount,
            "PUT": put_logs_amount,
            "DELETE": delete_logs_amount
        },
        "top3_client":
    }





