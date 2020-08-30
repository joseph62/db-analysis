#! /usr/bin/env python3
from argparse import ArgumentParser
from collections import defaultdict, Counter
from pprint import pprint
import csv
import sys


def get_arguments(args):
    parser = ArgumentParser(description="Find the differing columns in csv rows")
    parser.add_argument("-f", "--file", help="csv file path", required=True)
    parser.add_argument(
        "--unique-columns",
        action="store_true",
        help="Make column names unique by combining name and index",
    )
    parser.add_argument(
        "--include-count",
        action="store_true",
        help="Include counts of the column values",
    )
    parser.add_argument(
        "--format-csv", action="store_true", help="Format output in csv"
    )
    return parser.parse_args(args)


def get_csv_rows(path, unique_columns=True):
    """
    Read a csv from path and return rows.
    """
    with open(path) as f:
        header, *rows = csv.reader(f)
    if unique_columns:
        header = [f"{title} - {index}" for index, title in enumerate(header)]
    return [dict(zip(header, row)) for row in rows]


def get_csv_columns(rows):
    columns = defaultdict(list)
    for row in rows:
        for key, value in row.items():
            columns[key].append(value)
    return columns


def get_diff_columns(columns):
    def all_same(iterable):
        return len(set(iterable)) == 1

    return {key: values for key, values in columns.items() if not all_same(values)}


def add_counts_columns(columns):
    return {key: dict(Counter(values)) for key, values in columns.items()}


def convert_columns_to_rows(columns):
    header = list(columns.keys())
    raw_columns = [columns[key] for key in header]
    rows = [list(row) for row in zip(*raw_columns)]
    return [header, *rows]


def main(args):
    rows = get_csv_rows(args.file, args.unique_columns)
    columns = get_csv_columns(rows)
    diffs = get_diff_columns(columns)

    if args.format_csv:
        diff_rows = convert_columns_to_rows(diffs)
        print("\n".join(",".join(row) for row in diff_rows))
    elif args.include_count:
        diffs = add_counts_columns(diffs)
        pprint(diffs)
    else:
        pprint(diffs)

    return 0


if __name__ == "__main__":
    sys.exit(main(get_arguments(sys.argv[1:])))
