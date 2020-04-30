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
#     data = "This is a large string which is to be sent to the receiver side \
# of the socket. This string, when completely received, including theese \
# digits: 42, indicates the proper working of the sender and receiver files \
# using RDTP protocol. This protocol aims to provide a reliable connection \
# by layering upon the existing UDP protocol using some necessary standards like \
# SRP protocol or the Stop-N-Wait protocol. Be sure to try it out!, and also\
# , a big Hello World! to you from this protocol!"
    # data = "Hello"
    send(data)

if __name__ == "__main__":
    main()