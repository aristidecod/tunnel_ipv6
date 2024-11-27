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
  ```bash
  sudo ip -6 route del fc00:1234:4::/64 via [ancienne_adresse_VM2-6]
  ```

## 3. Test ping6 fc00:1234:ffff::1
- Aucune capture visible sur Wireshark

## 4. Test ping6 fc00:1234:ffff::10
- Capture Wireshark montre des requêtes ICMPv6 Echo Request sans réponse
- Les paquets sont visibles avec la source fc00:1234:ffff::1 et la destination fc00:1234:ffff::10

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
