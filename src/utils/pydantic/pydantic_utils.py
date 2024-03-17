from typing import Any

from pydantic import BaseModel as BaseSchema

def model_json_schema_customized_for_admin_app(resourceSchema: BaseSchema) -> dict[str, Any]:
    """Generates a JSON schema for a model class, customized for admin app.
       1. Replaces AnyOf[someType, null] with type=someType

    Args:
        by_alias: Whether to use attribute aliases or not.
        ref_template: The reference template.
        schema_generator: To override the logic used to generate the JSON schema, as a subclass of
            `GenerateJsonSchema` with your desired modifications
        mode: The mode in which to generate the schema.

    Returns:
        The JSON schema for the given model class.
    """
    json_schema = resourceSchema.model_json_schema(by_alias=False)
    # replace all AnyOf
    schema_properties: dict = json_schema['properties']

    for property, property_details in schema_properties.items():
        if 'anyOf' in property_details:
            unexpectedAnyOf = False
            if len(property_details['anyOf']) != 2:
                unexpectedAnyOf = True

            any_of_types = [t['type'] for t in property_details['anyOf'] if 'type' in t]
            null_types = [t for t in any_of_types if t == 'null']
            non_null_types = [t for t in any_of_types if t != 'null']

            if len(null_types) != 1:
                unexpectedAnyOf = True
            else:
                if len(non_null_types) == 0: # type is object
                    any_of_refs = [t['$ref'] for t in property_details['anyOf'] if '$ref' in t]
                    if len(any_of_refs) == 1:
                        property_details['$ref'] = any_of_refs[0]
                    else:
                        unexpectedAnyOf = True
                else:
                    property_details['type'] = non_null_types[0]
                    if property_details['type'] == 'array':
                        items_ref = [t['items'] for t in property_details['anyOf'] if ('type' in t and t['type'] == 'array' and '$ref' in t['items'])]
                        property_details['items'] = items_ref[0]

            if unexpectedAnyOf:
                raise Exception((
                    'Error - Found unexpected anyOf !\n'
                    'Mostly due to non-standard field implementation with pydantic schema model\n'
                    f'{json_schema["title"]}[{property}] = {schema_properties[property]}'
                ))

            property_details.pop('anyOf') # clean up anyOf

    return json_schema
