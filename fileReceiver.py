#!/usr/bin/env python

import argparse
import os
from RDTPConnection import RDTPReceiver

output = None

def this_func(data):
    global output
    with open(output, "wb") as f:
        f.write(data)

def main():
    conn = RDTPReceiver()
    try:
        conn.listen(on_data_run=this_func, exit_after_run=True)
    except KeyboardInterrupt:
        print("\rUser exit signal encountered!")
    conn.close()

def parseArgs():
    parser = argparse.ArgumentParser(description="Receive files sent with RDTP protocol")
    parser.add_argument("-o", "--output", help="path of file to be written")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    if args.output is None:
        print("Output file location required")
        exit()
    output = args.output
    main()