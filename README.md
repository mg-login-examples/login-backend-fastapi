
# About
This app is a demo login Api supporting the [frontend demo login app](https://github.com/mg-login-examples/login-frontend-vue). It is built using [FastAPI](https://fastapi.tiangolo.com/), a Python web framework.

### Features
- Docker (including for development with live reload)
- FastAPI Framework
- Interactive API Documentation
- Production ready Python web server using Uvicorn
- CORS (Cross Origin Resource Sharing)


## Requirements
**Docker Based**
- Docker

**Without Docker**
- Python3
- MySQL


<br/><br/> 

# Quickstart (Local Development)
## Docker Based
Ensure you have [docker](https://docs.docker.com/engine/install/) installed on your machine

- To **launch api** (accessible at htpp://localhost:8018): 
    - Build & Start containers and launch app with live reload:
        - ```docker compose -p backend --profile backend-serve up --build```
            - FastAPI interactive **API documentation** available at:
                - http://localhost:8018/docs
                - http://localhost:8018/redoc
    - Stop containers:
        - ```CTRL+C```
    - Delete containers:
        - ```docker compose -p backend --profile backend-serve down```
- To **run new/affected tests with live reload** for Test Driver Development:
    - Build & Start containers and run tests with live reload: 
        - ```docker compose -f docker-compose.test.yml -p backend --profile backend-test run fastapi_test ptw -- --testmon```
    - Build & Start containers and run Unit tests only with live reload: 
        - ```docker compose -f docker-compose.test.yml -p backend --profile backend-test run fastapi_test ptw -- --testmon test/unit_tests```
    - Stop containers:
        - ```CTRL+C```
    - Delete containers:
        - ```docker compose -p backend --profile backend-test down```
- To **run all Api tests**:
    - Build & Start containers and run all (unit + integration) pytest tests:
        - ```docker compose -f docker-compose.test.yml -p backend --profile backend-test up --build --abort-on-container-exit```
    - Stop containers:
        - ```CTRL+C```
    - Delete containers:
        - ```docker compose -p backend --profile backend-test down```
- To **run E2E fullstack tests** with frontend login app:
    - **PREREQUISITES**
        - Clone repo inside project directory: ```git clone https://github.com/mg-login-examples/login-frontend-vue.git```
    - Build & Start containers and run end-to-end cypress tests:
        - ```docker compose -f docker-compose.test.yml -p backend --profile fullstack-e2e-test up --build```
    - Stop containers:
        - ```CTRL+C```
    - Delete containers:
        - ```docker compose -p backend --profile fullstack-e2e-test down```
- To **launch fullstack app**:
    - **PREREQUISITES**
        - Clone repo inside project directory: ```git clone https://github.com/mg-login-examples/login-frontend-vue.git```
    - Start containers with live reload for frontend & backend:
        - ```docker compose -p backend --profile fullstack-serve up --build```
    - Stop containers:
        - ```CTRL+C```
    - Delete containers:
        - ```docker compose -p backend --profile fullstack-serve down```

## Without Docker
1. Install Python3
2. Navigate to code directory: ```cd src```
2. Install Python dependencies: ```pip install -r requirements.txt```
3. Launch App
    - without MySQL
        - **Launch app** (accessible at htpp://localhost:8018): 
            - ```uvicorn main:app --reload```
            - FastAPI interactive **API documentation** available at:
                - http://localhost:8018/docs
                - http://localhost:8018/redoc
        - Do **Test Driver Development** (Run tests locally with live reload):
            - ```ptw -- --testmon```
    - with MySQL
        - **Launch app** (accessible at htpp://localhost:8018): 
            - ```TODO```

# Advanced
## Logging
[Coloredlogs](https://pypi.org/project/coloredlogs/) is used for logging.
## CICD / Git Workflow
### Develop a new feature / Fix a bug
- 1. Fork a branch from *main*
- 2. Develop your feature / Fix the bug
- 3. Test your code locally
- 4. Create a pull request to merge your branch back to *main*
- 5. Merge the *feature* branch into *main*
### Release a new version
- 1. Create a pull request to merge your branch into *staging*
- 2. Merge *main* branch into *staging*
- 3. Create a pull request to merge your branch into *staging*
- 4. Merge *staging* branch into *master*

## Docker Setup
### Local Development
- Compose File: *docker-compose.dev.yml*
- Compose Services:
    - mysqldb
    - fastapi
        - Related dockerfile: *src/Dockerfile*
    - 
### Useful Docker commands:
- Build and start container: ```docker-compose -f docker-compose.dev.yml up```
- When updating docker-compose files:
    - ```docker-compose -f <docker-compose-file> down```
    - ```docker-compose -f <docker-compose-file> up```
- When running a command for a service:
    - ```docker-compose -f <docker-compose-file> -p <new-container-name> run <service-name> <command>```
    - Example: ```docker-compose -f docker-compose.dev.yml -p tests run fastapi pytest```


## Test Reports
- **Pytest test report:**
    - Docker based: ```docker-compose -f docker-compose.dev.yml -p tests run fastapi pytest --html=report.html --self-contained-html```
    - Without Docker: ```pytest --html=report.html --self-contained-html```
- **Code Coverage:**
    - 1. Measure code coverage:
        - Docker based: ```docker-compose -f docker-compose.dev.yml -p tests run fastapi coverage run -m pytest```
        - Without Docker: ```coverage run -m pytest```
    - 2. Generate html coverage report (from above measured coverage report):
        - Docker based: ```docker-compose -f docker-compose.dev.yml -p tests run fastapi coverage html```
        - Without Docker: ```coverage html```

