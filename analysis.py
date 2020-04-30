#!/usr/bin/env python

import matplotlib.pyplot as plt

print("Using file size: 16.2KB")

# Delay vs Time taken
# time for 0 delay = 0.003 s
delay   = [10, 20, 50, 80, 100, 150, 200, 400, 700, 1000, 1500, 2000, 3000, 5000]
time    = [0.125, 0.244, 0.605, 0.963, 1.2, 1.8, 2.4, 4.8, 8.4, 12, 18, 20, 30, 40]
plt.title("Delay vs Time")
plt.ylabel("Time taken (in sec)")
plt.xlabel("Delay (in ms)")
plt.plot(delay,time)
# plt.legend()
# plt.grid(True)
plt.show()

# Delay vs Throughput
# throughput for 0 delay = 6161 KB/s
delay       = [10, 20, 50, 80, 100, 150, 200, 400, 700, 1000, 1500]#, 2000, 5000]
throughput  = [128, 66, 26, 16, 13, 9, 6.7, 3.3, 1.9, 1.3, 0.87,]# 0.80, 0.4]
plt.title("Delay vs Throughput")
plt.ylabel("Throughput (KB/s)")
plt.xlabel("Delay (in ms)")
plt.plot(delay,throughput)
plt.show()

# Loss % vs Time taken
# time for 0 loss = 0.002 s
loss = [5, 10, 20, 35, 50]#, 80, 100]
time = [3, 10, 23, 45, 70]
plt.title("Loss % vs Time")
plt.ylabel("Time taken (in sec)")
plt.xlabel("Loss %")
plt.plot(loss,time)
plt.show()

# Loss % vs Throughput
# throughput for 0 loss = 7990 KB/s
loss = [5, 10, 20, 35, 50]#, 80, 100]
throughput = [5.3, 1.6, 0.7, 0.37, 0.2]
plt.title("Loss % vs Throughput")
plt.ylabel("Throughput (KB/s)")
plt.xlabel("Loss %")
plt.plot(loss, throughput)
plt.show()

# Corruption % vs Time taken
# time for 0 corrupt = 0.002
corrupt = [5, 10, 20, 35, 50]#, 80, 100]
time = [5, 10, 28, 40, 75]
plt.title("Corrupt % vs Time")
plt.ylabel("time (in sec)")
plt.xlabel("Corrupt %")
plt.plot(corrupt, time)
plt.show()

# Corruption % vs Throughput
# throughput for 0 corrupt = 8127 KB/s
corrupt = [5, 10, 20, 35, 50]#, 80, 100]
throughput = [3.2, 2, 0.8, 0.36, 0.21]
plt.title("Corrupt % vs Throughput")
plt.ylabel("Throughput (KB/s)")
plt.xlabel("Corrupt %")
plt.plot(corrupt, throughput)
plt.show()

# Packet Reorder vs Time taken
reorder = [0, 5, 10, 20, 35, 50, 80, 100]
time = [0.8, 1.004, 0.903, 0.902, 0.8, 0.7, 0.3, 0.1]
plt.title("Reorder(in 100ms delay) % vs Time")
plt.ylabel("Time taken (in sec)")
plt.xlabel("Reorder %")
plt.plot(reorder, time)
plt.show()

# Packet Reorder vs Throughput
reorder = [0, 5, 10, 20, 35, 50, 80, 100]
throughput = [20, 16, 17, 17, 22, 72, 78, 158]
plt.title("Reorder(in 100ms delay) % vs Throughput")
plt.ylabel("Throughput (in KB/s)")
plt.xlabel("Reorder %")
plt.plot(reorder, throughput)
plt.show()

# Packet Duplication vs Time
# time for 0 duplication = 0.0021
duplication = [0, 5, 10, 20, 35, 50]#, 80, 100]
time = [0.0015, 0.0022, 0.0018, 0.002, 0.0023, 0.0021]
plt.title("Duplication % vs Time")
plt.ylabel("Time taken (in sec)")
plt.xlabel("Duplication %")
plt.ylim(0, 0.01)
plt.plot(duplication, time)
plt.show()

# Packet Duplication vs Throughput
# throughput for 0% duplication = 10225 KB/s
duplication = [0, 5, 10, 20, 35, 50]#, 80, 100]
throughput = [8225, 7222, 7327, 8017, 6805, 7628]
plt.title("Duplication % vs Throughput")
plt.ylabel("Throughput (KB/s)")
plt.xlabel("Duplication %")
plt.ylim(3000, 10000)
plt.plot(duplication, throughput)
plt.show()

# Jitter vs Time taken
jitter   = [10, 20, 50, 80, 100]
time    = [2, 2.09, 2, 2.15, 2.01]
plt.title("Jitter(in 200ms Delay) vs Time")
plt.ylabel("Time taken (in sec)")
plt.xlabel("jitter (in ms)")
plt.ylim(0, 4)
plt.plot(jitter,time)
plt.show()

# Jitter vs Throughput
jitter       = [10, 20, 50, 80, 100]
throughput  = [8, 7.7, 8, 7.4, 8.02]
plt.title("Jitter(in 200ms Delay) vs Throughput")
plt.ylabel("Throughput (KB/s)")
plt.xlabel("Jitter (in ms)")
plt.ylim(0, 18)
plt.plot(jitter,throughput)
plt.show()