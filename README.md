## CowryWise Backend Assessment Test

You have been tasked to develop an application to manage books in a library. With your application, users can browse through the catalogue of books and borrow them. You are to build 2 independent API services for this application. 

1. Frontend API

  This API will be used to 

  * Enroll users into the library using their email, firstname and lastname.
  * List all available books
  * Get a single book by its ID
  * Filter books 
    * by publishers e.g Wiley, Apress, Manning 
    * by category e.g fiction, technology, science
  * Borrow books by id (specify how long you want it for in days)



2. Backend/Admin API

  This API will be used by an admin to:

  * Add new books to the catalogue
  * Remove a book from the catalogue.
  * Fetch / List users enrolled in the library.
  * Fetch/List users and the books they have borrowed
  * Fetch/List the books that are not available for borrowing (showing the day it will be available)



Requirements

* The endpoints need not be authenticated
* The API can be built using any python framework
* Design the models as you deem fit. 
* A book that has been lent out should no longer be available in the catalogue.
* The two services should use different data stores.
* Device a way to communicate changes between the two services. i.e when the admin adds a book to the catalogue via the admin api, the frontend api should also be updated with the latest book added by the admin.
* The project should be deployed using docker containers
* Add necessary unit/integration tests.


## Thought Process
* From the requirements there should be two independent services with different data storage but persisted data between the two services, so from this all I can think of is building a distributed system with interservice communication to persist data between the two services, which then yield my second thought for communication between the two systems.

## Implementation of the thought process
Since it's clear I'm building microservices with  interservice communication, 
I built the independent service A and service B independently using `django and DRF` just wanted to stay within the atmosphere you know what I mean, and the requirement was to use just python and any of it web framework.
Implement the interservice communication using `EDA` *Event Driven Architecture*, which was implemented leveraging `Redis PubSub` and `Docker Network`

## Event Architecture Flow
User Enrolls to the system through the Service A, Service A then emits an event with the user enrollment data to service B so as to also persist the new user in it storage. Same for other actions that has to be persisted in the two services store.
Yeah, that's the design.

## Getting Started To Test
Since `docker` and `docker compose` are used no need for the bulky configuration I did, so just do all these:
- Clone the repository
- Open three terminals in your workspace
    - Terminal 1 for the two services running simultaneously with all their dependent services
        - Run with `make run-library`
    - Terminal 2 for service A  event consumer service
        - Run with `make frontend_consumer`
    - Terminal 3 for service B event consumer service
        - Run with `make admin-consumer`
- Admin service will be serving at port `8300`
- Frontend service will be serving at port `8400`

## Other Technical Steps
Since the service are all running on a private and internal docker networks, you might need to run django migrations from inside the docker container
- Run `docker exec -it admin_service sh` to enter the admin service container
- Run `docker exec -it frontend_service sh` to enter the frontend service container
- Run `docker exec -it postgres_service sh` to enter the postgres service container

## Just Incase
If you need to connect the postgres container instance to your Database Editor or Explorer use the `localhost` as the host and `5433` as the port and `admin` as the user and `password` as the password or run the `psql -U admin -d postgres` from inside the postgres container

## Seed The Category table for the two services

```sql
INSERT INTO api_category VALUES
(1, 'Fiction'),(2, 'Non-Fiction'),(3, 'Drama'),(4, 'Biographies');
```

## Test the independent service
### Admin service
```sh
cd admin_api
pytest
```

### Frontend service
```sh
cd frontend_api
pytest
```