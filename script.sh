#!/bin/sh
case=${1:-default}
if [ $case = "launch-app-local" ]
then
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend-serve up --build
elif [ $case = "tdd" ]
then
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend-test run fastapi ptw -- --testmon
elif [ $case = "run-api-tests" ]
then
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend-test run fastapi pytest --alluredir='./test/allure-results'
elif [ $case = "launch-app" ]
then
   echo "Launching backend api & `mysql` container"
#    export DATABASE_URL="todo-for-prod"
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend --profile backend-serve up --build
else
   echo "no option passed"
   echo "available options are:
    - run-api-tests
    - run-fullstack-tests
    - launch-api
    "
fi