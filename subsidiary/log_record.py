from ipaddress import IPv4Address
from re import match
from time import struct_time, strptime


class RequestType:
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3


class LogRecord:
    REGEX = r"(\S{7,15}) - - \[(.+)] \"(.+)\" (\d+) (\d+) \"(.+)\" \"(.+)\" (\d+)"
    REQUEST_TYPE = {
        "GET": RequestType.GET,
        "POST": RequestType.POST,
        "PUT": RequestType.PUT,
        "DELETE": RequestType.DELETE
    }

    def __init__(self, log_line: str):
        result = match(self.REGEX, log_line)
        assert result is not None
        self.__client_ip = IPv4Address(result.group(1))
        self.__date = strptime(result.group(2), "%d/%b/%Y:%H:%M:%S %z")
        self.__request = result.group(3)
        self.__answer_code = int(result.group(4))
        self.__answer_size = int(result.group(5))
        self.__url = result.group(6)
        self.__user_agent = result.group(7)
        self.__request_duration = int(result.group(8))
        self.__request_type_name = self.__request.partition(' ')[0]
        self.__request_type: int = self.REQUEST_TYPE.get(self.__request_type_name, -1)

    @property
    def answer_code(self) -> int:
        return self.__answer_code

    @property
    def answer_size(self) -> int:
        return self.__answer_size

    @property
    def client_ip(self) -> IPv4Address:
        return self.__client_ip

    @property
    def date(self) -> struct_time:
        return self.__date

    @property
    def request(self) -> str:
        return self.__request

    @property
    def request_duration(self) -> int:
        return self.__request_duration

    @property
    def request_type(self) -> int:
        return self.__request_type

    @property
    def request_type_name(self) -> str:
        return self.__request_type_name

    @property
    def user_agent(self) -> str:
        return self.__user_agent

    @property
    def url(self) -> str:
        return self.__url


