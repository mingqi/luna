#!/bin/bash

# FORWARD chain
/sbin/iptables -D FORWARD -d 172.16.0.0/12 -i docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
/sbin/iptables -D FORWARD -d 172.16.0.0/12 -i docker0 -j ALAUDA_LINK
/sbin/iptables -D FORWARD -d 172.16.0.0/12 -i docker0 -j DROP

/sbin/iptables -N ALAUDA_LINK

/sbin/iptables -I FORWARD -d 172.16.0.0/12 -i docker0 -j DROP
/sbin/iptables -I FORWARD -d 172.16.0.0/12 -i docker0 -j ALAUDA_LINK
/sbin/iptables -I FORWARD -d 172.16.0.0/12 -i docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# INPUT chain
/sbin/iptables -D INPUT -d 172.16.0.0/12 -i docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
/sbin/iptables -D INPUT -d 172.16.0.0/12 -i docker0 -j DROP

/sbin/iptables -I INPUT -d 172.16.0.0/12 -i docker0 -j DROP
/sbin/iptables -I INPUT -d 172.16.0.0/12 -i docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
