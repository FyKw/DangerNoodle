import xml.etree.ElementTree as ET
import json


def convert_xml_to_json(xml_file_path):
    # 1. Parse the XML file
    xml_root = read_xml(xml_file_path)

    # 2. Create a template for the JSON output
    json_output = {
        "components": [],
        # Any static metadata fields can be added here
        "type": "default",
        "id": "nameHere",  # This can be dynamic if needed
        "exporter": {
            "name": "CustomExporter",
            "version": "1.0"
        },
        "executionPlatform": "Camunda Platform",
        "executionPlatformVersion": "7.19.0",
        "schemaVersion": 9
    }

    for panel in xml_root.findall('Panel'):
        panel_name = panel.find("stringAttribute[@name='value']").text
        json_output["components"].append({
            "label": panel_name,
            "type": "image",
            "layout": {"row": 0, "columns": 12},  # Default layout; can be adjusted
            "id": "img_" + panel_name,  # Creating a unique ID based on panel name
            "source": "https://placehold.co/1000x70?text=Tab"  # This can be replaced with the actual URL
        })

        for form_group in panel.findall('FormGroup'):

            #If only one field is in a panel it will not be shown as a single item list but directly have the fieldattribus
            if form_group.find('formField') is None:
                form_fields = [form_group]
            else:
                form_fields = form_group.findall('formField')
            for form_field in form_fields:
                # Determine field type and properties
                component = translate_field(form_field)

                json_output["components"].append(component)

    output_path = "result.JSON"
    write_json_to_file(json_output, output_path)

    return json_output

def write_json_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def translate_field(form_field):
    field_type = "unknown"

    match form_field:
        case _ if form_field.find('stringAttribute') is not None:
            field_type = 'text'
            return {
                'label': "text field",
                'type': 'textfield',

                'defaultValue': default_value,
                "layout": {"row": 0, "columns": 12},
                "id": "field_" + xml_element.find('name').text  # Creating a unique ID based on field name
                # ... any other properties
            }
        case _ if form_field.find('booleanAttribute') is not None:
            field_type = 'checkbox'
        # You can add more cases as needed for other field types
        case _:
            pass  # default case; can add logging or error handling here

    return field_type


def map_string_attribute(xml_element):
    # Extract necessary details from the XML element
    label = xml_element.find('name').text
    default_value = xml_element.find('value').text  # This is a hypothetical path and might need adjustments

    # Return the corresponding JSON component representation
    return {
        'label': label,
        'type': 'text',
        'defaultValue': default_value,
        "layout": {"row": 0, "columns": 12},
        "id": "field_" + xml_element.find('name').text  # Creating a unique ID based on field name
        # ... any other properties
    }


def read_xml(file_path):
    """Read and parse an XML file.

    Args:
        file_path (str): Path to the XML file.

    Returns:
        Element: Root element of the parsed XML.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root


if __name__ == "__main__":
    xml_root = read_xml("Test_Sweha.xml")