# Features Requirement

### Technical Decisions / Constraints
- Support demo Vue App to assign/unassign items to user
- Support admin app to manage items & users

*Write specs such that they are directly transferable as E2E tests*
---
## API Doc
- View API doc
    - Must be able to access API documentation
        - url: https://domain.com/docs

## Items
- Get all items
    - Must be able to get all items:
        - url: GET https://domain.com/api/items/
        - query params:
            - skip: number of items to skip from initial
            - limit: max number of items to get
        - response:
            - status: 200
            - body: list of items (paginated)
    - Must be able to get next group of items
- Get item
    - Must be able to get an item by id
        - url: GET https://domain.com/api/items/{item_id}/
        - response:
            - status: 200
            - body: item object
- Create new item
    - Must be able to create an item
        - url: POST https://domain.com/api/items/
        - request: 
            - body: item object (without id)
        - response:
            - status: 200
            - body: item object (with id)
- Delete item
    - Must be able to delete an item by id
        - url: DELETE https://domain.com/api/items/{item_id}/
        - response:
            - status: 204

### User Items
- Get user items
    - Must be able to get a user's items
        - url: GET https://domain.com/api/users/{user_id}/items/
        - query params:
            - skip: number of items to skip from initial
            - limit: max number of items to get
        - response:
            - status: 200
            - body: list of items (paginated)
    - Must be able to get next group of items
- Assign item to user
    - Must be able to assign an item to a user
        - url: POST https://domain.com/api/users/{user_id}/items/{item_id}/
        - request: 
            - body: None
        - response:
            - status: 204
- Unassign item from user
    - Must be able to get a user's items
        - url: DELETE https://domain.com/api/items/{user_id}/items/{item_id}/
        - response:
            - status: 204

## Users
- Get all users
    - Must be able to get all users:
        - url: GET https://domain.com/api/users/
        - query params:
            - skip: number of users to skip from initial
            - limit: max number of users to get
        - response:
            - status: 200
            - body: list of users (paginated) 
    - Must be able to get next group of users
- Get user
    - Must be able to get an user by id
        - url: GET https://domain.com/api/users/{user_id}/
        - response:
            - status: 200
            - body: user object
- Create new user
    - Must be able to create an user
        - url: POST https://domain.com/api/users/
        - request: 
            - body: user object (without id)
        - response:
            - status: 200
            - body: user object (with id)
- Delete user
    - Must be able to delete an user by id
        - url: DELETE https://domain.com/api/users/{user_id}/
        - response:
            - status: 204
