# Tunnel IPv6 sur IPv4

Ce projet implémente un système de tunneling permettant de faire communiquer deux réseaux IPv6 isolés à travers un réseau IPv4. Le tunnel encapsule le trafic IPv6 dans des paquets TCP/IPv4 pour permettre la connectivité entre les deux îlots IPv6.

---

## Contexte
Dans un scénario où deux réseaux IPv6 sont séparés par un réseau IPv4, ce projet permet de créer un tunnel bidirectionnel pour restaurer la connectivité IPv6.

## Topologie réseau

```
VM1-6 (IPv6) ←→ VM1 (IPv4) ←→ VM3 (IPv4) ←→ VM3-6 (IPv6)
```

## Architecture
Le projet est structuré autour de plusieurs composants :
- **Interface TUN** : Interface réseau virtuelle pour capturer et injecter le trafic
- **Bibliothèque de gestion TUN** : Création et gestion des interfaces virtuelles
- **Bibliothèque tunnel** : Gestion des extrémités du tunnel
- **Démon principal** : Service gérant le tunnel bidirectionnel

## Fonctionnalités
- Création d'interfaces TUN virtuelles
- Encapsulation IPv6 dans TCP/IPv4
- Tunnel bidirectionnel asynchrone
- Configuration via fichier
- Tests de connectivité et de performance

## Configuration IPv6
Pour activer IPv6 si désactivé :
```bash
# Activer IPv6 si désactivé
echo "net.ipv6.conf.all.disable_ipv6 = 0" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## Utilisation
1. **Configuration**
   - Créer un fichier de configuration avec les paramètres réseau appropriés (IP locales/distantes, ports, etc.)
2. **Tests de connectivité**
   - Test ping IPv6 :
     ```bash
     ping6 -c 1 [IP_DESTINATION_IPv6]
     ```
   - Test de bande passante :
     ```bash
     iperf3 -6 -c [IP_DESTINATION_IPv6]
     ```

## Tests
- **Couche 3** : Connectivité IPv6
- **Couche 4** : Transfert de fichiers avec netcat
- **Performance** : Tests de bande passante avec iperf3

## Débogage
- Capture de paquets :
  ```bash
  sudo tcpdump -i tun0
  ```
- Vérification des interfaces :
  ```bash
  ip link show
  ip addr show
  ```

## Améliorations possibles
- Chiffrement du tunnel
- Gestion automatique des routes
- Interface de monitoring

---

## Structure du projet
- `VM1`, `VM2`, `VM3`, `VM3-6`, `VM1-6` : Dossiers contenant la configuration et les scripts pour chaque VM.
- `partage/` : Dossier de partage de scripts et de fichiers communs.
- `notes_projet_reseaux.md` : Notes et documentation technique sur le projet.

## Technologies utilisées
- **Python** : Scripts de gestion du tunnel et de capture réseau.
- **SaltStack** : Automatisation de la configuration des VM.
- **Vagrant** : Provisionnement et gestion des VM.
- **Shell** : Scripts d'automatisation.

## Prérequis
- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/) ou autre provider compatible
- [Python 3](https://www.python.org/)
- [SaltStack](https://saltproject.io/)

## Auteurs
- aristidecod

## Licence
Ce projet est open source.