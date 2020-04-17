# RDTP (Reliable Data Transfer Protocol)(Name subject to change) Specification

## Table of Contents

- [Abstract](#abstract)
- [Introduction](#introduction)
- [Specification](#specification)
    - [Process](#process)
    - [Data Structure Format](#data-structure-formal)
- [Assumptions](#assumptions)
    - [Network Assumptions](#network-assumptions)
    - [Application Assumptions](#application-assumptions)
- [Performance Analysis](#performance-analysis)
- [References](#references)


## Abstract

This specification describes Reliable Data Transfer Protocol(RDTP). RDTP is lightweight 
packet transfer protocol with the basic aim to provide in-order reliable packet delivery 
layered over traditional UDP/IP Protocol. This protocol is suitable for simple 
communication protocols like instant messaging or chat(application subject to change).


## Introduction

RDTP aims to provide a flexible and minimal design over existing UDP transport protocol 
with support for in-order and reliable delivery using a sliding window protocol.


## Specification

### Process

**Sender**: The sender calls the send method from the RDTP library
1) Application data is divided into chunks of fixed size(size subject to change).
2) A header with packet info is attached to each chunk
3) A connection with the receiver is opened
4) Packets are sent out using a reliable and in order delivery protocol
5) Return the status of data sent with error if any

**Receiver**: Receiver listens for any sent data and transfers it to application in case
of a delivery
1) A socket is created and bind to a port to receive data
2) When an inbound connection is detected, it is accepted and data transfer starts
3) All the received data is collected according to the delivery protocol
4) Collected data is sorted in-oreder, stripped of its headers and sent to the application


### Data Structure Format

**Header Format**:
- 1st byte: Sequence number.
- 2nd byte: Acknowledgement number.
- 3rd byte: Protocol flags.
- 4th byte: Protocol attributes (like length of packet)
- 5th and 6th byte: Checksum

```
+----------------+----------------+
|   Seq Number   |   Ack Number   |
+----------------+----------------+
|    Flag Bits   |   Attributes   |
+----------------+----------------+
|             Checksum            |
+----------------+----------------+
|                                 |
|              Data               |
|                                 |
+----------------+----------------+
```

**Sequence Number**: 

**Acknowledgement Number**:

**Flag Bits**: An octet where each bit is a flag
- 1st bit - ACK bit: This bit is set when the received packet is an acknowledgement packet.
- 2nd bit - SYN bit: This is the synchronize bit, set when starting a new connection.
- 3rd bit - FIN bit: This is the finish bit, set when ending a connection.
- 4th bit - NUL bit: This is a null bit, set when pinging to check if host is online.

The rest 4 bits are unused.


## Assumptions

### Network Assumptions
- No error correction is provided. Therefore, any corrupted packet reveiced will be dropped.
- No flow control is provided as of current specification. So data transfer is not regulated 
    either at sender or receiver
- Transfered packets are of fixed size.(subject to change)
- Packets which have not been acked before timeout are assumed to be lost
- A full duplex network link is assumed for bi-directional data transfer.

### Application Assumptions

