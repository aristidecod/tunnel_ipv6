#!/bin/bash

# Configuration de l'interface tun0 avec IPv6
sudo ip -6 addr add fc00:1234:ffff::2/64 dev tun0

# Activation de l'interface
sudo ip link set tun0 up

# Affichage de la configuration pour vérification
ip -6 addr show tun0
