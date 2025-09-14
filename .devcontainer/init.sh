#!/bin/bash

# Ensure bashrc
source /.bashrc

# === USER SETUP ===

# Vscode user
useradd -m -s /bin/bash -u 1000 -U vscode
usermod -aG wheel vscode # Make user sudo
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/wheel

# Docker user
groupadd -g 998 docker || true
usermod -aG docker vscode

# copy bashrc file over
cp /.bashrc /home/vscode/.bashrc

# === PACKAGE INSTALLATION ===

# bun
curl -fsSL https://bun.com/install | bash

# just
bun i -g rust-just

# ssh
pacman -S --noconfirm openssh
