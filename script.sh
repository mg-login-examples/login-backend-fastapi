#!/bin/sh
case=${1:-default}
if [ $case = "launch-app-local" ]
then
   # Stop all backend project's containers and build and start backend stack containers
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend up --build
elif [ $case = "tdd" ]
then
   # Stop all backend project's containers and build, start backend stack containers and run tests with watch
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend build
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend run fastapi ptw -- --testmon
elif [ $case = "run-api-tests" ]
then
   # Stop all backend project's containers and build, start backend stack containers and run tests
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend build
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend run fastapi python main.py create_db_tables
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend run fastapi python main.py add_admin_user test_admin@fakemail.com secretpwd
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend run fastapi python -m pytest --alluredir='./test/allure-results'
elif [ $case = "launch-app-dev-env" ]
then
   # Stop all backend project's containers and build and start backend stack containers for production
   echo "Launching backend api & `mysql` container"
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend down
   export CORS_ORIGINS_SET="Cloud-Development"
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend up --build -d
elif [ $case = "launch-fullstack-local" ]
then
   # Stop all backend project's containers and build and start full stack
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend --profile fullstack up --build
elif [ $case = "run-e2e-tests" ]
then
   # Stop all backend project's containers
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend --profile fullstack-e2e build
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile fullstack-e2e run fastapi python main.py create_db_tables
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile fullstack-e2e run fastapi python main.py add_admin_user test_admin@fakemail.com secretpwd
   export CYPRESS_ENV_FILE=.env_cypress.ci_e2e
   export CYPRESS_VIDEO=false
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend --profile fullstack-e2e run vueapp_test_e2e npm run test:e2e -- --headless --mode ci_e2e
elif [ $case = "stop" ]
then
   # Stop all backend project's containers
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend down
else
   echo "no option passed"
   echo "available options are:
    - run-api-tests
    - run-fullstack-tests
    - launch-api
    "
fi