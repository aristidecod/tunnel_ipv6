import socket
import sys
import select
import os
import fcntl
import struct

def ext_out(port=123, tun_name='tun0'):
    """
    Crée un serveur qui écoute sur le port spécifié et gère
    la communication bidirectionnelle entre le client TCP et l'interface tun
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
                # Attendre des données soit du client soit de tun0
                readable, _, _ = select.select([client, tun], [], [])
                
                for fd in readable:
                    if fd is client:
                        # Données venant du client TCP
                        data = client.recv(4096)
                        if not data:
                            raise Exception("Client déconnecté")
                        # Écrire vers tun0
                        os.write(tun, data)
                    
                    if fd is tun:
                        # Données venant de tun0
                        data = os.read(tun, 4096)
                        if not data:
                            continue
                        # Envoyer au client TCP
                        client.send(data)
                        
        except Exception as e:
            print(f"Erreur: {e}", file=sys.stderr)
        finally:
            client.close()
            print(f"Connexion fermée avec {addr}", file=sys.stderr)
            
            
def ext_in(host, port=123, tun_name='tun0'):
    """
    Ouvre une connexion TCP et gère le trafic bidirectionnel entre tun0 et le serveur
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
            # Attendre des données soit de tun0 soit du serveur
            readable, _, _ = select.select([tun, sock], [], [])
            
            for fd in readable:
                if fd is tun:
                    # Données venant de tun0
                    data = os.read(tun, 4096)
                    if not data:
                        continue
                    # Envoyer au serveur
                    sock.sendall(data)
                
                if fd is sock:
                    # Données venant du serveur
                    data = sock.recv(4096)
                    if not data:
                        raise Exception("Serveur déconnecté")
                    # Écrire vers tun0
                    os.write(tun, data)
            
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
    finally:
        sock.close()
        os.close(tun)
