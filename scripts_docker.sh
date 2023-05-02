#!/bin/sh
# docker_down_all_backend_containers() { docker-compose -f docker-compose.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.fastapi_localdb.yml -f compose-files/compose.full_app_proxy.yml -f compose-files/compose.cypress.yml -p backend down --rmi all; }
docker_down_all_backend_containers() { docker-compose -f docker-compose.yml -p backend down --rmi all -v --remove-orphans; }
build_backend_stack_docker_images() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend build; }
run_db_migrations() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi alembic upgrade head; }
create_admin_users() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi python main.py add_admin_user $1 $2; }

build_backend_stack_docker_images_localdb() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi_localdb.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend build; }
run_db_migrations_localdb() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi_localdb.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi alembic -c alembic.sqlite.ini upgrade head; }
create_admin_users_localdb() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi_localdb.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi python main.py add_admin_user $1 $2; }

case=${1:-default}
if [ $case = "launch-api-local" ]
then
   docker_down_all_backend_containers
   # Ensure app.log file is created otherwise docker creates app.log directory by default as it is mounted
   touch app.log
   # Define test admin users
   BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
   BACKEND_ADMIN_USER_PASSWORD="admin"
   # build backend stack images, run db migrations and create test admin users
   build_backend_stack_docker_images && run_db_migrations && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
   # Launch backend app & db
   export LOG_ENV_VARS_ON_APP_START=True
   docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend up
elif [ $case = "launch-fullstack-local" ]
then
   docker_down_all_backend_containers
   # Ensure app.log file is created otherwise docker creates app.log directory by default as it is mounted
   touch app.log
   # Define test admin users
   BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
   BACKEND_ADMIN_USER_PASSWORD="admin"
   # build backend stack images, run db migrations and create test admin users
   build_backend_stack_docker_images && run_db_migrations && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
   # Launch fullstack app and db
   docker-compose -f docker-compose.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend up --build
elif [ $case = "launch-fullstack-local-with-proxy" ]
then
   docker_down_all_backend_containers
   # Ensure app.log file is created otherwise docker creates app.log directory by default as it is mounted
   touch app.log
   # Define test admin users
   BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
   BACKEND_ADMIN_USER_PASSWORD="admin"
   # build backend stack images, run db migrations and create test admin users
   build_backend_stack_docker_images && run_db_migrations && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
   # set env vars
   # set auth cookie type for e2e docker tests
   export USER_AUTH_COOKIE_TYPE=same_site_not_secure
   export VITE_APP_BACKEND_URL=http://backend.login.com:8030
   export VITE_APP_BACKEND_WEBSOCKET_URL=ws://backend.login.com:8030/ws/main
   # launch app
   docker-compose -f docker-compose.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -f compose-files/compose.full_app_proxy.yml -p backend up --build
elif [ $case = "launch-tdd" ]
then
   docker_down_all_backend_containers
   # Ensure app.log file is created otherwise docker creates app.log directory by default as it is mounted
   touch app.log
   # Define test admin users
   BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
   BACKEND_ADMIN_USER_PASSWORD="admin"
   # build backend stack images, run db migrations and create test admin users
   build_backend_stack_docker_images && run_db_migrations && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
   # set test user credentials as env vars
   export TEST_ADMIN_USER_EMAIL=$BACKEND_ADMIN_USER_EMAIL
   export TEST_ADMIN_USER_PASSWORD=$BACKEND_ADMIN_USER_PASSWORD
   # Run tdd command on app container
   docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi ptw -- --testmon
elif [ $case = "run-api-tests" ]
then
   docker_down_all_backend_containers
   # Ensure app.log file is created otherwise docker creates app.log directory by default as it is mounted
   touch app.log
   touch app-tests.log
   # Define test admin users
   BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
   BACKEND_ADMIN_USER_PASSWORD="admin"
   # build backend stack images, run db migrations and create test admin users
   build_backend_stack_docker_images && run_db_migrations && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
   # set test user credentials as env vars
   export TEST_ADMIN_USER_EMAIL=$BACKEND_ADMIN_USER_EMAIL
   export TEST_ADMIN_USER_PASSWORD=$BACKEND_ADMIN_USER_PASSWORD
   # Run tdd command on app container
   docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi python -m pytest -n 3 --capture=no --alluredir='./test/allure-results'
elif [ $case = "run-api-tests-localdb" ]
then
   docker_down_all_backend_containers
   # Ensure app.log file is created otherwise docker creates app.log directory by default as it is mounted
   touch app.log
   touch app-tests.log
   # Define test admin users
   BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
   BACKEND_ADMIN_USER_PASSWORD="admin"
   # build backend stack images, run db migrations and create test admin users
   build_backend_stack_docker_images_localdb && run_db_migrations_localdb && create_admin_users_localdb $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
   # set test user credentials as env vars
   export TEST_ADMIN_USER_EMAIL=$BACKEND_ADMIN_USER_EMAIL
   export TEST_ADMIN_USER_PASSWORD=$BACKEND_ADMIN_USER_PASSWORD
   # Run tdd command on app container
   docker-compose -f docker-compose.yml -f compose-files/compose.fastapi_localdb.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi python -m pytest -n 3 --capture=no --alluredir='./test/allure-results'
elif [ $case = "run-e2e-tests-cypress" ]
then
   docker_down_all_backend_containers
   # create log file (used as docker volume) to prevent docker from creating a directory
   touch app.log
   # Define test admin users
   BACKEND_ADMIN_USER_EMAIL="test_admin@fakemail.com"
   BACKEND_ADMIN_USER_PASSWORD="secretpwd"
   # build backend stack images, run db migrations and create test admin users
   build_backend_stack_docker_images && run_db_migrations && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
   # Set env vars before building images
   # set vite build env vars
   export VITE_APP_BACKEND_URL=http://backend.full_app_proxy.com
   export VITE_APP_BACKEND_WEBSOCKET_URL=ws://backend.full_app_proxy.com/ws/main
   # set full app proxy env vars for nginx config for e2e test
   export NGINX_FILENAME=nginx-e2e-test.conf
   # build frontend and cypress containers
   docker-compose -f docker-compose.yml -f compose-files/compose.cypress.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -f compose-files/compose.full_app_proxy.yml -p backend build
   # set env vars for tests execution
   # set auth cookie type for e2e docker tests
   export USER_AUTH_COOKIE_TYPE=same_site_not_secure
   # set cypress env vars
   export CYPRESS_BASE_URL=http://frontend.full_app_proxy.com
   export CYPRESS_VIDEO=true
   # export CYPRESS_TAGS=@notes-feature
   export CYPRESS_VERIFY_TIMEOUT=100000 # Enable when running script locally and system is slow
   export CYPRESS_apiUrl=http://backend.full_app_proxy.com/api
   export CYPRESS_adminApiUrl=http://backend.full_app_proxy.com/api/admin
   export CYPRESS_adminApiLoginUsername=$BACKEND_ADMIN_USER_EMAIL
   export CYPRESS_adminApiLoginPassword=$BACKEND_ADMIN_USER_PASSWORD
   # export CYPRESS_TAGS=@tag1,@tag2 # example with multiple tags
   # run e2e tests
   docker-compose -f docker-compose.yml -f compose-files/compose.cypress.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -f compose-files/compose.full_app_proxy.yml -p backend run vueapp_test_e2e_cypress npm run test:e2e:dev:run:docker
elif [ $case = "run-e2e-tests-playwright" ]
then
   docker_down_all_backend_containers
   # create log file (used as docker volume) to prevent docker from creating a directory
   touch app.log
   # Define test admin users
   BACKEND_ADMIN_USER_EMAIL="test_admin@fakemail.com"
   BACKEND_ADMIN_USER_PASSWORD="secretpwd"
   # build backend stack images, run db migrations and create test admin users
   build_backend_stack_docker_images && run_db_migrations && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
   # Set env vars before building images
   # set vite build env vars
   export VITE_APP_BACKEND_URL=http://backend.full_app_proxy.com
   export VITE_APP_BACKEND_WEBSOCKET_URL=ws://backend.full_app_proxy.com/ws/main
   # set full app proxy env vars for nginx config for e2e test
   export NGINX_FILENAME=nginx-e2e-test.conf
   # build frontend and playwright containers
   docker-compose -f docker-compose.yml -f compose-files/compose.playwright.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -f compose-files/compose.full_app_proxy.yml -p backend build
   # set env vars for tests execution
   # set auth cookie type for e2e docker tests
   export USER_AUTH_COOKIE_TYPE=same_site_not_secure
   # set playwright env vars
   export PLAYWRIGHT_BASE_URL=http://frontend.full_app_proxy.com
   export PLAYWRIGHT_apiUrl=http://backend.full_app_proxy.com/api
   export PLAYWRIGHT_adminApiUrl=http://backend.full_app_proxy.com/api/admin
   export PLAYWRIGHT_adminApiLoginUsername=$BACKEND_ADMIN_USER_EMAIL
   export PLAYWRIGHT_adminApiLoginPassword=$BACKEND_ADMIN_USER_PASSWORD
   # run e2e tests
   docker-compose -f docker-compose.yml -f compose-files/compose.playwright.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -f compose-files/compose.full_app_proxy.yml -p backend run vueapp_test_e2e_playwright npm run test:e2e:playwright
elif [ $case = "launch-api-cloud-dev" ]
then
   docker_down_all_backend_containers
   # Ensure app.log file is created otherwise docker creates app.log directory by default as it is mounted
   touch app.log
   # Build containers & run db migrations
   build_backend_stack_docker_images && run_db_migrations
   # Launch backend app and db
   export CORS_ORIGINS_SET="Cloud-Development"
   export USER_AUTH_COOKIE_TYPE=cross_site_secure
   export ADMIN_USER_AUTH_COOKIE_TYPE=same_site_secure
   export PRIMARY_DOMAIN="login-example.duckdns.org"
   export RELOAD_APP_ON_CHANGE=True
   docker-compose -f docker-compose.yml -f docker-compose.override.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend up --build -d
elif [ $case = "launch-databases" ]
then
   docker_down_all_backend_containers
   docker-compose -f docker-compose.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend up --build
elif [ $case = "down" ]
then
   docker_down_all_backend_containers
else
   echo "no option passed"
   echo "available options are:
    - launch-api-local
    - launch-fullstack-local
    - launch-fullstack-local-with-proxy
    - launch-tdd
    - run-api-tests
    - run-e2e-tests
    - launch-api-cloud-dev
    - launch-databases
    - down
    "
fi