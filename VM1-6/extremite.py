import socket
import sys

def ext_out(port=123):
    """
    Crée un serveur qui écoute sur le port spécifié et redirige 
    les données reçues vers la sortie standard.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', port))
    server.listen(1)
    
    while True:
        client, addr = server.accept()
        print(f"Connexion acceptée depuis {addr}", file=sys.stderr)
        
        try:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
        except Exception as e:
            print(f"Erreur: {e}", file=sys.stderr)
        finally:
            client.close()

def ext_in(host, port=123):
    """
    Ouvre une connexion TCP vers l'hôte distant et transmet 
    les données de l'entrée standard vers la socket.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((host, port))
        print(f"Connecté à {host}:{port}", file=sys.stderr)
        
        while True:
            data = sys.stdin.buffer.read1(4096)
            if not data:
                break
            sock.sendall(data)
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
    finally:
        sock.close()
