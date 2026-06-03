#!/bin/bash
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
main() {
    echo "Decargando tecnologias necesarias...!!"
    tecnologias_sistema

    echo "Creando archivo de las variables de entorno!!."
    generar_punto_env
    python3 app.py
}
main