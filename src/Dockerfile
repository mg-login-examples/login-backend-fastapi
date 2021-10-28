# Pull base image
FROM python:3.9 as install-stage
# working directory in the container
WORKDIR /app
# copy dependency file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
# copy code
COPY . .
# expose port
EXPOSE 8018

# test
FROM install-stage as test-stage
CMD ["pytest"]

# test
FROM install-stage as test-stage-live
CMD ["ptw", "--", "--testmon"]

# launch app
FROM install-stage as serve-stage
CMD ["python", "main.py"]