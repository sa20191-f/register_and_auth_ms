# register_and_auth_ms

## Instrucciones para ejecutar la aplicación
### En un entorno virtual de python (localmente)
    Clonar el proyecto y ubicarse en la raíz.
    
    $ python3 -m venv project_env
    $ source project_env/bin/activate
    $ pip3 install -r requirements.txt
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    $ python3 manage.py runserver
    
### En un contenedor de docker
    Crear el servidor rancher
    Crear un nodo en el servidor rancher
    Ubicarse sobre el nodo (en caso de este ejemplo, el nodo 2)
    
    $ docker-machine start rancher-server
    $ docker-machine start rancher-node2
    $ eval $(docker-machine env rancher-node2)
    $ docker-compose build
    $ docker-compose up

