# Implement my own Application layer protocol based on reliable UDP

## Roadmap/Notes
 - [ ] Write a class to implement protocol
 - [ ] Designing reliability over UDP in application layer. Take care of:
   - [ ] Sequence numbers
   - [ ] Checksum for corruption verification
   - [ ] Acknowledgements
   - [ ] Re-transmissions
   - [ ] In-Order Delivery
   - [ ] Connection handling (close connection with a END/RST signal, persistent-connection check, etc)
   - [ ] Flow control (rate of sending/receiving packets) (Not required as assignment talks of reliability only)
 - [ ] A toy application (chat, messaging, file transfer, etc) which uses the designed protocol
 - [ ] A Readme.txt file with instructions to compile and run the application
 - [ ] Submit a Protocol Specification
   - [ ] Have a look at example specification in folder
   - [ ] Contain assumptions about application
   - [ ] Contain assumptions about network
   - [ ] Strategies to tackle different situations
   - [ ] 2-3 pages with 11 point font size for non-header text
 - [ ] PDF with plots of performance analysis under different network conditions: (using netem tool to emulate conditions on localhost)
   - [ ] packet loss
   - [ ] delays
   - [ ] re-ordering
   - [ ] corruption
   - [ ] jitter?
   - [ ] rate?


## Some Assumptions (we can have)
 - no error correction provided/corrupted packets are dropped
 - no flow control provided/fixed data transmission rate
 - udp packets/segments are of fixed size?
 - packets that do not receive ACK are assumed to lost/corrupted
 - (if implemented) SRP requires full duplex link


## Ideas
**Reliable UDP(RUDP or RDP)**: the sender sends all packets as normal UDP packets and the receiver indexes all the packets. Once all the packets are transmitted, the receiver sends a lists of packet indices that it did not receive (SRP?). This can make UDP reliable.


## References/Links
 - [kurose-ross assign overview](https://www.cs.grinnell.edu/~weinman/courses/CSC364/2014S/labs/reliable-data-transfer.html)
 - [Reliable UDP (exisiting) specification](https://tools.ietf.org/id/draft-ietf-sigtran-reliable-udp-00.txt)
 - [Real Python socket guide](https://realpython.com/python-sockets/)
 - [Socket Python Docs](https://docs.python.org/3/howto/sockets.html)
 - [netem - emulate network conditions](https://wiki.linuxfoundation.org/networking/netem?utm_medium=twitter&utm_source=twitterfeed)
 - [selective repeat protocol(SRP)](https://www.geeksforgeeks.org/sliding-window-protocol-set-3-selective-repeat/)
