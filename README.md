<br />
<p align="center">
  <h2 align="center">Reliable Data Transfer Protocol (RDTP)</h2>

  <p align="center">
    A reliable protocol built over UDP
  </p>
</p>


## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Dependencies](#dependencies)
  - [To Run](#to-run)
- [Usage](#usage)
- [Project Layout](#project-layout)
- [License](#license)
- [Project Contributors](#project-contributors)


## About The Project

This repo contains the specification and code for RDTP Protocol. This protocol 
is a part of our Networks course assignment in building a reliable protocol 
over UDP.

We have selected a file transfer application which uses the built specification's
API to transfer files. Performance analysis is performed usig [netem](https://wiki.linuxfoundation.org/networking/netem) tool

RDTP specification can be found [here](./RDTP%20Specification.pdf) and performance 
analysis can be found [here](./RDTP%20-%20Performance%20Analysis.pdf)


## Getting Started

To get a local copy up and running follow these simple steps.  
This protocol is implemented in python ver >= 3.7.


### Dependencies

There are no external dependencies/modules used. The following core python modules are used:
 - sockets
 - math
 - random


### To Run
 
1. Clone the Reliable-UDP
```sh
git clone https://github.com/RikilG/Reliable-UDP.git
cd Reliable-UDP
```
2. To run the file transfer application
```sh
# first run the receiver which listens for incomming connections
python fileReceiver.py -o <output filepath>

# run the sender which sends file to receiver at target IP address
# if no target ip is given, it defaults to localhost(127.0.0.1)
python fileSender.py -i <input filepath> -ip <ip_address>
```


## Usage

The API provided is explained in the specification. It's usage example is the file 
transfer application.  
RDTPConnection package provides 2 modules RDTPSender and RDTPReceiver which 
can be used by you application to transfer data.


## Project Layout

```sh
Repo root directory
  ├── Images # Graphs produced by performance analysis
  │   ├── Corrupt_Throughput.png
  │   ├── Corrupt_Time.png
  │   ├── Delay_Throughput.png
  │   ├── Delay_Time.png
  │   ├── Duplication_Throughput.png
  │   ├── Duplication_Time.png
  │   ├── Jitter_Throughput.png
  │   ├── Jitter_Time.png
  │   ├── Loss_Throughput.png
  │   ├── Loss_Time.png
  │   ├── Reorder_Throughput.png
  │   └── Reorder_Time.png
  ├── other # Other stuff which helped in building the protocol
  │   ├── ...
  │   └── UDPsender.py
  ├── RDTPConnection
  │   ├── __init__.py
  │   ├── Packet.py
  │   ├── RDTPReceiver.py
  │   ├── RDTPSender.py
  │   ├── SocketCore.py
  │   ├── SRSocket.py
  │   └── SWSocket.py
  ├── analysis.py
  ├── assignment-3.pdf
  ├── fileReceiver.py
  ├── fileSender.py
  ├── LICENSE
  ├── RDTP - Performance Analysis.pdf
  ├── RDTP Specification.pdf
  ├── README.md
  └── Specification.md
```


## License

Distributed under the MIT License. See `LICENSE` for more information.


## Project Contributors

- Rikil Gajarla - 2017A7PS0202H
- L Srihari - 2017A7PS1670H
- Koushik Perika - 2017A7PS0207H
- Sayanti Ghosh - 2017A7PS0261H
- Poosarala Divakar - 2017A7PS0225H

Project Link: [https://github.com/RikilG/Reliable-UDP](https://github.com/RikilG/Reliable-UDP).