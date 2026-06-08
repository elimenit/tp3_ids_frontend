#!/bin/bash
export DOCKER_BUILDKIT=0 # (Build)
URL_API="http://127.0.0.1:15000/"
tecnologias_sistema() {
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip python3-venv
}
activar_entorno_virtual() {
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -r requirements.txt
}
generar_punto_env() {
    if [[ ! -f ".env" ]]; then
        echo -ne "URL_API='http://127.0.0.1:15000/'\n" > .env
    else
        echo "Archivo .env ya existente!!!."
    fi
}
correr_container_docker() {
    
    echo "Construyendo imagen del frontend!!!"
    docker build -t tp3_frontend .
    echo "Corriendo contenedor de la imagen del frontend en el puerto 10000!!"
    docker run --name tp3_frontend -e URL_API="$URL_API" -p 10000:10000 tp3_frontend 
    docker container rm tp3_frontend
    docker image rm tp3_frontend
}
main() {
    echo "Decargando tecnologias necesarias...!!"
    #tecnologias_sistema

    echo "Creando archivo de las variables de entorno!!."
    generar_punto_env
    correr_container_docker
}
main