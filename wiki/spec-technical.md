# Technical Requirements

### Technical Decisions / Constraints
- Docker:
    - Using docker: Yes

- Database:
    - Database type: MySQL
    - Database for testing: SQLite for testing
- Database ORM Library: SQLAlchemy

- Backend Application
    - Language: Python
    - Web framework selected: FastAPI
        - Deploys with ASGI uvicorn server
    - SQL ORM Library: SQLAlchemy

**Write specs such that they are directly transferable as tests for TDD**
---
- Data Module
    - Role: Contains DB models & data schemas, and Db functions to manage data
    - Contents:
        - CRUD Utility Functions:
            - Role: Functions to Create, Read, Update and Delete resources from database. Serves as bridge between SQLAlchemy Models and Pydantic Schemas
            - Packages:
                - Base
                    - Role: Generic CRUD operations, directly uses SQLAlchemy functions
                    - Get resource object by id
                        -  **TODO** *Given resource's ORM Model and object id, return resource object*
                    - Get list of resource objects:
                        -  **TODO** *Given resource's ORM Model and skip number and limit number, return list of resource objects*
                    - Create resource object:
                        -  **TODO** *Given resource's ORM Model and object to create, create object and return it*
                    - Delete resource object by id
                        -  **TODO** *Given resource's ORM Model and object id, delete resource object*
                - Items
                    - Role: CRUD operations for Items resources. Uses CRUD Base's generic functions to perform db operations
                    - Get item by id
                        - **Done** *Given item id, call Base CRUD method: get_object and return its output*
                    - Get list of items:
                        - **Done** *Given skip number and limit number, call Base CRUD method: get_objects and return its output*
                    - Create item:
                        - **Done** *Given item to create, call Base CRUD method: create_object and return its output*
                    - Delete item by id
                        - **Done** *Given item id, call Base CRUD method: delete_object*
                - Users
                    - Role: CRUD operations for Users resources. Uses CRUD Base's generic functions to perform db operations
                    - Get user by id
                        - **Done** *Given user id, call Base CRUD method: get_object and return its output*
                    - Get list of users:
                        - **Done** *Given skip number and limit number, call Base CRUD method: get_objects and return its output*
                    - Create user:
                        - **Done** *Given user to create, call Base CRUD method: create_object and return its output*
                    - Delete user by id
                        - **Done** *Given user id, call Base CRUD method: delete_object*
                - User Items
                    - Get user items
                    - Add user item
                    - Remove user item
        - Schemas (using Pydantic)
            - Role: Serve as API response objects and easily convert to ORM Models
            - Schemas for items
                - itemBase
                - itemCreate
                - item
            - Schemas for users
                - userBase
                - userCreate
                - user
        - Database
            - Role: Contains modules related to Database 
            - ORM Models (using sqlAlchemy)
                - Role: Maps models to tables in the database
                - Models:
                    - item
                    - user
            - SQLAlchemy Database Manager
                - Role: Manages DB sessions
                - *On init, stores database url as an attribute*
                - *On init, creates SQLAlchemy engine and stores as an attribute*
                - *On init, creates SQLAlchemy Session class as an attribute*
                - *method db_session returns a new Session instance as a generator*
                - *method db_session closes session*
            - dbUtils
                - Role: Creates database tables based on Models
                - Note: To be replaced by Alembic

