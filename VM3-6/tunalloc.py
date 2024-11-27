#!/usr/bin/python3
# Allocate a tun/tap virtual network device

import os,sys
from fcntl import ioctl
import getopt, struct

def tun_alloc(dev):
    # Create Interface
    try:
        fd = os.open("/dev/net/tun", os.O_RDWR)
    except IOError as err:
        print("Alloc tun :" + os.strerror())
        exit(-1)

    # Config Flags:
    # IFF_TUN   - TUN device (no Ethernet headers) 
    # IFF_TAP   - TAP device
    # IFF_NO_PI - Do not provide packet information  
    TUNSETIFF = 0x400454ca
    IFF_TUN   = 0x0001
    IFF_TAP   = 0x0002
    IFF_NO_PI = 0x1000

    TUNMODE = IFF_TUN
    try:
        ifs = ioctl(fd, TUNSETIFF, struct.pack("16sH", bytes(dev,'utf-8'), TUNMODE))
    except OSError as err:
        print("Options tun", os.strerror(err.errno))
        exit(-1)

    ifname = ifs[:16].strip(b'\0')

    return fd, ifname

##################################################"
# Main
argv = sys.argv
print("CrÃ©ation de", argv[1])
tunfd,ifname = tun_alloc(argv[1])
print(f"Faire la configuration de {ifname}...")
input("Appuyez sur une touche pour continuer")
print(f"Interface {ifname} ConfigurÃ©e : ")
os.system("ip addr")
input("\nAppuyez sur une touche pour terminer.")

exit(0)
