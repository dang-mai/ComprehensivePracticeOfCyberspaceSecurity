#!/usr/bin/python 
from scapy.all import *

def spoof_pkt(pkt): 
		print("Original Packet.........") 
		print("Source IP : ", pkt[IP].src) 
		print("Destination IP :", pkt[IP].dst) 

		a = IP() 
		b = TCP() 
		data = pkt[TCP].payload 
		newpkt = a/b/data 

		print("Spoofed Packet.........") 
		print("Source IP : ", newpkt[IP].src) 
		print("Destination IP :", newpkt[IP].dst) 
		send(newpkt) 

pkt = sniff(filter=¡¯tcp¡¯,prn=spoof_pkt)
