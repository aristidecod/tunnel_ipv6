# Configuration eth1
# RAPPEL: eth0 est à vagrant, ne pas y toucher

## Désactivation de network-manager
NetworkManager:
  service:
    - dead
    - enable: True
    
## Suppression de la passerelle par défaut
ip route del default:
  cmd:
    - run
   

##Configuration de VM2
eth1:
  network.managed:
    - enabled: True
    - type: eth
    - proto: static
    - ipaddr: 172.16.2.132
    - netmask: 28
    - enable_ipv6: false
    
eth2:
  network.managed:
    - enabled: True
    - type: eth
    - proto: static
    - ipaddr: 172.16.2.162
    - netmask: 28
    - enable_ipv6: false

# enable ipv4 forwarding
net.ipv4.ip_forward:
  sysctl:
    - present
    - value: 1

