# Environments
## Production
- Real world environment
- Contains real data
- Used by real customers
## Staging / UAT
- As close to Production environment
- Could also contain snapshot of production data
- Used for internal demo, pilot programs
## Development
- Contains test data
- Used for testing by developers & qa

# Git
## Git branches
- *master* branch
    - Parent - None
    - Contains production code
    - Deployed in *Production* environment as an external release
    - Once code is merged into *master*, it is in production cycle
- *staging* branch
    - Parent: *master*
    - Contains staging code, ready to be merged into *master* branch for external release
    - Deployed in *Staging* environment as an internal release
    - Once code is merged into *staging* branch, it is in staging cycle
- *main* branch
    - Parent: *staging*
    - Contains working development code, to be merged into *staging* branch after qa cycle is complete
    - Deployed in *Development* environment as a dev release
    - Once code is merged into *main* branch, it is in qa cycle
- *feature*X branch
    - Parent: *main*
    - Contains code for new feature X, to be merged into *main* branch after feature is completed
- *bugfix*X branch
    - Parent: *main*
    - Contains code for bug fix, to be merged into *main* branch after bug is fixed
- *hotfixX* branch
    - Parent: *staging*
    - Contains code for bug fix, to be merged into *staging* branch after bug is fixed
- *hotfix*Y branch
    - Parent: *master*
    - Contains code for critical fix, to be merged directly into *master*
- Note:
    - Parent denotes branch from which it is created, and any changes on parent branch must be merged into that branch ASAP
## Gif Flow
- 1. *main* branch contains latest code. Developers fork *feature* branches and *bugfix* branches from *main* branch
- 2 *feature* branches and *bugfix* branches are merged back to *main* branch once development is completed on them. Prior to merging in *main* branch, CI pipeline runs tests to ensure code quality
- 3. *main* branch is merged into *staging* branch once code is ready for release. Prior to merging in *staging* branch, CI pipeline runs tests to ensure code quality
- 4. *staging* branch is merged into *main* branch for a release. No tests are run when merging to *master*

# Available Tests
- *Pytest Unit*
    - Unit & Integration Backend Tests
    - Tests on backend code directly
    - Required integration:
        - Database
- *API E2E*
    - E2E Backend tests
    - Tests on deployed API
    - Required integration:
        - Backend stack
- *Vue Component*
    - Unit & Component Frontend Tests
    - Tests on frontend code directly
    - Required integration:
        - None
- *Vue Cypress E2E*
    - E2E Frontend tests
    - Tests on frontend code directly
    - Required integration:
        - Backend stack
- *Cypress E2E*
    - E2E Frontend tests
    - Tests on a served Frontend
    - Required integration:
        - Frontend stack
        - Backend stack

# Continuous Integration Continuous Development

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
Admin app must be cloned inside folder: ```src/admin_app```

To build a new admin_app:
    - cd into vue project folder: ```cd src/admin_app/vue_admin```
    - build static app: ```npm run build``` (or ```npm run build -- --mode development --watch``` to build in development and watch)

The app will be built inside folder: ```src/admin_app/vue_admin_html```, from where FastAPI will mount the static files and serve to: ```<https://your-fastapi-domain.com>/admin```

## Frontend


