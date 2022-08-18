#!/bin/sh
case=${1:-default}
if [ $case = "launch-api-local" ]
then
   # Stop all backend project's containers and build and start backend stack containers
   docker-compose -f docker-compose.yml -f compose.vueapp.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend up --build
elif [ $case = "launch-fullstack-local" ]
then
   # Stop all backend project's containers and build and start fullstack containers
   docker-compose -f docker-compose.yml -f compose.vueapp.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend up --build
elif [ $case = "launch-tdd" ]
then
   # Stop all backend project's containers and build, start backend stack containers and run tests with watch
   docker-compose -f docker-compose.yml -f compose.vueapp.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend build
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend run fastapi ptw -- --testmon
elif [ $case = "run-api-tests" ]
then
   # Stop all backend project's containers and build, start backend stack containers and run tests
   docker-compose -f docker-compose.yml -f compose.vueapp.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend build
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend run fastapi alembic upgrade head
   export TEST_ADMIN_USER_EMAIL="test_admin@fakemail.com"
   export TEST_ADMIN_USER_PASSWORD="secretpwd"
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend run fastapi python main.py add_admin_user $TEST_ADMIN_USER_EMAIL $TEST_ADMIN_USER_PASSWORD
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend run fastapi python -m pytest --alluredir='./test/allure-results'
elif [ $case = "launch-api-cloud-dev" ]
then
   # Stop all backend project's containers and build and start backend stack containers for production
   echo "Launching backend api & `mysql` container"
   docker-compose -f docker-compose.yml -f compose.vueapp.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend down
   export CORS_ORIGINS_SET="Cloud-Development"
   export SECURE_COOKIES=True
   export SAMESITE=none
   export PRIMARY_DOMAIN="login-example.duckdns.org"
   docker-compose -f docker-compose.yml -f docker-compose.override.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend up --build -d
elif [ $case = "launch-fullstack-local" ]
then
   # Stop all backend project's containers and build and start full stack
   docker-compose -f docker-compose.yml -f compose.vueapp.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vueapp.yml -p backend up --build
elif [ $case = "run-e2e-tests" ]
then
   # Stop all backend project's containers
   docker-compose -f docker-compose.yml -f compose.vueapp.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend down
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend build
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend run fastapi alembic upgrade head
   export BACKEND_ADMIN_USER_EMAIL="test_admin@fakemail.com"
   export BACKEND_ADMIN_USER_PASSWORD="secretpwd"
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -p backend run fastapi python main.py add_admin_user $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
   export CYPRESS_ENV_FILE=.env_cypress.ci_e2e
   export CYPRESS_VIDEO=true
   export CYPRESS_MAILSLURP_API_KEY=$CYPRESS_MAILSLURP_API_KEY
   export CYPRESS_ADMIN_API_LOGIN_USERNAME=$BACKEND_ADMIN_USER_EMAIL
   export CYPRESS_ADMIN_API_LOGIN_PASSWORD=$BACKEND_ADMIN_USER_PASSWORD
   # export CYPRESS_TAGS=@tag1,@tag2
   export SAMESITE=none
   docker-compose -f docker-compose.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend run vueapp_test_e2e npm run test:e2e -- --headless --mode ci_e2e --browser chrome
elif [ $case = "down" ]
then
   # Stop all backend project's containers
   docker-compose -f docker-compose.yml -f compose.vueapp.yml -f compose.fastapi.yml -f compose.mysql.yml -f compose.vuecypress.yml -p backend down
else
   echo "no option passed"
   echo "available options are:
    - launch-api-local
    - launch-tdd
    - run-api-tests
    - launch-api-cloud-dev
    - launch-fullstack-local
    - run-e2e-tests
    - down
    "
fi