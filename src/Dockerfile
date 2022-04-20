# Pull base image
FROM python:3.9-alpine as install-stage
# working directory in the container
WORKDIR /app
# copy dependency file and install dependencies
COPY requirements.txt .
RUN apk add gcc musl-dev mariadb-connector-c-dev
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
