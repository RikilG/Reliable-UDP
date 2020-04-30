# RDTP - Reliable Data Transfer Protocol

This repo contains the specification and code for RDTP Protocol. This protocol 
is a part of our Networks course assignment in building a reliable protocol 
over UDP.

## Requirements
- Python (>=3.6)

## Instructions to Run
This repo provides an example file transfer application which can be run 
using the following commands:

```bash
# first run the receiver which listens for incomming connections
python fileReceiver.py -o <output filepath>

# run the sender which sends file to receiver at target IP address
# if no target ip is given, it defaults to localhost(127.0.0.1)
python fileSender.py -i <input filepath> -ip <ip_address>
```

## Team Members
- Rikil Gajarla - 2017A7PS0202H
- L Srihari - 2017A7PS1670H
- Koushik Perika - 2017A7PS0207H
- Sayanti Ghosh - 2017A7PS0261H
- Poosarala Divakar - 2017A7PS0225H

## Additional notes
RDTP specification can be found [here](./RDTP%20Specification.pdf) and performance 
analysis can be found [here](./RDTP%20-%20Performance%20Analysis.pdf)