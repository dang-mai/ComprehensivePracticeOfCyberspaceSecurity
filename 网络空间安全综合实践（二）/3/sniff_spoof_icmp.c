#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>
#include <pcap.h>
#include <ctype.h>
#include "myheader.h"

unsigned short in_cksum(unsigned short *buf,int length);
void send_raw_ip_packet(struct ipheader* ip);



void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet)
{
    int size_data=0;
    printf("\nGot a packet\n");
    struct icmpheader *icmp1;
    icmp1 = (struct icmpheader *)(packet + sizeof(struct ethheader) + sizeof(struct ipheader));

    if(icmp1->icmp_type == 8) {
        struct ipheader *ip1 = (struct ipheader *) (packet + sizeof(struct ethheader));
        printf("	From: %s\n", inet_ntoa(ip1->iph_sourceip));
        printf("	To: %s\n", inet_ntoa(ip1->iph_destip));

        char buffer[PACKET_LEN];
        memset(buffer, 0, PACKET_LEN);

        char *data = (u_char *) packet + sizeof(struct ethheader) + sizeof(struct ipheader) + sizeof(struct icmpheader);
        size_data = ntohs(ip1->iph_len) - (sizeof(struct ipheader) + sizeof(struct icmpheader));
        if (size_data > 0) {
            memcpy((char *)(buffer + sizeof(struct ipheader) + sizeof(struct icmpheader)), (char *)data, size_data);
        }

        struct icmpheader *icmp;
        icmp = (struct icmpheader *)(buffer + sizeof(struct ipheader));
        icmp->icmp_type = 0; //ICMP Type: 8 is request, 0 is reply.
        // Calculate the checksum for integrity
        icmp->icmp_chksum = 0;
        icmp->icmp_id = icmp1->icmp_id;
        icmp->icmp_seq = icmp1->icmp_seq;
        icmp->icmp_chksum = in_cksum((unsigned short *)icmp,
                                     sizeof(struct icmpheader) + size_data);

        struct ipheader *ip = (struct ipheader *) (buffer);
        ip->iph_ver = 4;
        ip->iph_ihl = ip1->iph_ihl;
        ip->iph_tos = 16;
        ip->iph_ident = htons(54321);
        ip->iph_ttl = 64;
        ip->iph_sourceip.s_addr = ip1->iph_destip.s_addr;
        ip->iph_destip.s_addr = ip1->iph_sourceip.s_addr;
        ip->iph_protocol = IPPROTO_ICMP; // The value is 1, representing ICMP.
        ip->iph_len = htons(sizeof(struct ipheader) + sizeof(struct icmpheader) + size_data);
        
        send_raw_ip_packet (ip);
    }
}

int main() {
    pcap_t *handle;
    char errbuf[PCAP_ERRBUF_SIZE];
    struct bpf_program fp;
    char filter_exp[] = "ICMP";
    bpf_u_int32 net;

    // Step 1: Open live pcap session on NIC with interface name
    handle = pcap_open_live("docker0", BUFSIZ, 1, 1000, errbuf);  // docker

    // Step 2: Compile filter_exp into BPF psuedo-code
    pcap_compile(handle, &fp, filter_exp, 0, net);
    pcap_setfilter(handle, &fp);

    // Step 3: Capture packets
    pcap_loop(handle, -1, got_packet, NULL);

    pcap_close(handle); //Close the handle
    return 0;
}

void send_raw_ip_packet(struct ipheader* ip)
{
    struct sockaddr_in dest_info;
    int enable = 1;

    // Create a raw network socket, and set its options.
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &enable, sizeof(enable));

    // Provide needed information about destination.
    dest_info.sin_family = AF_INET;
    dest_info.sin_addr = ip->iph_destip;

    // Send the packet out.
    printf("Sending spoofed IP packet...\n");
    if(sendto(sock,ip,ntohs(ip->iph_len),0,(struct sockaddr *)&dest_info,sizeof(dest_info)) < 0)
    {
        perror("PACKET NOT SENT\n");
        return;
    }
    else {
        printf("\n---------------------------------------------------\n");
        printf("   From: %s\n",inet_ntoa(ip->iph_sourceip));
        printf("   To: %s\n",inet_ntoa(ip->iph_destip));
        printf("\n---------------------------------------------------\n");
    }
    close(sock);
}

unsigned short in_cksum(unsigned short *buf,int length)
{
    unsigned short *w = buf;
    int nleft = length;
    int sum = 0;
    unsigned short temp=0;

    /*
    * The algorithm uses a 32 bit accumulator (sum), adds
    * sequential 16 bit words to it, and at the end, folds back all the
    * carry bits from the top 16 bits into the lower 16 bits.
    */
    while (nleft > 1)  {
        sum += *w++;
        nleft -= 2;
    }

    /* treat the odd byte at the end, if any */
    if (nleft == 1) {
        *(u_char *)(&temp) = *(u_char *)w ;
        sum += temp;
    }

    /* add back carry outs from top 16 bits to low 16 bits */
    sum = (sum >> 16) + (sum & 0xffff);     // add hi 16 to low 16
    sum += (sum >> 16);                     // add carry
    return (unsigned short)(~sum);
}

