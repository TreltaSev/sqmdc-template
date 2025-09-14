FROM archlinux:multilib-devel

# === SYSTEM SETUP ===
# Update database files for 'core' and 'extra'
RUN pacman -Sy
COPY .bashrc /.bashrc
# Install most packages
RUN pacman -S --noconfirm git unzip bun openssh

# === USER SETUP ===
# Create vscode user
RUN useradd -m -s /bin/bash -u 1000 -U vscode
# Make vscode user sudo
RUN usermod -aG wheel vscode
RUN echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/wheel

# === POST SETUP ===
# Copy init.sh file over
COPY init.sh /home/vscode/init.sh
RUN chmod o+rwx /home/vscode/init.sh
# Run init script
RUN /home/vscode/init.sh
