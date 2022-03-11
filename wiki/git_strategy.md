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


# Continuous Integration Continuous Development
