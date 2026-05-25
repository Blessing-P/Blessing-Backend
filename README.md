Configuración del entorno — Blessing Backend
El proyecto usa dos bases de datos separadas: una local para desarrollo y Neon (la nube) para producción.

Primera vez que clonan el proyecto:

1. Pedir los archivos .env.dev y .env.prod (no están en Git por seguridad)
2. Colocarlos en la raíz del proyecto, al mismo nivel que manage.py
3. Para desarrollo crear la BD local en PostgreSQL:
   CREATE DATABASE blessingdev;
   CREATE USER blessing_user WITH PASSWORD 'la_password_que_les_den';
   GRANT ALL PRIVILEGES ON DATABASE blessingdev TO blessing_user;
4. Actualizar 'DATABASE_URL' en el archivo .env.dev con la password y bd creada para trabajar localmente.
5. Aplicar migrations:
   python manage.py migrate
6. Crear su superusuario local:
   python manage.py createsuperuser

7. Para cambiar bd's solo usar:
   $env:DJANGO_ENV="prod" (Alojada en Neon)
   o para desarrollo:
   $env:DJANGO_ENV="dev" (Local)

python manage.py migrate # o cualquier comando

Reglas del equipo:

-python manage.py runserver → siempre conecta a local, úsenlo libremente
-Nunca corran comandos con $env:DJANGO_ENV="prod" sin avisar al equipo
-Nunca suban .env.dev ni .env.prod a Git

Nota:
$env:DJANGO_ENV solo controla a qué base de datos se conecta Django.
No afecta el código, los endpoints, ni dónde corre el servidor.

- Con "dev" → conecta a tu PostgreSQL local
- Con "prod" → conecta a Neon (la nube)
  El backend desplegado en Render tiene su propia configuración separada y no se ve afectado por este comando.
