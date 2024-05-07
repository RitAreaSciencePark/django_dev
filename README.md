 # Wagtail over Django and Postgres with Docker-Compose

## General architecture
```
.
├── **docker-compose-getting-started.yaml**
├── **requirements.txt**
└── django (webapp)
    ├── django
    ├── docs
    ├── extras
    ├── **getting_started_site**
    │   ├── **manage.py**
    │   ├── getting_started_site
    │   │   └── settings
    │   │       └── **base.py**
    │   ├── home
    │   ├── media
    │   └── search
    ├── js_tests
    ├── scripts
    └── tests
```        
Command to start:
docker compose -f docker-compose-getting-started.yaml up -d
or visual studio Ctrl+Shift+p: Compose up (docker-compose-getting-started.yaml)
When the container are up,
1) with the debugger attached: Run and Debug: Puthon Debugger Remote Attach
2) by terminal: docker exec -itd \[django_directory\]-webapp-1 python3 django/getting_started_site/manage.py runserver 0.0.0.0:8080
