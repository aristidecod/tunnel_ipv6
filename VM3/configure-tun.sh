#!/bin/bash

# Configuration de l'interface tun0 avec IPv6
sudo ip -6 addr add fc00:1234:ffff::2/64 dev tun0

# Activation de l'interface
sudo ip link set tun0 up

# Ajout de la route vers VM1-6 via tun0
sudo ip -6 route add fc00:1234:3::/64 dev tun0

# Affichage de la configuration pour vérification
ip -6 addr show tun0
ip -6 route show
