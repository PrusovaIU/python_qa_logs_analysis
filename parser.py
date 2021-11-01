from contextlib import suppress
from os import mkdir, getcwd
from os.path import normpath, split
from subsidiary import parse
from subsidiary.form_report import report
from typing import Tuple, Dict
import argparse


CURRENT_DIR = getcwd()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", default=CURRENT_DIR, help="Absolute path to directory with logs")
    parser.add_argument("-f", "--file", default='', help="Absolute path to file with logs")

    args = parser.parse_args()
    report_path = f"{CURRENT_DIR}/reports"
    with suppress(FileExistsError):
        mkdir(report_path)
    if args.file != '':
        logs: Tuple[parse.LogRecord] = parse.file_parse(args.file)
        file_name = split(args.file)[1]
        file_name = file_name.split('.')[0]
        report(logs, normpath(f"{report_path}/{file_name}"), file_name)
    else:
        logs: Dict[str, Tuple[parse.LogRecord]] = parse.dir_parse(args.dir)
        print(f"Files have been found: {str(' ').join(logs.keys())}\n")
        for file_name, logs_list in logs.items():
            report(logs_list, normpath(f"{report_path}/{file_name}"), file_name)
