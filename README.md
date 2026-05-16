Configuración del entorno — Blessing Backend
El proyecto usa dos bases de datos separadas: una local para desarrollo y Neon (la nube) para producción.

Primera vez que clonan el proyecto:

1. Pedir los archivos .env.dev y .env.prod (no están en Git por seguridad)
2. Colocarlos en la raíz del proyecto, al mismo nivel que manage.py
3. Crear la BD local en PostgreSQL:

CREATE DATABASE BlessingDev;
CREATE USER blessing_user WITH PASSWORD 'la_password_que_les_den';
GRANT ALL PRIVILEGES ON DATABASE BlessingDev TO blessing_user;

4. Aplicar migrations:
python manage.py migrate

5. Crear su superusuario local:
python manage.py createsuperuser

Reglas del equipo:

  -python manage.py runserver → siempre conecta a local, úsenlo libremente
  -Nunca corran comandos con $env:DJANGO_ENV="prod" sin avisar al equipo
  -Nunca suban .env.dev ni .env.prod a Git

6. Para cambiar bd solo usar:
$env:DJANGO_ENV="prod"
o para desarrollo:
$env:DJANGO_ENV="dev"

python manage.py migrate      # o cualquier comando


