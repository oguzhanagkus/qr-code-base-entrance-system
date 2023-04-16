docker volume create pgadmin_volume
docker build -t pgadmin .
docker run -d -p 8000:80 -v pgadmin_volume:/var/lib/pgadmin --name pgadmin pgadmin
