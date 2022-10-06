from typing import List

from crud_endpoints_generator.resource_configurations import ResourceConfigurations

def add_resource_url_ids_to_schema_properties(
    resource_schema_dict: dict,
    resource_configurations: ResourceConfigurations,
    admin_resources: List[ResourceConfigurations]
):
    for resource_schema_property in resource_schema_dict["properties"]:
        if (
            ("$ref" in resource_schema_dict["properties"][resource_schema_property])
            or (resource_schema_dict["properties"][resource_schema_property]["type"] == "array")
        ):
            resource_schema_property_type = resource_configurations.ResourceSchema.get_class_by_field(resource_schema_property)
            for propertyResource in admin_resources:
                if (
                    issubclass(resource_schema_property_type, propertyResource.ResourceSchema)
                    or issubclass(propertyResource.ResourceSchema, resource_schema_property_type)
                    or (propertyResource.ResourceSchema == resource_schema_property_type)
                ):
                    resource_schema_dict["properties"][resource_schema_property]["resourceUrlId"] = propertyResource.resource_endpoints_url_prefix
