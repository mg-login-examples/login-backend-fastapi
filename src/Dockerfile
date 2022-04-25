# Pull base image
FROM python:3.9-alpine as install-stage
# working directory in the container
WORKDIR /app
# copy dependency file and install dependencies
COPY requirements.txt .
# Install mysql dependencies to prevent pip install errors
RUN apk add gcc musl-dev mariadb-connector-c-dev
# Install bcrypt dependencies to prevent pip install errors
RUN apk add libffi-dev
RUN pip install -r requirements.txt
# copy code
COPY . .

# launch app stage
FROM install-stage as serve-stage
# expose app server port
EXPOSE $SERVER_PORT
CMD ["python", "main.py"]
# CMD ["pytest", "--alluredir='./test/allure-results'"]
# CMD ["ptw", "--", "--testmon"]
