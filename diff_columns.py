#! /usr/bin/env python3
from argparse import ArgumentParser
from collections import defaultdict, Counter
from pprint import pprint
import csv

def get_arguments():
    parser = ArgumentParser(description="Find the differing columns in csv rows")
    parser.add_argument("-f","--file",help="csv file path",required=True)
    parser.add_argument("--include-count",action="store_true",
                        help="Include counts of the column values")
    parser.add_argument("--format-csv",action="store_true",
                        help="Format output in csv")
    return parser.parse_args()

def get_csv_rows(lines):
    """
    Get a list of dicts for each row of the csv
    """
    header, *rows = list(csv.reader(lines))
    # make sure column headers are unique
    header = [f'{title} - {index}' for index,title in enumerate(header)]
    return [ dict(zip(header,row)) for row in rows ]

def get_csv_columns(rows):
    columns = defaultdict(list)
    for row in rows:
        for key,value in row.items():
            columns[key].append(value)
    return columns

def get_diff_columns(columns):
    def all_same(iterable):
        return len(set(iterable)) == 1
    return dict([(key,values) for key,values in columns.items() 
                                        if not all_same(values)])

def add_counts_columns(columns):
    return dict([(key,dict(Counter(values))) for key,values in columns.items()])

def convert_columns_to_rows(columns):
    header = list(columns.keys())
    raw_columns = [ columns[key] for key in header ]
    rows = [ list(row) for row in zip(*raw_columns) ]
    return [header, *rows]

def main(args):

    with open(args.file,'r') as f:
        lines = [line.rstrip() for line in f]

    rows = get_csv_rows(lines)
    columns = get_csv_columns(rows)
    diffs =  get_diff_columns(columns)
    if args.format_csv:
        diff_rows = convert_columns_to_rows(diffs)
        print("\n".join([",".join(row) for row in diff_rows]))
    elif args.include_count:
        diffs = add_counts_columns(diffs)
        pprint(diffs)
    else:
        pprint(diffs)

if __name__ == '__main__':
    main(get_arguments())
