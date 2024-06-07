 # Wagtail over Django and Postgres with Docker-Compose

## General architecture
TODO: expand this

In general we have a site: getting-started-site
with two apps, a wagtail app named "home", where the main site stems
and a django app named "external_db_app", used as an ORM map to create/edit/manage an external database.
The database routing is done through getting_started_site/settings/base.py and db_routers.py.

Command to start:
docker compose -f docker-compose-getting-started.yaml up -d
or visual studio Ctrl+Shift+p: Compose up (docker-compose-getting-started.yaml)
When the container are up,
run: 
docker exec -it \[django_directory\]-webapp-1 python3 django/getting_started_site/manage.py migrate
docker exec -it \[django_directory\]-webapp-1 python3 django/getting_started_site/manage.py createsuperuser
(add -d if you need to migrate on the fly)

and then:
1) with the debugger attached: Run and Debug: Python Debugger Remote Attach
2) by terminal: docker exec -it \[django_directory\]-webapp-1 python3 django/getting_started_site/manage.py runserver 0.0.0.0:8080
(add -d if you want to execute on background)

