
## Backend
### Development Cycle
- 1. Setup codebase
    - 1. Create a new branch:
        - For developing a new feature:
            - Fork a feature branch from *main* branch
        - For critical bug fixes (hot fixes):
            - Fork a hotfix branch from *master* or *staging* branch depending on where bug is found
    - 2. 

- 2. Do Test Driven Development
    - Docker based (prefered):
        - Run script to create docker container for python api and populate database
        - Run Pytest tests and watch for change
        - Set sqlite as database in environment variables 
        - Launch python api to test manually
        - Set mysql/sqlite as database in environment variables
    - Without Docker:
        - Setup python environment
        - Run Pytest tests and watch for change
        - Set sqlite as database in environment variables
        - Launch python api
        - Set mysql/sqlite as database in environment variables
- 2. Running E2E tests to ensure no errors on frontend
    - Docker based (prefered):
        - Run script to create docker containers for:
            - python api
            - Database if MySQL
            - Vue server serving Frontend Master branch code
        - Run Vue Cypress E2E tests
- 3. Add flag in git commit to optionally run docker tests before commit


- Development branch CI
    - Tests to run
        - Pytest
    - Branch Pipeline triggers
        - Push to Development branch
        - Merge to Development branch (from branches for features, fixes etc)
    - Branch Rules & Limitations
        - Cannot be merged into Master
            - To merge into Master, merge into Staging
        - Cannot be merged into Hotfix
        - Can be merged into Staging only by select users
- 5. Hotfix branch CI
    - Tests to run:
        - Pytest
    - Branch Pipeline triggers:
        - Push to Hotfix branch
    - Branch Rules & Limitations
        - Cannot be merged into Master
            - To merge into Master, merge into Staging
        - Can be merged into Staging only by select users
        - Should be created only from Master branches
        - No branch can be merged into Hotfix
- 6. Staging / QA Cycle
    - Staging branch CI
        - Tests to run
            - Backen Pytest
            - Backend E2E
        - Branch Pipeline triggers
            - Push to Staging branch
        - Branch Rules & Limitations
            - Can be merged into Staging For Master only by select users
            - Only Development & Hotfix can be merged into Staging
- 6. Production Cycle
    - Production branch CI
        - Tests to run
            - None
    - Branch Rules & Limitations
        - Only Staging can be merged into Master
        - Should be merged only after current Frontend has been tested with it


## Admin App
Admin app must be cloned inside folder: ```src/admin/view```

To build a new admin_app:
    - cd into vue project folder: ```cd src/admin/view/vue_admin```
    - build static app: ```npm run build``` (or ```npm run build -- --mode development --watch``` to build in development and watch)

The app will be built inside folder: ```src/admin_app/vue_admin_html```, from where FastAPI will mount the static files and serve to: ```<https://your-fastapi-domain.com>/admin```

## Frontend


