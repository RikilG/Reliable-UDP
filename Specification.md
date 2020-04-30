# RDTP (Reliable Data Transfer Protocol)(Name subject to change) Specification

## Table of Contents

- [RDTP (Reliable Data Transfer Protocol)(Name subject to change) Specification](#rdtp-reliable-data-transfer-protocolname-subject-to-change-specification)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Specification](#specification)
    - [API Specification: (describe the api of class)](#api-specification-describe-the-api-of-class)
    - [Protocol Overview](#protocol-overview)
    - [Packet Format](#packet-format)
    - [Connection Establishment](#connection-establishment)
    - [Data Transfer](#data-transfer)
    - [Connection Termination](#connection-termination)
  - [Assumptions](#assumptions)
    - [Network Assumptions](#network-assumptions)
    - [Application Assumptions](#application-assumptions)


## Introduction

This specification describes a Reliable Data Transfer Protocol(RDTP). RDTP is a lightweight 
packet transfer protocol with the basic aim to provide in-order reliable packet delivery 
layered over traditional UDP/IP Protocol. 

This protocol is suitable for simple communication protocols like instant messaging or 
moderately sized file transfer. RDTP aims to provide a flexible and minimal design over 
existing UDP transport protocol with support for in-order and reliable delivery using a 
sliding window protocol.



## Specification

### API Specification: (describe the api of class)

### Protocol Overview

The **Sender** performs the following tasks: 
1) The sender calls the send method from the RDTPConnection library.
2) Application data is divided into chunks of fixed size.
3) A header with packet info is attached to each chunk.
4) A connection with the receiver is opened.
5) Packets are sent out using a reliable and in-order delivery protocol.
6) Terminate the connection with the receiver.

The **Receiver** performs the following tasks: 
1) Receiver uses the listen method from the RDTPConnection library
2) A socket is created and binds to port 8448
3) Receiver listens for any inbound connection requests.
4) When an inbound connection is detected, it is accepted 
5) All the received data is collected according to the delivery protocol
6) Collected data is sorted in-order, stripped of its headers and sent to the application



### Packet Format

**Header Format** (8 Bytes):
- 1st byte: Sequence number.
- 2nd byte: Acknowledgement number.
- 3rd byte: Protocol flags.
- 4th byte: Data-Index.
- 5th and 6th byte: Content-length.
- 7th and 8th byte: Checksum

```
+----------------+----------------+
|   Seq Number   |   Ack Number   |
+----------------+----------------+
|    Flag Bits   |   Data Index   |
+----------------+----------------+
|          Content-length         |
+----------------+----------------+
|             Checksum            |
+----------------+----------------+
|                                 |
|          Payload (data)         |
|                                 |
+----------------+----------------+
```

**Sequence Number**: A number used to denote/identify a packet sent. Also serves 
the purpose of denoting present and past packets

**Acknowledgement Number**: Denotes the sequence number of the next packet to be 
received. It can also denote the acknowledgment of the previous sent packet.

**Flag Bits**: An octet where each bit is a flag
- 1st bit - ACK bit: This bit is set when the received packet is an acknowledgement packet.
- 2nd bit - SYN bit: This is the synchronize bit, set when starting a new connection.
- 3rd bit - FIN bit: This is the finish bit, set when ending a connection.
- 4th bit - NUL bit: This is a null bit, set when pinging to check if host is online.
- 5th bit - BEG bit: This is the data begin (signal) bit. Packet with this bit set is sent before data is sent.
- 6th bit - END bit: This is the data end (signal) bit. Packet with this bit set is sent after data transfer is complete.

The rest 2 bits are unused.

**Data Index**: An index number used to represent the position of packet in the current window

**Content-Length**: Length of the payload in the current packet(in bytes).

**Checksum**: A number that uniquely denotes the content of each packet. Any corruption of 
packet data can be verified using this checksum.

**Payload**: The data chunk carried in the current packet.


### Connection Establishment

RDTP uses a 3-way handshake to establish a connection:
1) First, the sender sends a SYN packet with initial random sequence number
2) The receiver accepts the request and sends a SYN-ACK packet with its sequence number
3) The sender sends back ACK packet to confirm the connection

After performing above 3 steps, both sender and receiver now have the required parameters to 
communicate with each other. The connection is now established on both sender and receiver


### Data Transfer

Steps followed for Data Transfer between client and server:
1) Sender sends a BEG packet (which has the length of complete data to be sent in payload) to 
   indicate start of data transfer
2) Receiver akcs the BEG packet, notes the data length and is now ready to receive
3) Sender sends all the packets in the current window and waits for ACK’s for each packet form receiver. 
   After timeout, it resends all un-ACKed packets. When all packets in current window are ACKed, the 
   window slides forward to the next unsent data
4) Receiver ACK’s all the received packets and saves their data in a cache/data structure. 
   Receiver’s window only moves forward if all packets in the current window are received.
5) When the data transfer is complete, sender sends an END packet to denote the end of data transfer
6) Receiver ACKs the END packet, and now arranges the data received in order and sends it to the application


### Connection Termination

RDTP uses a similar 3-way handshake to signal connection termination:
1) First, the sender denotes the end of connection with a FIN packet
2) The remote receiver sends back a FIN-ACK packet to acknowledge termination
3) The sender ACKs the FIN-ACK packet and terminates

After the above 3 steps, both the sender and receiver successfully terminate and the 
connection is broken down.



## Assumptions

### Network Assumptions
- No error correction is provided. Therefore, any corrupted packet received will be dropped.
- No flow control is provided as of current specification. So data transfer is not regulated 
    either at sender or receiver
- Transferred packets are of fixed size.(subject to change)
- Packets which have not been acked before timeout are assumed to be lost
- A full duplex network link is assumed for bi-directional data transfer.

### Application Assumptions

