#!/usr/bin/env python

import os
import argparse
from time import time
from RDTPConnection import RDTPSender

def send(ip, data):
    st_time = time()
    conn = RDTPSender()
    conn.connect(ip)
    conn.send(data)
    conn.close()
    duration = round(time() - st_time, 6)
    throughput = round(len(data)/(duration*1024), 3) # KB/s
    print(f"File Size: {len(data)} Bytes")
    print(f"Duration: {duration} sec")
    print(f"Throughput: {throughput} KB/s")

def main(input, ip):
    if not os.path.exists(input):
        print("Input file does not exist. please check again!")
        exit()
    with open(input, "rb") as f:
        data = f.read()
        try: 
            send(ip, data)
        except Exception as e:
            print("Error in data transfer. Please retry again later")

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