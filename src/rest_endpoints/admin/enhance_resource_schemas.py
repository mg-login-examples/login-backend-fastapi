from crud_endpoints_generator.resource_configurations import \
    ResourceConfigurations


def enhance_resource_schemas(
    create_resource_schema_dict: dict,
    update_resource_schema_dict: dict,
    resource_configurations: ResourceConfigurations,
    all_resources_configurations: list[ResourceConfigurations],
    is_resource_sql: bool,
):
    # Add get items url for foreign key fields to schemas
    if is_resource_sql:
        _add_resource_url_ids_to_schema_properties(
            create_resource_schema_dict,
            resource_configurations,
            all_resources_configurations,
        )
        _add_resource_url_ids_to_schema_properties(
            update_resource_schema_dict,
            resource_configurations,
            all_resources_configurations,
        )

    # Add readonly and designation fields to schemas
    # update schemas
    update_schema_readonly_fields = [
        field
        for field in resource_configurations.readonly_fields
        if (field in update_resource_schema_dict["properties"].keys())
    ]
    if len(update_schema_readonly_fields) > 0:
        update_resource_schema_dict["readonly"] = update_schema_readonly_fields
    update_schema_designation_fields = [
        field
        for field in resource_configurations.designation_fields
        if field in update_resource_schema_dict["properties"].keys()
    ]
    if len(update_schema_designation_fields) > 0:
        update_resource_schema_dict["designation_fields"] = (
            update_schema_designation_fields
        )
    # create schemas
    create_schema_readonly_fields = [
        field
        for field in resource_configurations.readonly_fields
        if field in create_resource_schema_dict["properties"].keys()
    ]
    if len(create_schema_readonly_fields) > 0:
        create_resource_schema_dict["readonly"] = create_schema_readonly_fields
    create_schema_designation_fields = [
        field
        for field in resource_configurations.designation_fields
        if field in create_resource_schema_dict["properties"].keys()
    ]
    if len(create_schema_designation_fields) > 0:
        create_resource_schema_dict["designation_fields"] = (
            create_schema_designation_fields
        )


# Move this function to pydantic utils if possible, or part of it


def _add_resource_url_ids_to_schema_properties(
    resource_schema_dict: dict,
    resource_configurations: ResourceConfigurations,
    all_resources_configurations: list[ResourceConfigurations],
):
    for resource_schema_property in resource_schema_dict["properties"]:
        schema_property = resource_schema_dict["properties"][resource_schema_property]
        if ("$ref" in schema_property) or (
            "type" in schema_property and schema_property["type"] == "array"
        ):
            resource_schema_property_type = resource_configurations.ResourceSchema.get_class_by_field(  # type: ignore
                resource_schema_property
            )
            for one_of_all_resource_configurations in all_resources_configurations:
                if (
                    issubclass(
                        resource_schema_property_type,
                        one_of_all_resource_configurations.ResourceSchema,
                    )
                    or issubclass(
                        one_of_all_resource_configurations.ResourceSchema,
                        resource_schema_property_type,
                    )
                    or (
                        one_of_all_resource_configurations.ResourceSchema
                        == resource_schema_property_type
                    )
                ):
                    schema_property["resourceUrlId"] = (
                        one_of_all_resource_configurations.resource_endpoints_url_prefix
                    )
