docker volume create entrance_system_database_volume
docker build -t entrance_system_database .
docker run -d -p 11000:5432 -v entrance_system_database_volume:/var/lib/postgresql/data --name entrance_database entrance_system_database
