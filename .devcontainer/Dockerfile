FROM archlinux:multilib-devel

# === SYSTEM SETUP ===
# Update database files for 'core' and 'extra'
RUN pacman -Sy
COPY .bashrc /.bashrc
COPY sshd_config /etc/ssh/sshd_config
RUN pacman -S --noconfirm --needed git base-devel nodejs openssh unzip
RUN pacman -S --noconfirm unzip

# === USER SETUP ===
# Create vscode user
RUN useradd -m -s /bin/bash -u 1000 -U vscode
# Make vscode user sudo
RUN usermod -aG wheel vscode
RUN echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/wheel


ARG USER=vscode
ARG UID=1000
ARG GID=1000
ARG DOCKER_GID=970  
RUN groupadd -g ${GID} ${USER} || true \
 && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER} || true \
 && (getent group docker >/dev/null && groupmod -g ${DOCKER_GID} docker || groupadd -g ${DOCKER_GID} docker) \
 && usermod -aG docker ${USER}


# === POST SETUP ===
# Switch to vscode user
USER vscode
RUN curl -fsSL https://bun.com/install | bash
RUN sudo pacman -S --noconfirm docker docker-compose iptables shadow

# Setup ssh
RUN sudo ssh-keygen -A

RUN source /.bashrc
RUN ~/.bun/bin/bun i -g rust-just
# Switch back to root
USER root
# Copy init.sh file over
COPY init.sh /home/vscode/init.sh
RUN chmod o+rwx /home/vscode/init.sh
# Run init script
RUN /home/vscode/init.sh
