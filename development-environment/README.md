# Development Environment

This directory describes the development environment that is used during this project.

## General
- I use Linux systems for my development processes. For this project, I used **Ubuntu 20.04**.

- I prefer using **JetBrains PyCharm IDE** for Python projects. 
The community edition can be downloaded from the official website or Snap store.
[musaade-management-system](https://github.com/oguzhanagkus/musaade-management-system) and
[musaade-entrance-system](https://github.com/oguzhanagkus/musaade-entrance-system) projects are PyCharm projects.
They can be opened directly by IDE. I will add the requirement files for the virtual environments when projects are completed.
No additional settings are required.

- I prefer **Flutter SDK** for the mobile application. I just followed [official installation documentation](https://flutter.dev/docs/get-started/install/linux).

## Database
- I prefer **Docker** for databases (PostgreSQL).
I just followed [official installation documentation](https://docs.docker.com/engine/install/ubuntu).
Also, I need to install [Docker Compose](https://docs.docker.com/compose/install).

- I set up databases as Docker containers. For Entrance System and Management system I have separate directories.
Corresponding directories have a Dockerfile and a run script. Follow them to up these containers.

- If you want to use, pgAdmin for managing and viewing your database, you can use Dockerfile in pgadmin directory.
Since these containers only communicate over host device, you should use your device's IP and corresponding port to add servers to pgAdmin panel.

- Also, you should change default username and password in Dockerfiles.

## HES System
- Since, using the government HES Code System requires some official procedures, I decided to implement my own HES system.

- It is simple API which gets code data and returns health status of code's owner.

- This service runs on Docker too. For development and production environments, I have different docker-compose files.
You can use appropriate one in for your purposes.

- You need to get a token for making queries. Just got to /get_token path of service. Enter your username. Password is "get_token".

- After getting token, you should at this token to header while asking for a HES code.

- Do not forget to set your own secret keys, authentication info, SSL certificates. They are just placeholders.

- In production, you should migrate and fill the database manually.
  - Run shell in container: **docker exec -it hes_api bash**
  - Run command for migration: **python manage.py create_db**
  - Run command for junk entries: **python manage.py fill_db**
  - Creating self-signed SSL certificates:
    - sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ~/hes-self-signed.key -out ~/keys/hes-self-signed.crt
    - Put them in /hes_system/services/server/certs directory

## Data Generator
- The person datas (names and national IDs) are generated randomly. They are not real and official.

- I use this [repository](https://github.com/mkozturk/turkishnames) to generate random names.
