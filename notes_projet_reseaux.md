
# 2.2. Configuration de l'interface

## 1. Configuration de tun0
- L'interface tun0 a été configurée avec l'adresse fc00:1234:ffff::1/64
- Script configure-tun.sh créé avec les commandes suivantes :
```bash
#!/bin/bash
# Configuration de l'interface tun0 avec IPv6
sudo ip -6 addr add fc00:1234:ffff::1/64 dev tun0
# Activation de l'interface
sudo ip link set tun0 up
# Affichage de la configuration pour vérification
ip -6 addr show tun0
```

## 2. Modification du routage
- Sur VM1 : Aucune modification nécessaire car elle n'avait pas de route spécifique via VM2-6
- Sur VM1-6 : Il faut supprimer la route statique qui passait par VM2-6 car cette route n'est plus valide


## 3. Test ping6 fc00:1234:ffff::1
- Aucune capture visible sur Wireshark

## 4. Test ping6 fc00:1234:ffff::10
- Capture Wireshark montre des requêtes ICMPv6 Echo Request sans réponse
- Les paquets sont visibles avec la source fc00:1234:ffff::1 et la destination fc00:1234:ffff::10
les fichier de capture sont disponible dans partage/wireshark(fc00:1234:ffff::10).txt et wireshark(fc00:1234:ffff::10).csv

## 5. Explication de la différence de comportement

### Pour ping6 fc00:1234:ffff::1
- Cette adresse est configurée sur l'interface tun0
- Le paquet reste dans la pile réseau du système (network stack)
- Il n'apparaît pas dans Wireshark car il n'atteint jamais l'interface tun0 elle-même
- Le système le traite directement au niveau de la pile réseau

### Pour ping6 fc00:1234:ffff::10
- Cette adresse n'est pas configurée sur l'interface
- Le paquet doit donc être envoyé sur l'interface tun0
- C'est pourquoi on le voit dans Wireshark
- Mais comme il n'y a pas de programme pour le traiter, il n'y a pas de réponse

# 2.3. Récupération des paquets - Réponses détaillées

## 1. Implémentation de la fonction copy_data

```python
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
```

## 2. Résultats des tests ping6

* `ping6 fc00:1234:ffff::1` : Aucun affichage car ces paquets sont traités directement par le noyau Linux (adresse locale).
* `ping6 fc00:1234:ffff::10` : Affichage des paquets car cette adresse est inconnue du noyau.

## 3. Comparaison avec Wireshark

* Les paquets visibles dans Wireshark correspondent exactement à ceux affichés par notre programme
* Les deux outils capturent les mêmes paquets car ils observent la même interface tun0
* On voit principalement des paquets ICMPv6 (ping/echo request)
les fichier de capture sont disponible dans partage/notes.txt

## 4. Option IFF_NO_PI

* Sans IFF_NO_PI : Les paquets commencent par 4 octets d'en-tête (`00 00 86 dd`)
* Avec IFF_NO_PI : Les paquets commencent directement par l'en-tête IP (`60...`)
L'option IFF_NO_PI supprime l'en-tête Protocol Information, donnant accès directement aux paquets IP bruts.


