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
    
## Configuration IPv6
net.ipv6.conf.all.disable_ipv6:
  sysctl.present:
    - value: 0

##Configuration de VM1
eth1:
  network.managed:
    - enabled: True
    - type: eth
    - proto: static
    - ipaddr: 172.16.2.131
    - netmask: 28
    
eth2:
  network.managed:
    - enabled: True
    - type: eth
    - proto: static
    - enable_ipv4: false
    - ipv6proto: static
    - enable_ipv6: true
    - ipv6_autoconf: no
    - ipv6ipaddr: fc00:1234:3::1
    - ipv6netmask: 64

## Configuration de la route vers LAN2 via VM2
routes:
  network.routes:
    - name: eth1
    - routes:
      - name: LAN2
        ipaddr: 172.16.2.160/28
        gateway: 172.16.2.132
        



