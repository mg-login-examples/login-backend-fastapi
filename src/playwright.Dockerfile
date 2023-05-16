FROM mcr.microsoft.com/playwright/python:v1.33.0-jammy as install-stage
# working directory in the container
WORKDIR /app
# copy dependency file and install dependencies
COPY requirements.playwright.txt .
# Install bcrypt dependencies to prevent pip install errors (when using python:alpine images)
# RUN apk add libffi-dev
RUN pip install -r requirements.playwright.txt
# copy code
COPY . .

FROM install-stage as playwright-stage
CMD ["pytest", "test/admin_app_e2e_tests"]
