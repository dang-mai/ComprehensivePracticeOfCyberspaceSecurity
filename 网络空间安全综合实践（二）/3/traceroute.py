from scapy.all import *
import sys
import time

target = sys.argv[1]

print("通过最多 30 个跃点跟踪")

count = 1
flag = True
while flag:
    start = time.perf_counter()
    ans, unans = sr(IP(dst=target, ttl=count, id=RandShort())/TCP(flags=0x2), verbose=0, timeout=1)
    time_used = str(int((time.perf_counter() - start) * 1000)) + 'ms'

    if len(ans):
        for snd, rcv in ans:
            if isinstance(rcv.payload, TCP):
                flag = False
            print("%-5s %-5s %s" % (snd.ttl, time_used, rcv.src))
    else:
        temp = '*'
        for snd in unans:
            print("%-5s %-5s %s" % (snd.ttl, temp, temp))
    count += 1
    if count > 30:
        flag = False

print("跟踪完成")
