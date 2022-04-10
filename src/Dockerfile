# Pull base image
FROM python:3.9-alpine as install-stage
# working directory in the container
WORKDIR /app
# copy dependency file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
# copy code
COPY . .

# test state
FROM install-stage as test-stage
CMD ["pytest"]

# test allure docker state
FROM install-stage as test-allure-stage
CMD ["pytest", "--alluredir='../../allure-docker/projects/backend/results'"]

# test with live reload stage
FROM install-stage as test-live-reload-stage
CMD ["ptw", "--", "--testmon"]

# launch app stage
FROM install-stage as serve-stage
# expose app server port
EXPOSE $SERVER_PORT
CMD ["python", "main.py"]