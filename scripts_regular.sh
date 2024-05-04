#!/bin/sh

backend_options="<option> one of: launch, api-tests, tdd, admin-app-tests, type-check, format-check, format-all, custom <your_custom_command>"
backend_localbdb_options="<option> one of: launch, api-tests, tdd, admin-app-tests, type-check, format-check, format-all, custom <your_custom_command>"

case=${1:-default}
if [ $case = "backend" ]
then
  cd src
  poetry run alembic upgrade head
  poetry run python main.py add_admin_user admin@admin.admin admin
  # determine final_command based on user input
  test_case=${2:-launch}
  if [ $test_case = "launch" ]
  then
    FINAL_COMMAND="python main.py"
  elif [ $test_case = "api-tests" ]
  then
    FINAL_COMMAND="poetry run pytest test/integration_and_unit_tests/ -n 8 --capture=no --alluredir=test/allure-results"
  elif [ $test_case = "tdd" ]
  then
    FINAL_COMMAND="poetry run ptw test/integration_and_unit_tests/ -- -- --testmon"
  elif [ $test_case = "admin-app-tests" ]
  then
    FINAL_COMMAND="poetry run pytest test/admin_app_e2e_tests --alluredir=test/allure-results"
  elif [ $test_case = "type-check" ]
  then
    FINAL_COMMAND="poetry run mypy . --exclude alembic_sqlite/ --exclude alembic/ --check-untyped-defs"
  elif [ $test_case = "format-check" ]
  then
    FINAL_COMMAND="poetry run black . --check --diff --color"
  elif [ $test_case = "format-all" ]
  then
    FINAL_COMMAND="poetry run black ."
  elif [ $test_case = "custom" ]
  then
    FINAL_COMMAND=${3}
  else
    echo "Unknown option passed for backend <option>
    $backend_options
    "
    exit 1
  fi
  $FINAL_COMMAND
elif [ $case = "backend-localdb" ]
then
  cd src
  poetry run alembic -c alembic.sqlite.ini upgrade head
  poetry run python main.py add_admin_user admin@admin.admin admin
  # determine final_command based on user input
  test_case=${2:-launch}
  if [ $test_case = "launch" ]
  then
    FINAL_COMMAND="python main.py"
  elif [ $test_case = "api-tests" ]
  then
    FINAL_COMMAND="poetry run pytest test/integration_and_unit_tests/ -n 10 --capture=no --alluredir=test/allure-results"
  elif [ $test_case = "tdd" ]
  then
    FINAL_COMMAND="poetry run ptw test/integration_and_unit_tests/ -- -- --testmon"
  elif [ $test_case = "admin-app-tests" ]
  then
    FINAL_COMMAND="poetry run pytest test/admin_app_e2e_tests --alluredir=test/allure-results"
  elif [ $test_case = "type-check" ]
  then
    FINAL_COMMAND="poetry run mypy . --exclude alembic_sqlite/ --exclude alembic/ --check-untyped-defs"
  elif [ $test_case = "format-check" ]
  then
    FINAL_COMMAND="poetry run black . --check --diff --color"
  elif [ $test_case = "format-all" ]
  then
    FINAL_COMMAND="poetry run black ."
  elif [ $test_case = "custom" ]
  then
    FINAL_COMMAND=${3}
  else
    echo "Unknown option passed for backend-localdb <option>
    $backend_localdb_options
    "
    exit 1
  fi
  $FINAL_COMMAND
else
  echo "no option passed"
  echo "available options are:
  - backend <option>
    $backend_options
  - backend-localdb <option>
    $backend_localdb_options
  "
fi