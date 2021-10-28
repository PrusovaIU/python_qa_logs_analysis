from .log_record import LogRecord
from os import listdir
from os.path import normpath
from progress.bar import IncrementalBar
from re import match
from typing import List, Tuple, Dict


def dir_parse(dir_path: str) -> Dict[str, Tuple[LogRecord]]:
    files = [file for file in listdir(dir_path) if match(r".+\.log", file) is not None]
    logs: Dict[str, Tuple[LogRecord]] = dict()
    for file in files:
        file_path = normpath(f"{dir_path}/{file}")
        new_logs: Tuple[LogRecord] = file_parse(file_path)
        logs[file.split('.')[0]] = new_logs
    return logs


def file_parse(file_path: str) -> Tuple[LogRecord]:
    logs: List[LogRecord] = list()
    with open(file_path, 'r') as file:
        lines = file.readlines()
    bar = IncrementalBar(file_path, max=len(lines))
    for line in lines:
        try:
            logs.append(LogRecord(line))
        except (IndexError, ValueError, AssertionError) as err:
            print(f"File {file_path}\n\tLine: {line}Unexpected format\nError: {err}")
        bar.next()
    bar.finish()
    return tuple(logs)
