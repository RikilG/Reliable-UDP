#!/usr/bin/env python

from RDTPConnection import RDTPSender

ip = "127.0.0.1" # localhost

def send(data):
    conn = RDTPSender()
    conn.connect(ip)
    conn.send(data)
    conn.close()

def main():
    data = input("Enter data you would like to send: ")
    send(data)

if __name__ == "__main__":
    main()