run_db_migrations() { poetry run alembic upgrade head; }
run_db_migrations_localdb() { poetry run alembic -c alembic.sqlite.ini upgrade head; }
create_admin_users() { poetry run python main.py add_admin_user $1 $2; }

case=${1:-default}
if [ $case = "launch-api-localdb" ]
then
    cd src
    # Define test admin users
    BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
    BACKEND_ADMIN_USER_PASSWORD="admin"
    # run db migrations and create test admin users
    run_db_migrations_localdb && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
    poetry run python main.py
elif [ $case = "launch-api-externaldb" ]
then
    cd src
    # Override localdb env vars
    export DATABASE_URL="${DATABASE_URL:-mysql://root@mysql_db/login}"
    export MONGO_HOST="${MONGO_HOST-mongo_db}"
    export MONGO_USERNAME="${MONGO_USERNAME:-root_user}"
    export USE_IN_MEMORY_MONGO_DB=False
    export ACCESS_TOKENS_STORE_TYPE="${ACCESS_TOKENS_STORE_TYPE:-redis}"
    export REDIS_URL="${REDIS_URL:-redis://redis_cache}"
    export CHECK_REDIS_CONNECTION_ON_APP_START=True
    export PUBSUB_URL="${PUBSUB_URL:-redis://redis_cache}"
    export CORS_ORIGINS_SET="${CORS_ORIGINS_SET:-Development}"
    export USER_AUTH_COOKIE_TYPE="${USER_AUTH_COOKIE_TYPE:-localhost_development}"
    export ADMIN_USER_AUTH_COOKIE_TYPE="${ADMIN_USER_AUTH_COOKIE_TYPE:-localhost_development}"
    # Define test admin users
    BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
    BACKEND_ADMIN_USER_PASSWORD="admin"
    # run db migrations and create test admin users
    run_db_migrations && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
    poetry run python main.py
elif [ $case = "lint-backend" ]
then
    cd backend
    poetry run mypy . --exclude 'alembic_sqlite/*' --exclude 'alembic/*'
elif [ $case = "run-api-tests" ]
then
    cd src
    # Define test admin users
    BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
    BACKEND_ADMIN_USER_PASSWORD="admin"
    # run db migrations and create test admin users
    run_db_migrations_localdb && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
    poetry run pytest test/integration_and_unit_tests
elif [ $case = "run-admin-app-tests" ]
then
    cd src
    # Define test admin users
    BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
    BACKEND_ADMIN_USER_PASSWORD="admin"
    # run db migrations and create test admin users
    run_db_migrations_localdb && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
    poetry run pytest test/admin_app_e2e_tests --alluredir='./test/allure-results'
else
   echo "no option passed"
   echo "available options are:
    - launch-api-local
    - launch-tdd
    - run-api-tests
    "
fi