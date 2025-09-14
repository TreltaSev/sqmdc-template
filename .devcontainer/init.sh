#!/bin/bash

# Ensure bashrc
source /.bashrc

# === USER SETUP ===

# # Docker user
# groupadd -g 998 docker || true
# usermod -aG docker vscode

# copy bashrc file over
cp /.bashrc /home/vscode/.bashrc

# === PACKAGE INSTALLATION ===

# git
pacman -S --noconfirm git

# bun
pacman -S --noconfirm unzip
curl -fsSL https://bun.com/install | bash

# just
bun i -g rust-just

# ssh
pacman -S --noconfirm openssh
