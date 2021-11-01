from .log_record import LogRecord, RequestType
from json import dumps
from ipaddress import IPv4Address
from time import strftime
from typing import Tuple, List, Dict


LOGS_TYPE = Tuple[LogRecord]


def count_record_by_request_type(logs: LOGS_TYPE, required_type: int) -> int:
    """
    Count amount of requests of the type
    :param logs: list of logs
    :param required_type: type of request
    :return: amount of requests
    """
    suitable_logs: List[LogRecord] = [log for log in logs if log.request_type == required_type]
    return len(suitable_logs)


def summarize_record_by_client(logs: LOGS_TYPE) -> Dict[IPv4Address, int]:
    """
    Count amount of requests by every client
    :param logs: list of logs
    :return: clients IP: amount of requests
    """
    amounts: Dict[IPv4Address, int] = dict()
    for log in logs:
        client = log.client_ip
        client_amount = amounts.get(client, 0)
        amounts[client] = client_amount + 1
    return amounts


def get_top_clients(logs: LOGS_TYPE, amount: int) -> List[Tuple[IPv4Address, int]]:
    """
    Count amount of request by every client
    :param logs: list of logs
    :param amount: required amount
    :return: required amount of clients with the highest number of requests
    """
    amount_logs_by_client: Dict[IPv4Address, int] = summarize_record_by_client(logs)
    sorted_logs_by_client: List[Tuple[IPv4Address, int]] = sorted(amount_logs_by_client.items(),
                                                                  key=lambda _item: _item[1], reverse=True)
    return list(sorted_logs_by_client[:amount])


def get_top_requests(logs: LOGS_TYPE, amount: int) -> List[LogRecord]:
    """
    Sorted list of logs by duration of request
    :param logs: list of logs
    :param amount: required amount of logs
    :return: required amount of the longest requests
    """
    sorted_logs_by_duration = sorted(logs, key=lambda log: log.request_duration, reverse=True)
    return sorted_logs_by_duration[:amount]


def form(logs: LOGS_TYPE) -> (str, str):
    """
    Form report in string and json formats
    :param logs: list of logs
    :return: string format, json format
    """

    all_logs_amount = len(logs)
    get_logs_amount = count_record_by_request_type(logs, RequestType.GET)
    post_logs_amount = count_record_by_request_type(logs, RequestType.POST)
    put_logs_amount = count_record_by_request_type(logs, RequestType.PUT)
    delete_logs_amount = count_record_by_request_type(logs, RequestType.DELETE)

    top_clients: List[Tuple[IPv4Address, int]] = get_top_clients(logs, 3)
    top_clients_str = [f"\t{str(item[0])}: {item[1]} requests" for item in top_clients]
    top_clients_str = str('\n').join(top_clients_str)

    top_requests: List[LogRecord] = get_top_requests(logs, 3)
    top_requests_str = [f"\tTYPE: {log.request_type_name} URL: {log.url} IP: {log.client_ip} " 
                        f"TIME: {strftime('%d-%m-%Y %H:%M:%S', log.date)} DURATION: {log.request_duration}"
                        for log in top_requests]
    top_requests_str = str('\n').join(top_requests_str)

    report_str = f"Logs amount: {all_logs_amount}\n" \
                 f"Logs amount by requests type:\n" \
                 f"\tGET: {get_logs_amount}\n" \
                 f"\tPOST: {post_logs_amount}\n" \
                 f"\tPUT: {put_logs_amount}\n" \
                 f"\tDELETE: {delete_logs_amount}\n" \
                 f"\n" \
                 f"TOP3 clients:\n" \
                 f"{top_clients_str}\n" \
                 f"\n" \
                 f"TOP3 requests:\n" \
                 f"{top_requests_str}"

    report_dict = {
        "logs_amount": {
            "all": all_logs_amount,
            "GET": get_logs_amount,
            "POST": post_logs_amount,
            "PUT": put_logs_amount,
            "DELETE": delete_logs_amount
        },
        "top3_clients": [(str(ip), requests_amount) for ip, requests_amount in top_clients],
        "top3_requests": [{
            "TYPE": log.request_type_name,
            "URL": log.url,
            "IP": str(log.client_ip),
            "TIME": strftime('%d-%m-%Y %H:%M:%S', log.date),
            "DURATION": log.request_duration
        } for log in top_requests]
    }

    return report_str, dumps(report_dict, indent=3)


def report(logs: LOGS_TYPE, report_file_path: str, source_file_name: str):
    report_str, report_json = form(logs)
    print(f"\n\033[4m{source_file_name}\033[0m")
    print(report_str)
    with open(report_file_path, 'w') as file:
        file.write(report_json)
    print(f"File {report_file_path} has been written")
