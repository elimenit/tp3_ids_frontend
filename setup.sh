#!/bin/bash
option=$1
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
correr_aplicacion() {
    if [[ ! -f "app.py" ]]; then
        echo "[-] No existe el archivo app.py"
        exit 0

    fi
    python3 -m app
}
menu( ) {
    echo "------------------Menu de Opciones-----------------"
    echo "1) Correr Aplicacion en Python"
    echo "2) Correr aplicacion en Docker"
    echo "3) Salir"
}
main() {
    menu
    echo "Decargando tecnologias necesarias...!!"
    #tecnologias_sistema
    option=$1
    if [[ ! $option ]]; then
        read -p "Ingrese la opcion: " option
    fi
    

    if [[ $option -eq 1 ]]; then

        echo "Creando archivo de las variables de entorno!!."
        generar_punto_env
        activar_entorno_virtual
        echo "Intentando Correr Aplicacion..."
        correr_aplicacion
    elif [[ $option -eq 2 ]]; then
        echo "Intentando correr el container de Docker (Dockerfile)"
        correr_container_docker
    elif [[ $option -eq 3 ]]; then
        echo "Saliendo ..."
        exit 0
    else
        echo "Opcion no valida"
        exit 0
    fi

}
main $option