#!bin/bash
# Safe Backup
# TODO put some ifs, catch some exception and sprinkle some pizazz through the code
timestamp="$(echo $(date) | awk '{
    split($0,t,/[ :]/);
    month = (index("JanFebMarAprMayJunJulAugSepOctNovDec",t[2])+2)/3;
    printf("%s%02d%02d%s%s%s",t[8],month,t[3],t[4],t[5],t[6])
}')"
printf "Backup creation..."
docker exec -w /app/django/easyDMP django_dev-webapp-1 python3 manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > backups/backup_dump_$timestamp.json
printf "Done - File: backups/backup_dump_$timestamp.json created.\n"
docker exec -w /app/django/easyDMP django_dev-webapp-1 python3 manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --database prpmetadata-db --indent 2 > backups/backup_dump_decos_metadata_$timestamp.json


printf "Resetting databases..."
# RESET the DATABASE
docker exec django_dev-db-1 dropdb -U easydmp 'easydmp_main' -f
docker exec django_dev-db-1 dropdb -U easydmp 'decos_metadata_db' -f
docker exec django_dev-db-1 createdb -U easydmp 'easydmp_main'
docker exec django_dev-db-1 createdb -U easydmp 'decos_metadata_db'
printf "Done.\n"

printf "Initial Migration..."
# Initial Migrate
docker exec -w /app/django/easyDMP django_dev-webapp-1 python3 manage.py migrate
docker exec -w /app/django/easyDMP django_dev-webapp-1 python3 manage.py migrate --database prpmetadata-db
printf "Inital Migration Done."

echo "Deleting Wagtail welcome page..."
# DELETE welcome page in WAGTAIL (if django native is not necessary)
docker exec django_dev-db-1 psql -U easydmp 'easydmp_main' -c 'DELETE FROM wagtailcore_site;'
docker exec django_dev-db-1 psql -U easydmp 'easydmp_main' -c 'DELETE FROM wagtailcore_page WHERE id = 2;'
echo "Delete Done."

echo "Loading easydmp database..."
# LOAD database
ls -oht backups/
echo "insert the name of the database to restore (without .json):"
read database_name
docker exec -w /app/django/easyDMP django_dev-webapp-1 python3 manage.py loaddata /app/backups/$database_name.json
# docker exec -w /app/django/easyDMP django_dev-webapp-1 python3 manage.py migrate
echo "Loading database Done."

echo "Loading decos metadata database..."
# LOAD database
ls -oht backups/
echo "insert the name of the database to restore (without .json):"
read database_name
docker exec -w /app/django/easyDMP django_dev-webapp-1 python3 manage.py loaddata --database prpmetadata-db /app/backups/$database_name.json
# docker exec -w /app/django/easyDMP django_dev-webapp-1 python3 manage.py migrate
echo "Loading database Done."