#!/usr/bin/env python

import argparse
import os
from RDTPConnection import RDTPSender

def send(ip, data):
    conn = RDTPSender()
    conn.connect(ip)
    conn.send(data)
    conn.close()

def main(input, ip):
    if not os.path.exists(input):
        print("Input file does not exist. please check again!")
        exit()
    with open(input, "rb") as f:
        data = f.read()
        send(ip, data)

def parseArgs():
    parser = argparse.ArgumentParser(description="Send files using RDTP protocol")
    parser.add_argument("-i", "--input", help="path of file to be sent")
    parser.add_argument("-ip", "--ip", help="IP address of receiver", default="127.0.0.1")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    if args.input is None:
        print("Input file required")
        exit()
    main(args.input, args.ip)