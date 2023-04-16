docker volume create management_system_database_volume
docker build -t management_system_database .
docker run -d -p 12000:5432 -v management_system_database_volume:/var/lib/postgresql/data --name management_database management_system_database
