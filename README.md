
# Intro
This app is a demo login Api supporting the frontend demo login app. It is built using FastAPI, a Python web framework.

# Features
- Docker (including for development with live reload)
- FastAPI Framework
- Interactive API Documentation
- Production ready Python web server using Uvicorn
- CORS (Cross Origin Resource Sharing)


# Requirements
## Docker Based
Docker
## Without Docker
Python3


# Quickstart (Local Development)
## Docker Based
1. Launch app: 
    - ```docker compose -p backend --profile backend-serve up --build```
        - App base url: htpp://localhost:8018
        - FastAPI interactive **API documentation** available at:
            - http://localhost:8018/docs
            - http://localhost:8018/redoc
2. To do *Test Driver Development* (run new tests or tests relevant to new code with live reload):
    - ```docker compose -p backend --profile backend-test run fastapi_test ptw -- --testmon```
2. To run all API tests:
    - ```docker compose -p backend --profile backend-test up --build --abort-on-container-exit```
3. To run E2E tests with frontend login app:
    - 1. Clone repo inside project directory: ```git clone https://github.com/mg-login-examples/login-frontend-vue.git```
    - 2. Run fullstack E2E tests: ```docker compose -p backend --profile fullstack-e2e-test up --build```
4. To run fullstack app: ```docker compose -p backend --profile fullstack-serve up --build```

## Without Docker
1. Install Python3
2. Navigate to code directory: ```cd src```
2. Install Python dependencies: ```pip install -r requirements.txt```
3. 
    - Launch app: ```uvicorn main:app --reload```
        - App base url: htpp://localhost:8000
        - FastAPI interactive **API documentation** available at:
            - http://localhost:8000/docs
            - http://localhost:8000/redoc
    - Run tests locally with live reload: ```ptw -- --testmon```

# Advanced
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

