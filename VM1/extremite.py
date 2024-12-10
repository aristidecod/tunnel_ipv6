import socket
import sys
import select

import os
import fcntl
import struct

def ext_out(port=123, tun_name='tun0'):
    """
    Crée un serveur qui écoute sur le port spécifié et redirige 
    les données reçues vers l'interface tun spécifiée
    """
    # Ouvrir et configurer tun0
    TUNSETIFF = 0x400454ca
    IFF_TUN = 0x0001
    IFF_NO_PI = 0x1000
    
    tun = os.open('/dev/net/tun', os.O_RDWR)
    ifr = struct.pack('16sH', tun_name.encode(), IFF_TUN | IFF_NO_PI)
    fcntl.ioctl(tun, TUNSETIFF, ifr)
    
    # Créer le serveur TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(1)
    
    print(f"Serveur en écoute sur le port {port}", file=sys.stderr)
    
    while True:
        client, addr = server.accept()
        print(f"Connexion acceptée depuis {addr}", file=sys.stderr)
        
        try:
            while True:
                # Recevoir les données du client
                data = client.recv(4096)
                if not data:
                    break
                # Écrire directement dans tun0
                os.write(tun, data)
        except Exception as e:
            print(f"Erreur: {e}", file=sys.stderr)
        finally:
            client.close()
            
def ext_in(host, port=123, tun_name='tun0'):
    """
    Ouvre une connexion TCP et lit le trafic de tun0 pour l'envoyer via la socket
    """
    # Ouvrir et configurer tun0
    TUNSETIFF = 0x400454ca
    IFF_TUN = 0x0001
    IFF_NO_PI = 0x1000
    
    tun = os.open('/dev/net/tun', os.O_RDWR)
    ifr = struct.pack('16sH', tun_name.encode(), IFF_TUN | IFF_NO_PI)
    fcntl.ioctl(tun, TUNSETIFF, ifr)
    
    # Créer et connecter la socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"Connexion au serveur {host}...", file=sys.stderr)
        sock.connect((host, port))
        print(f"Connecté à {host}:{port}", file=sys.stderr)
        
        while True:
            # Lire les paquets directement depuis tun0
            data = os.read(tun, 4096)
            if not data:
                break
            # Envoyer les paquets au serveur
            sock.sendall(data)
            
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
    finally:
        sock.close()
        os.close(tun)
