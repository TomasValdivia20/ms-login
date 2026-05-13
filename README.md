ReadMe MicroServicio Login:

En este readme encontraran todo lo relacionado con el microservicio de login:
encontraran multiples funciones tales como crear,eliminar,editar,actualizar
la cual tienen interaccion con el login del usuario.

Este microservicio esta hecho con Django, el cual utiliza Python, por lo cual
debemos seguir los siguientes pasos para poder correr este microservicio


Crear entorno virtual:
python -m venv venv

En Windows: venv\Scripts\activate
Instalar dependencias:

pip install -r requirements.txt

Migraciones:

python manage.py migrate

Crear Superusuario (opcional para el admin de Django):

python manage.py createsuperuser
