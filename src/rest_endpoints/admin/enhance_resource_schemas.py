from typing import List

from crud_endpoints_generator.resource_configurations import ResourceConfigurations

def enhance_resource_schemas(
    create_resource_schema_dict: dict,
    update_resource_schema_dict: dict,
    resource_configurations: ResourceConfigurations,
    all_resources_configurations: List[ResourceConfigurations],
    is_resource_sql: bool,
):
    # Add get items url for foreign key fields to schemas
    if is_resource_sql:
        _add_resource_url_ids_to_schema_properties(
            create_resource_schema_dict,
            resource_configurations,
            all_resources_configurations
        )
        _add_resource_url_ids_to_schema_properties(
            update_resource_schema_dict,
            resource_configurations,
            all_resources_configurations
        )

    # Add readonly and designation fields to schemas
    update_resource_schema_dict["readonly"] = resource_configurations.readonly_fields
    update_resource_schema_dict["designation_fields"] = resource_configurations.designation_fields


def _add_resource_url_ids_to_schema_properties(
    resource_schema_dict: dict,
    resource_configurations: ResourceConfigurations,
    all_resources_configurations: List[ResourceConfigurations]
):
    for resource_schema_property in resource_schema_dict["properties"]:
        if (
            ("$ref" in resource_schema_dict["properties"][resource_schema_property])
            or (resource_schema_dict["properties"][resource_schema_property]["type"] == "array")
        ):
            resource_schema_property_type = resource_configurations.ResourceSchema.get_class_by_field(resource_schema_property)
            for one_of_all_resource_configurations in all_resources_configurations:
                if (
                    issubclass(resource_schema_property_type, one_of_all_resource_configurations.ResourceSchema)
                    or issubclass(one_of_all_resource_configurations.ResourceSchema, resource_schema_property_type)
                    or (one_of_all_resource_configurations.ResourceSchema == resource_schema_property_type)
                ):
                    resource_schema_dict["properties"][resource_schema_property]["resourceUrlId"] = one_of_all_resource_configurations.resource_endpoints_url_prefix
