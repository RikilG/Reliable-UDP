# netem tool help

- lo - indicates loopback device (localhost or "127.0.0.1" in our sense). 
  can be replaced with any of `ip link` listed devices.

This commands can be found [here](https://wiki.linuxfoundation.org/networking/netem)

## Basic COMMAND SYNTAX
```
sudo tc qdisc <add/change> dev <lo/eth0> root netem <operation> <...operation params...>
```

## To see what is configured on an interface, do this
```
sudo tc -s qdisc ls dev lo
```

## Reset any modifications
```
sudo tc qdisc del dev lo root
```

## Delay
```
sudo tc qdisc add dev lo root netem delay <value in ms> [<+/- vary in ms> [<% for randomized correlation>]]
sudo tc qdisc add dev lo root netem delay 100ms 10ms 25%

# using distribution
sudo tc qdisc add dev lo root netem delay 100ms 10ms distribution normal
```

## Packet Loss
smallest possible loss value: 2^32 = 0.0000000232% 
```
# 1/1000 packets are randomly dropped
sudo tc qdisc change dev lo root netem loss 0.1% 

# Add correlation to emulate packet burst losses
sudo tc qdisc change dev lo root netem loss 0.3% 25%
```

## Packet Duplication
```
# specified similar to packet loss
sudo tc qdisc change dev lo root netem duplicate 1%
```

## Packet Corruption
Random noise can be emulated (in 2.6.16 or later) with the corrupt option. This introduces a single bit error at a random offset in the packet. 
```
# corrupt 1/1000 packets
sudo tc qdisc change dev lo root netem corrupt 0.1%
```

## Packet Re-order
The first method gap uses a fixed sequence and reorders every Nth packet. A simple usage of this is: 
```
sudo tc qdisc change dev lo root netem gap 5 delay 10ms
```
The second form reorder of re-ordering is more like real life. It causes a certain percentage of the packets to get mis-ordered. 
```
sudo tc qdisc change dev lo root netem delay 10ms reorder 25% 50%
# Newer versions of netem will also re-order packets if the random 
# delay values are out of order.
sudo tc qdisc change dev lo root netem delay 100ms 75ms
```

## Rate Control
```
sudo tc qdisc add dev lo root handle 1:0 netem delay 100ms
sudo tc qdisc add dev lo parent 1:1 handle 10: tbf rate 256kbit buffer 1600 limit 3000
```

## Emulate slow internet connection (not working in arch)
```
sudo tc qdisc add dev lo root handle 1: htb default 12 
sudo tc class add dev lo parent 1:1 classid 1:12 htb rate 56kbps ceil 128kbps 
sudo tc qdisc add dev lo parent 1:12 netem delay 1000ms
```