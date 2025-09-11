# Starts the docker process
[working-directory: './']
start SERVICE="" *FLAGS:
    just tool setup
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
    just tool setup
    bash compose/before.sh && \ 
    docker compose \
    -f compose.yml \
    -f compose/dev.compose.yml \
    -f compose/test.compose.yml \
    run --rm {{SERVICE}} {{PARAMETERS}}

# Starts the docker process in development mode
[working-directory: './']
@dev SERVICE="" *FLAGS:
    just tool --dev setup
    bash compose/before.sh && docker compose -f compose.yml -f ./compose/dev.compose.yml up --build {{SERVICE}} {{FLAGS}}

# Prune all inactive docker files
[working-directory: './']
prune:
    docker system prune -f
    docker volume prune -f

# Tools entrypoint
[working-directory: './']
@tool *ARGS:
    docker compose -f compose.yml -f compose/tools.compose.yml \
        build --pull \
        --build-arg UID="$(id -u)" --build-arg GID="$(id -g)" \
        tools
    docker compose -f compose.yml -f compose/tools.compose.yml \
        run --rm \
        -e HOST_USER=$(whoami) \
        -e HOST_CWD=$(pwd) \
        --user "$(id -u):$(id -g)" \
        tools {{ARGS}}
