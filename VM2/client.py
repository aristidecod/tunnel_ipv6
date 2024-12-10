# client.py
from extremite import ext_in
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} adresse_ip_serveur")
        sys.exit(1)
        
    server_address = sys.argv[1]
    print(f"Connexion au serveur {server_address}...")
    ext_in(server_address, 123)
