#!/bin/sh
docker_down_all_containers() { docker-compose -f docker-compose.yml -p backend down --rmi all -v --remove-orphans; }
build_backend_stack_docker_images() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend build; }
run_db_migrations() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi poetry run alembic upgrade head; }
create_admin_users() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi poetry run python main.py add_admin_user $1 $2; }

build_backend_stack_docker_images_localdb() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi_localdb.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend build; }
run_db_migrations_localdb() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi_localdb.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi poetry run alembic -c alembic.sqlite.ini upgrade head; }
create_admin_users_localdb() { docker-compose -f docker-compose.yml -f compose-files/compose.fastapi_localdb.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend run fastapi poetry run python main.py add_admin_user $1 $2; }

setup_backend() {
  docker_down_all_containers
  # Ensure app.log file is created otherwise docker creates app.log directory by default as it is mounted
  touch app.log
  touch app-tests.log
  # build backend stack images, run db migrations and create test admin users
  build_backend_stack_docker_images && run_db_migrations && create_admin_users $1 $2
}

case=${1:-default}
if [ $case = "launch-app-local" ]
then
  # Define test admin users
  BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
  BACKEND_ADMIN_USER_PASSWORD="admin"
  setup_backend $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
  # Launch fullstack app and db
  export LOG_ENV_VARS_ON_APP_START=True
  FINAL_COMMAND=${2:-'up --build'}
  docker-compose -f docker-compose.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend $FINAL_COMMAND
elif [ $case = "launch-app-local-with-proxy" ]
then
  # Define test admin users
  BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
  BACKEND_ADMIN_USER_PASSWORD="admin"
  setup_backend $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
  # set env vars
  # set auth cookie type for e2e docker tests
  export USER_AUTH_COOKIE_TYPE=same_site_not_secure
  export LOG_ENV_VARS_ON_APP_START=True
  export VITE_APP_BACKEND_URL=http://backend.login.com:8030
  export VITE_APP_BACKEND_WEBSOCKET_URL=ws://backend.login.com:8030/ws/main
  # launch app
  FINAL_COMMAND=${2:-'up --build'}
  docker-compose -f docker-compose.yml -f compose-files/compose.full_app_proxy.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend $FINAL_COMMAND
elif [ $case = "backend" ]
then
  # Define test admin users
  BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
  BACKEND_ADMIN_USER_PASSWORD="admin"
  setup_backend $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
  # set test user credentials as env vars
  export TEST_ADMIN_USER_EMAIL=$BACKEND_ADMIN_USER_EMAIL
  export TEST_ADMIN_USER_PASSWORD=$BACKEND_ADMIN_USER_PASSWORD
  ADD_PLAYWRIGHT_CONTAINER=""
  # determine final_command based on user input
  test_case=${2:-launch}
  if [ $test_case = "launch" ]
  then
    export LOG_ENV_VARS_ON_APP_START=True
    FINAL_COMMAND="up"
  elif [ $test_case = "api-tests" ]
  then
    FINAL_COMMAND="run fastapi poetry run pytest test/integration_and_unit_tests/ -n 3 --capture=no --alluredir=test/allure-results"
  elif [ $test_case = "tdd" ]
  then
    FINAL_COMMAND="run fastapi poetry run ptw test/integration_and_unit_tests/ -- -- --testmon"
  elif [ $test_case = "admin-app-tests" ]
  then
    # remove existing containers, otherwise error "dependency failed to start: container backend-fastapi-run-xxx exited (0)"
    docker_down_all_containers
    export PLAYWRIGHT_APP_BASE_URL="http://backend:8018"
    ADD_PLAYWRIGHT_CONTAINER="-f compose-files/compose.pytest_playwright.yml"
    FINAL_COMMAND="run pytest_playwright poetry run pytest test/admin_app_e2e_tests --alluredir=test/allure-results"
  elif [ $test_case = "type-check" ]
  then
    FINAL_COMMAND="run fastapi poetry run mypy . --exclude alembic_sqlite/* --exclude alembic/* --check-untyped-defs"
  elif [ $test_case = "format-check" ]
  then
    FINAL_COMMAND="run fastapi poetry run black . --check --diff --color"
  elif [ $test_case = "custom" ]
  then
    FINAL_COMMAND=${3}
  else
    echo "Unknown option passed for backend <option>
      <option> one of: launch, api-tests, tdd, admin-app-tests, type-check, format-check, custom <your_custom_command>
    "
    exit 1
  fi
  docker-compose -f docker-compose.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml $ADD_PLAYWRIGHT_CONTAINER -p backend $FINAL_COMMAND
elif [ $case = "backend-localdb" ]
then
  docker_down_all_containers
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
  ADD_PLAYWRIGHT_CONTAINER=""
  # determine final_command based on user input
  test_case=${2:-launch}
  if [ $test_case = "launch" ]
  then
    export LOG_ENV_VARS_ON_APP_START=True
    FINAL_COMMAND="up"
  elif [ $test_case = "api-tests" ]
  then
    FINAL_COMMAND="run fastapi poetry run pytest test/integration_and_unit_tests/ -n 3 --capture=no --alluredir=test/allure-results"
  elif [ $test_case = "tdd" ]
  then
    FINAL_COMMAND="run fastapi poetry run ptw test/integration_and_unit_tests/ -- -- --testmon"
  elif [ $test_case = "admin-app-tests" ]
  then
    # remove existing containers, otherwise error "dependency failed to start: container backend-fastapi-run-xxx exited (0)"
    docker_down_all_containers
    export PLAYWRIGHT_APP_BASE_URL="http://backend:8018"
    ADD_PLAYWRIGHT_CONTAINER="-f compose-files/compose.pytest_playwright.yml"
    FINAL_COMMAND="run pytest_playwright poetry run pytest test/admin_app_e2e_tests --alluredir=test/allure-results"
  elif [ $test_case = "type-check" ]
  then
    FINAL_COMMAND="run fastapi poetry run mypy . --exclude alembic_sqlite/* --exclude alembic/* --check-untyped-defs"
  elif [ $test_case = "format-check" ]
  then
    FINAL_COMMAND="run fastapi poetry run black . --check --diff --color"
  elif [ $test_case = "custom" ]
  then
    FINAL_COMMAND=${3}
  else
    echo "Unknown option passed for backend-localdb <option>
      <option> one of: launch, api-tests, tdd, admin-app-tests, type-check, format-check, custom <your_custom_command>
    "
    exit 1
   fi
   # Run tdd command on app container
   docker-compose -f docker-compose.yml -f compose-files/compose.fastapi_localdb.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml $ADD_PLAYWRIGHT_CONTAINER -p backend $FINAL_COMMAND
elif [ $case = "run-e2e-tests-cypress" ]
then
  BACKEND_ADMIN_USER_EMAIL="test_admin@fakemail.com"
  BACKEND_ADMIN_USER_PASSWORD="secretpwd"
  setup_backend $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
  # remove existing containers, otherwise error "dependency failed to start: container backend-fastapi-run-xxx exited (0)"
  docker_down_all_containers
  # Set env vars
  export LOG_ENV_VARS_ON_APP_START=True
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
  # run e2e cypress tests
  docker-compose -f docker-compose.yml -f compose-files/compose.cypress.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -f compose-files/compose.full_app_proxy.yml -p backend run vueapp_test_e2e_cypress npm run test-e2e-cypress
elif [ $case = "run-e2e-tests-playwright" ]
then
  BACKEND_ADMIN_USER_EMAIL="test_admin@fakemail.com"
  BACKEND_ADMIN_USER_PASSWORD="secretpwd"
  setup_backend $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
  # remove existing containers, otherwise error "dependency failed to start: container backend-fastapi-run-xxx exited (0)"
  docker_down_all_containers
  # Set env vars
  export LOG_ENV_VARS_ON_APP_START=True
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
  # run e2e playwright tests
  docker-compose -f docker-compose.yml -f compose-files/compose.playwright.yml -f compose-files/compose.vueapp_compiled.yml -f compose-files/compose.fastapi.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -f compose-files/compose.full_app_proxy.yml -p backend run vueapp_test_e2e_playwright npm run test-e2e-playwright
elif [ $case = "launch-api-cloud-dev" ]
then
   docker_down_all_containers
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
  docker_down_all_containers
  docker-compose -f docker-compose.yml -f compose-files/compose.mysql.yml -f compose-files/compose.mongo.yml -f compose-files/compose.redis.yml -p backend up --build
elif [ $case = "down" ]
then
  docker_down_all_containers
else
  echo "no option or invalid option passed"
  echo "available options are:
    - launch-backend-local
    - launch-app-local
    - launch-app-local-with-proxy
    - backend <option>
      <option> one of: launch, api-tests, tdd, admin-app-tests, type-check, format-check, custom <your_custom_command>
    - backend-localdb <option>
      <option> one of: launch, api-tests, tdd, admin-app-tests, type-check, format-check, custom <your_custom_command>

    - run-api-tests
    - run-api-tests-localdb
    - run-admin-app-e2e-tests
    - run-e2e-tests-cypress
    - run-e2e-tests-playwright
    - launch-api-cloud-dev
    - launch-databases
    - down
  "
fi