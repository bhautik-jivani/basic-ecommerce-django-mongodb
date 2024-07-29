# E-Commerce App

## Objective

Using the DRF (Django Rest Framework), MongoDB (MongoEngine) and Docker, created scalable and reliable backend REST APIs for a ecmmerce platform that can support a wide range of users with different access levels.

## Installation

create an `.env.local` file in root directory of project

Inside `.env.local` have to mention below details:

```
MONGODB_HOST=db //docker service name
MONGODB_PORT=27017
MONGODB_DB=<your_db_name>
```
Run below code to start docker services
```
docker compose up -d
```
Create initial setup using below command

```
docker exec -it ecomm_backend bash -c "python manage.py createinitialsetup" 
```
Use attached postman collection to run apis

[Attachment](./postman_collection.json)