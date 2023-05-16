run_db_migrations() { alembic upgrade head; }
run_db_migrations_localdb() { alembic -c alembic.sqlite.ini upgrade head; }
create_admin_users() { python main.py add_admin_user $1 $2; }

case=${1:-default}
if [ $case = "launch-api-localdb" ]
then
    cd src
    # Define test admin users
    BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
    BACKEND_ADMIN_USER_PASSWORD="admin"
    # run db migrations and create test admin users
    run_db_migrations_localdb && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
    python main.py
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
    export TEST_REDIS_CONNECTION_ON_APP_START=True
    export PUBSUB_URL="${PUBSUB_URL:-redis://redis_cache}"
    export CORS_ORIGINS_SET="${CORS_ORIGINS_SET:-Development}"
    export USER_AUTH_COOKIE_TYPE="${USER_AUTH_COOKIE_TYPE:-localhost_development}"
    export ADMIN_USER_AUTH_COOKIE_TYPE="${ADMIN_USER_AUTH_COOKIE_TYPE:-localhost_development}"
    # Define test admin users
    BACKEND_ADMIN_USER_EMAIL="admin@admin.admin"
    BACKEND_ADMIN_USER_PASSWORD="admin"
    # run db migrations and create test admin users
    run_db_migrations && create_admin_users $BACKEND_ADMIN_USER_EMAIL $BACKEND_ADMIN_USER_PASSWORD
    python main.py
else
   echo "no option passed"
   echo "available options are:
    - launch-api-local
    - launch-tdd
    - run-api-tests
    "
fi