FROM oven/bun:latest

WORKDIR /frontend

COPY frontend/package.json frontend/bun.lock ./

RUN bun install --force --verbose

# Expose Frontend Port
EXPOSE 3000
ENV PORT=3000

CMD ["bun", "run", "dev", "--host", "--port", "3000"]