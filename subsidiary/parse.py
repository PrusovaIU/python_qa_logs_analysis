from .log_record import LogRecord
from os import listdir
from os.path import normpath
from re import match
from typing import List, Tuple


def dir_parse(dir_path: str) -> (Tuple[LogRecord], Tuple[str]):
    files = [file for file in listdir(dir_path) if match(r".+\.log", file) is not None]
    logs: List[LogRecord] = list()
    for file in files:
        new_logs: Tuple[LogRecord] = file_parse(normpath(f"{dir_path}/{file}"))
        logs.extend(new_logs)
    return logs, files


def file_parse(file_path: str) -> Tuple[LogRecord]:
    logs: List[LogRecord] = list()
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        try:
            logs.append(LogRecord(line))
        except (IndexError, ValueError, AssertionError) as err:
            print(f"File {file_path}\n\tLine: {line}Unexpected format\nError: {err}")
    return tuple(logs)
