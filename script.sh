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
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend run fastapi ptw -- --testmon
elif [ $case = "run-api-tests" ]
then
   # Stop all backend project's containers and build, start backend stack containers and run tests
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend run fastapi pytest --alluredir='./test/allure-results'
elif [ $case = "launch-app-dev-env" ]
then
   # Stop all backend project's containers and build and start backend stack containers for production
   echo "Launching backend api & `mysql` container"
#    export DATABASE_URL="todo-for-prod"
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend up --build -d
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