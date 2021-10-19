from os.path import dirname, normpath
from subsidiary import parse
from subsidiary.form_report import form as form_report
from typing import Tuple
import argparse


CURRENT_DIR = dirname(__file__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", default=CURRENT_DIR, help="Absolute path to directory with logs")
    parser.add_argument("-f", "--file", default='', help="Absolute path to file with logs")

    args = parser.parse_args()
    logs: Tuple[parse.LogRecord] = tuple()
    if args.file != '':
        logs = parse.file_parse(args.file)
    else:
        logs, files = parse.dir_parse(args.dir)
        print(f"Files have been found: {str(' ').join(files)}\n")

    report_str, report_json = form_report(logs)
    print(report_str)
    with open(normpath(f"{CURRENT_DIR}/report.json"), 'w') as file:
        file.write(report_json)
