# Pull base image
# FROM python:3.10-alpine as install-stage
FROM python:3.11.6 as install-stage
# working directory in the container
WORKDIR /app
# Install mysql dependencies to prevent pip install errors (when using python:alpine images)
# RUN apk add gcc musl-dev mariadb-connector-c-dev
# Install bcrypt dependencies to prevent pip install errors (when using python:alpine images)
# RUN apk add libffi-dev
# Install pipx for poetry - used to install Python CLI applications globally while still isolating them in virtual environments
RUN pip install pipx
RUN pipx ensurepath
# Install poetry
RUN pipx install poetry
ENV PATH="${PATH}:/root/.local/bin"
# copy dependency files and install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root
# copy app code
COPY . .
# launch app stage
FROM install-stage as serve-stage
# expose app server port
EXPOSE $SERVER_PORT
# run app
CMD ["poetry", "run", "python", "main.py"]
# CMD ["tail", "-f", "/dev/null"]
