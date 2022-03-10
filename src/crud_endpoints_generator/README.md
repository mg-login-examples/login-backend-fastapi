# Crud Endpoints Generator

This package helps quickly generate CRUD endpoints for any db resource.
**Note** Works with FastAPI & SQLAlchemy ORM only.

## Add a new endpoint using Crud Endpoints Generator:
- Create a SQLAlchemy Model for the resource
- Create Pydantic schemas for Create, Update/View resource
- Create schemasToModels converters for Create and/or Update endpoints if required
- Create resource Endpoints
    - create resource configurations object
    - select crud endpoints to be created
    - generate endpoints
