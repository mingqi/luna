#!/bin/bash

iptables -D FORWARD -d 172.16.0.0/12 -i docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -D FORWARD -d 172.16.0.0/12 -i docker0 -j ALAUDA_LINK
iptables -D FORWARD -d 172.16.0.0/12 -i docker0 -j DROP

iptables -N ALAUDA_LINK

iptables -I FORWARD -d 172.16.0.0/12 -i docker0 -j DROP
iptables -I FORWARD -d 172.16.0.0/12 -i docker0 -j ALAUDA_LINK
iptables -I FORWARD -d 172.16.0.0/12 -i docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
