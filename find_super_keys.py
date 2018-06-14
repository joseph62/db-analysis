#! /usr/bin/env python3

import sys
from pprint import pprint
from itertools import combinations, chain, islice
from argparse import ArgumentParser
from csv import reader
from re import match

def get_arguments(argv):
    parser = ArgumentParser(description='Find all super keys in a csv file')
    parser.add_argument('-f','--file',help='CSV file to analyze',required=True)
    parser.add_argument('-n','--number',help='Number of keys to show',type=int)
    parser.add_argument('-e','--exclusion',help='List of strings to exclude from keys',nargs='+',default=[])
    parser.add_argument('-r','--regex-exclusion',help='Regular expression to exclude columns')
    parser.add_argument('-s','--max-key-size',help='Maximum key size to accept',type=int,default=None)
    return parser.parse_args(argv[1:])

def get_csv_data(file_):
    with open(file_,'r') as f:
        lines = [line.strip() for line in f]
    header, *rows = list(reader(lines))
    # make sure column headers are unique
    header = [f'{title} - {index}' for index,title in enumerate(header)]
    return (header,[dict(zip(header,row)) for row in rows])

def is_super_key(key,rows):
    values = set()
    for row in rows:
        value = tuple(row[k] for k in key)
        if value in values:
            return False
        values.add(value)
    return True

def filter_regex(header,regex):
    if regex:
        header = list(key for key in header if match(regex,key) is None)
    return header

def filter_exclusions(header,exclusions):
    if exclusions:
        header = [key for key in header if key not in args.exclusion]
    return header

def main(argv):
    args = get_arguments(argv)
    header,rows = get_csv_data(args.file)

    header = filter_regex(filter_exclusions(header,args.exclusion),args.regex_exclusion)

    max_length = args.max_key_size if args.max_key_size and args.max_key_size < len(header) else len(header) 
    all_combinations = chain.from_iterable(combinations(header,r=i) for i in range(1,max_length+1)) 
    super_keys = (key for key in all_combinations if is_super_key(key,rows))
    for key in islice(super_keys,None,args.number):
        print(key)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
