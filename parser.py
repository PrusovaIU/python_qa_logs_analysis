from os.path import dirname
from subsidiary import parse
from typing import Tuple
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", default=dirname(__file__), help="Absolute path to directory with logs")
    parser.add_argument("-f", "--file", default='', help="Absolute path to file with logs")

    args = parser.parse_args()
    logs: Tuple[parse.LogRecord] = tuple()
    if args.file != '':
        logs = parse.file_parse(args.file)
    else:
        logs, files = parse.dir_parse(args.dir)
        print(f"Files have been found: {str(' ').join(files)}")
    print(1)
