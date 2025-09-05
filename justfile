# Starts the docker process
[working-directory: './']
start SERVICE="" *FLAGS:
    bash compose/before.sh && \
        docker compose up \
        --build -d {{SERVICE}} {{FLAGS}}

# Stops specified docker processes
[working-directory: './']
stop SERVICE="":
    docker compose down {{SERVICE}}

# Runs a docker image or container, as the user
[working-directory: './']
run SERVICE="" *PARAMETERS:
    bash compose/before.sh && \ 
    docker compose \
    -f compose.yml \
    -f compose/dev.compose.yml \
    -f compose/test.compose.yml \
    run --rm {{SERVICE}} {{PARAMETERS}}

# Starts the docker process in development mode
[working-directory: './']
@dev SERVICE="" *FLAGS:
    bash compose/before.sh && docker compose -f compose.yml -f ./compose/dev.compose.yml up --build {{SERVICE}} {{FLAGS}}

# Prune all inactive docker files
[working-directory: './']
prune:
    docker system prune -f && docker volume prune -f

# Tools entrypoint
[working-directory: './']
@tool *ARGS:
    docker compose -f compose.yml -f compose/tools.compose.yml build --pull tools > /dev/null 2>&1
    docker compose -f compose.yml -f compose/tools.compose.yml run --remove-orphans --rm tools {{ARGS}}