
def add_resource_url_ids_to_schema_properties(resourceSchemaDict, resource, adminResources):
    for resourceSchemaProperty in resourceSchemaDict["properties"]:
        if (
            ("$ref" in resourceSchemaDict["properties"][resourceSchemaProperty])
            or (resourceSchemaDict["properties"][resourceSchemaProperty]["type"] == "array")
        ):
            resourceSchemaPropertyType = resource.ResourceSchema.get_class_by_field(resourceSchemaProperty)
            for propertyResource in adminResources:
                if (
                    issubclass(resourceSchemaPropertyType, propertyResource.ResourceSchema)
                    or issubclass(propertyResource.ResourceSchema, resourceSchemaPropertyType)
                    or (propertyResource.ResourceSchema == resourceSchemaPropertyType)
                ):
                    resourceSchemaDict["properties"][resourceSchemaProperty]["resourceUrlId"] = propertyResource.url_id
