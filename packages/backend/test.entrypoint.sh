#!/bin/sh
set -e

# If the Caddy CA is mounted, install it into the trust store
if [ -f /caddydata/caddy/pki/authorities/local/root.crt ]; then
  cp /caddydata/caddy/pki/authorities/local/root.crt /usr/local/share/ca-certificates/caddy-local.crt || true
  update-ca-certificates || true
fi


exec /opt/venv/bin/pytest --disable-warnings --maxfail=1 -v -p pytest_asyncio "$@"