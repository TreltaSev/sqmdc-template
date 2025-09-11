FROM alpine:3.19

## Install Packages
RUN apk add --update --no-cache python3 git libpq-dev gcc py3-pip python3-dev g++ py3-virtualenv bash curl
RUN apk add --no-cache openssh-client

# Bun
RUN curl -fsSL https://bun.com/install | bash
ENV BUN_INSTALL="/root/.bun"
ENV PATH="$BUN_INSTALL/bin:$PATH"

RUN bun i -g prettier

WORKDIR /tools

COPY tools/requirements.txt ./

# Build venv using virtualenv
RUN python3 -m virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements using the venv's pip
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install -r requirements.txt

# Copy backend utilities
RUN mkdir -p /deps/backend/src/utils
COPY backend/src/utils /deps/backend/src/utils
COPY backend/pyproject.toml /deps/backend/pyproject.toml
COPY backend/requirements.txt /deps/backend/requirements.txt

RUN /opt/venv/bin/pip install -e /deps/backend

COPY tools/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

## Add user
RUN adduser -D -u 1000 appuser

## chown folders
RUN mkdir /logs /project
RUN chown -R appuser:appuser /tools /logs /project /tools 

USER appuser
ENTRYPOINT [ "/entrypoint.sh" ]