#!/usr/bin/python3
# Allocate a tun/tap virtual network device

import os,sys
from fcntl import ioctl
import getopt, struct
import select

def tun_alloc(dev):
    """
    Cette fonction tun_alloc :
    1. Crée une interface réseau virtuelle (comme un "faux câble réseau")
    2. Cette interface est de type TUN (niveau IP) plutôt que TAP (niveau Ethernet)
    3. Vous donne un descripteur (fd) qui permet de :
       - Lire les paquets qui arrivent sur cette interface (avec read)
       - Écrire des paquets sur cette interface (avec write)
    """
    # 1. Ouvre le "fichier" qui permet de créer des interfaces TUN/TAP
    try:
        fd = os.open("/dev/net/tun", os.O_RDWR)
    except IOError as err:
        print("Alloc tun :" + os.strerror())
        exit(-1)

    # 2. Définition des constantes pour configurer l'interface
    TUNSETIFF = 0x400454ca  # Code spécial pour configurer l'interface
    IFF_TUN   = 0x0001      # Mode TUN (niveau IP)
    IFF_TAP   = 0x0002      # Mode TAP (niveau Ethernet)
    IFF_NO_PI = 0x1000      # Sans Protocol Information

    """
    # 3. On choisit le mode TUN
    TUNMODE = IFF_TUN
    """

    # Après (avec IFF_NO_PI)
    TUNMODE = IFF_TUN | IFF_NO_PI

    # 4. Configuration de l'interface avec ioctl
    try:
        # Prépare les données : nom de l'interface + mode
        ifs = ioctl(fd, TUNSETIFF, struct.pack("16sH", 
                                              bytes(dev,'utf-8'),  # Nom (ex: "tun0")
                                              TUNMODE))            # Mode (TUN)
    except OSError as err:
        print("Options tun", os.strerror(err.errno))
        exit(-1)

    # 5. Récupère le nom de l'interface créée
    ifname = ifs[:16].strip(b'\0')

    # 6. Retourne le descripteur et le nom
    return fd, ifname
    
def copy_data(src_fd, dst_fd):
    """
    Cette fonction:
    1. Lit en continu les paquets depuis l'interface TUN (src_fd)
    2. Les copie vers la destination (dst_fd)
    """
    BUFFER_SIZE = 2048  # Taille maximale d'un paquet
    
    while True:
        try:
            # Attend qu'il y ait des données à lire
            ready_to_read, _, _ = select.select([src_fd], [], [])
            
            if src_fd in ready_to_read:
                # Lit les données depuis l'interface TUN
                data = os.read(src_fd, BUFFER_SIZE)
                if data:
                    # Écrit les données vers la destination
                    os.write(dst_fd, data)
        except KeyboardInterrupt:
            print("\nArrêt de la copie des paquets")
            break
        except Exception as e:
            print(f"Erreur: {e}", file=sys.stderr)
            break

##################################################"
# Main
    """
    Pour tester:
        - src_fd sera le descripteur de tun0
        - dst_fd sera 1 (sortie standard)
        - Utilisez | hexdump -C pour voir les paquets en hexadécimal
    """
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <interface>")
        sys.exit(1)

    print("Création de", sys.argv[1])
    tunfd, ifname = tun_alloc(sys.argv[1])
    print(f"Interface {ifname.decode('utf-8')} créée")
    
    print("Démarrage de la capture des paquets... (Ctrl+C pour arrêter)")
    # Copie les paquets vers la sortie standard (1)
    copy_data(tunfd, 1)
    
    os.close(tunfd)

exit(0)
