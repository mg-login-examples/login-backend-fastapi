
- Implement custom trailing slash router for FastAPI's APIRouter 
    - https://github.com/tiangolo/fastapi/issues/2060
    - When a url without trailing '/' is included, FastAPI/Starlette redirects to url with trailing '/'. This causes some issues
    - One such issue is that when accessing the frontend admin app's resource url, if the trailing slash is not included, the redirect does not work, returning a 404

- Sort docker scripts
    - Split dockerfile scripts
    - Split docker-compose scripts

- Parallelize each test
