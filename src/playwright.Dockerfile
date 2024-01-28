FROM python:3.11.6 as install-stage
# working directory in the container
WORKDIR /app
# Install python dependencies
RUN apt update
# Install mysql dependencies to prevent pip install errors (when using python:alpine images)
# RUN apk add gcc musl-dev mariadb-connector-c-dev
# Install bcrypt dependencies to prevent pip install errors (when using python:alpine images)
# RUN apk add libffi-dev
# # Install pipx for poetry - used to install Python CLI applications globally while still isolating them in virtual environments
RUN pip install pipx
RUN pipx ensurepath
# Install poetry
RUN pipx install poetry
ENV PATH="${PATH}:/root/.local/bin"
# Install playwright and browsers
RUN pipx install playwright
ENV PATH="${PATH}:/root/.local/pipx/venvs/playwright/bin"
RUN playwright install --with-deps
# copy dependency files and install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root
# Install playwright
RUN poetry run playwright install --with-deps
# copy code
COPY . .
# # Run playwright tests
FROM install-stage as playwright-stage
CMD ["poetry", "run", "pytest", "test/admin_app_e2e_tests"]
