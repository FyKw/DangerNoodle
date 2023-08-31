"""
This script should be put into a folder with xml files.
After execution, it should make a dir, filled with a json file for each xml file respectively.
"""

import glob
import json
import random
import string
import uuid
from ast import literal_eval

from lxml import etree

# Function to process an individual XML file
xsd_file_path = 'autogenerated_schema.xsd'
# Search for all .xml files in the current folder
xml_files = glob.glob('./*.xml')


def generate_uuid(length):
    return str(uuid.uuid4())[:length]


def generate_random_string(length):
    # Get all the ASCII letters in lowercase and uppercase
    letters = string.ascii_letters
    # Randomly choose characters from letters for the given length of the string
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def process_xml_file(file_path):
    # Parse the XML file and validate it against the schema
    xsd_tree = etree.parse(xsd_file_path)
    schema = etree.XMLSchema(xsd_tree)

    xml_tree = etree.parse(file_path)
    print(f"XML Validation: {schema.validate(xml_tree)}")  # Print validation result
    if schema.validate(xml_tree):
        process_tree(xml_tree)


def get_value_from_elements(list_of_elements, look_for_this_name):
    for element in list_of_elements:
        name_attribute = element.find('./name')
        if name_attribute is not None and name_attribute.text == f'{look_for_this_name}':
            if element.find('./value') is not None and element != "":
                res = element.find('./value').text
                return res


def translate_tab_item(xml_element):
    # Arrange

    row_number = generate_random_string(6)
    make_id = "Field_" + generate_uuid(7)
    tab_name_element = xml_element.find('./stringAttribute/value')
    tab_name = tab_name_element.text if tab_name_element is not None else ""
    # placehold.co will give us simple images that we can use to create the illusion of hline like blocks
    placeholder_url = "https://placehold.co/1000x70?text=" + str(tab_name)

    # build result
    result = {
        "label": "Image view",
        "type": "image",
        "layout": {
            "row": row_number,
            "columns": None
        },
        "id": make_id,
        "source": placeholder_url,
        "properties": {}  # empty for now
    }
    # print(json.dumps(result, indent=4))  # This should print to file later
    return result


def translate_group_item(xml_element):
    # TODO clean this mess up

    row_number = generate_random_string(6)
    make_id = "Field_" + generate_uuid(7)
    group_name_element = xml_element.find('./stringAttribute/value')
    group_name = group_name_element.text if group_name_element is not None else "No Name Set for Group"
    my_text = "## " + group_name

    # build result
    result = {
        "text": my_text,
        "label": "todo",
        "type": "text",
        "layout": {
            "row": row_number,
            "columns": None
        },
        "id": make_id,
    }
    # print(json.dumps(result, indent=4))  # This should print to file later
    return result


def translate_date(xml_element):
    datefield_label_element = xml_element.find('./label')
    datefield_label = datefield_label_element.text if datefield_label_element is not None else ""

    row_number = generate_random_string(6)
    make_id = "Field_" + generate_uuid(7)
    make_key = generate_uuid(7) + "_key"

    boolean_attributes = xml_element.findall('./booleanAttribute')

    # default attributes, booleans are set at check
    my_date_description = ""

    disabled_value = not get_value_from_elements(boolean_attributes, 'editable').capitalize() == 'True'
    readonly_value = get_value_from_elements(boolean_attributes, 'readOnly').capitalize() == 'True'

    # build result
    result = {
        "subtype": "datetime",
        "dateLabel": datefield_label,
        "label": "todo",
        "type": "datetime",
        "layout": {
            "row": row_number,
            "columns": None
        },
        "id": make_id,
        "key": make_key,
        "timeLabel": "Todo",
        "timeSerializingFormat": "utc_offset",
        "timeInterval": 5,
        "description": my_date_description,
        "disabled": disabled_value,
        "readonly": readonly_value
    }
    # print(json.dumps(result, indent=4))  # This should print to file later
    return result


def translate_textarea(xml_element):
    # make Id elements
    row_number = generate_random_string(6)
    make_id = "Field_" + generate_uuid(7)
    make_key = generate_uuid(7) + "_key"

    # set default values, bool will be set by the check
    default_attribute = ""
    description_attribute = ""
    min_length_attribute = 0
    max_length_attribute = 99999
    pattern_attribute = ""

    # define lookup tables from the xml
    long_string_attributes = xml_element.findall('./longStringAttribute')
    boolean_attributes = xml_element.findall('./booleanAttribute')
    string_attributes = xml_element.findall('./stringAttribute')
    number_attributes = xml_element.findall('./numberAttribute')

    # label of the element
    textfield_label_element = xml_element.find('./label')
    textfield_label = textfield_label_element.text if textfield_label_element is not None else ""

    # Description of the element
    if get_value_from_elements(long_string_attributes, 'description') is not None:
        description_attribute = get_value_from_elements(long_string_attributes, 'description')

    # default value of the element
    if get_value_from_elements(string_attributes, 'emptyText') is not None:
        default_attribute = get_value_from_elements(string_attributes, 'emptyText')

    # min length of the element
    if get_value_from_elements(number_attributes, 'minLength') is not None:
        min_length_attribute = get_value_from_elements(number_attributes, 'minLength')

    # max length of the element
    if get_value_from_elements(number_attributes, 'maxLength') is not None:
        min_length_attribute = get_value_from_elements(number_attributes, 'maxLength')

    # pattern to check against of the element
    if get_value_from_elements(string_attributes, 'regex') is not None:
        pattern_attribute = get_value_from_elements(string_attributes, 'regex')

    # readonly bool of the element
    readonly_attribute = get_value_from_elements(boolean_attributes, 'readOnly').capitalize == 'True'

    # required value of the element
    required_attribute = get_value_from_elements(boolean_attributes, 'allowBlank').capitalize == 'True'

    # build result
    result = {
        "label": textfield_label,
        "type": "textfield",
        "layout": {
            "row": row_number,
            "columns": None
        },
        "id": make_id,
        "key": make_key,
        "defaultValue": default_attribute,
        "description": description_attribute,
        "readonly": readonly_attribute,
        "validate": {
            "required": required_attribute,
            "minLength": min_length_attribute,
            "maxLength": max_length_attribute,
            "pattern": pattern_attribute
        }
    }
    # print(json.dumps(result, indent=4))  # This should print to file later
    return result


def translate_timespinner(xml_element):
    name_element = xml_element.find('./name')
    if name_element is not None:  # Check if the 'name' element was found
        name = name_element.text  # Access the text content of the 'name' element
        print(name)
    else:
        print("Name element not found")
    pass


def translate_radiobutton(xml_element):
    # make Id elements
    row_number = generate_random_string(6)
    make_id = "Field_" + generate_uuid(7)
    make_key = generate_uuid(7) + "_key"

    # set default values, bool will be set by the check
    description_attribute = ""

    # define lookup tables from the xml
    long_string_attributes = xml_element.findall('./longStringAttribute')
    custom_attributes = xml_element.findall('./customAttribute')
    array_attributes = xml_element.findall('./arrayAttribute')

    # label of the element
    radio_label_element = xml_element.find('./label')
    label_attribute = radio_label_element.text if radio_label_element is not None else ""

    # disabled was not set in test data
    disabled_attribute = False

    # readonly was not set in test data
    readonly_attribute = False

    # required attribute was not set in test data
    required_attribute = False

    # values from the data
    # Convert the string to a Python list
    input_str = get_value_from_elements(array_attributes, 'data')
    input_list = literal_eval(input_str)

    # Flatten the list and create the desired dictionary
    values_attribute = [{"label": val, "value": val} for sublist in input_list for val in sublist]

    # default attribute
    default_attribute = literal_eval(get_value_from_elements(custom_attributes, 'value'))[0]

    # description attribute
    # Description of the element
    if get_value_from_elements(long_string_attributes, 'description') is not None:
        description_attribute = get_value_from_elements(long_string_attributes, 'description')

    result = {
        "values": values_attribute,  # should be a list [] with elements {}
        "label": label_attribute,
        "type": "radio",
        "layout": {
            "row": row_number,
            "columns": None
        },
        "id": make_id,
        "key": make_key,
        "description": description_attribute,
        "defaultValue": default_attribute,
        "disabled": disabled_attribute,
        "readonly": readonly_attribute,
        "validate": {
            "required": required_attribute
            }
        }
    # print(json.dumps(result, indent=4))
    return result


def translate_textfield(xml_element):
    # Todo: check if there are any other changes
    return translate_textarea(xml_element)


def translate_booleancombo(xml_element):
    # make Id elements
    row_number = generate_random_string(6)
    make_id = "Field_" + generate_uuid(7)
    make_key = generate_uuid(7) + "_key"

    # set default values, bool will be set by the check
    default_attribute_bool = False
    description_attribute = ""
    disabled_attribute = False

    # define lookup tables from the xml
    long_string_attributes = xml_element.findall('./longStringAttribute')
    boolean_attributes = xml_element.findall('./booleanAttribute')
    string_attributes = xml_element.findall('./stringAttribute')

    # label of the element
    label_attribute = xml_element.find('./label').text

    # description attribute of the element
    if get_value_from_elements(long_string_attributes, 'description') is not None:
        description_attribute = get_value_from_elements(long_string_attributes, 'description')

    # disabled attribute
    if get_value_from_elements(string_attributes, 'value') is not None:
        disabled_attribute = get_value_from_elements(string_attributes, 'value').text == "True"

    # readonly attribute
    readonly_attribute = get_value_from_elements(boolean_attributes, 'readOnly').capitalize == 'True'

    # required attribute was not set in test data
    required_attribute_bool = get_value_from_elements(boolean_attributes, 'allowBlank').capitalize == 'True'

    result = {
        "label": label_attribute,
        "type": "checkbox",
        "layout": {
            "row": row_number,
            "columns": None
        },
        "id": make_id,
        "key": make_key,
        "description": description_attribute,
        "defaultValue": default_attribute_bool,
        "disabled": disabled_attribute,
        "readonly": readonly_attribute,
        "validate": {
            "required": required_attribute_bool
        }
    }
    # print(json.dumps(result, indent=4))
    return result


def translate_combo(xml_element):
    row_number = generate_random_string(6)
    make_id = "Field_" + generate_uuid(7)
    make_key = generate_uuid(7) + "_key"

    # set default values, bool will be set by the check
    description_attribute = ""

    # define lookup tables from the xml
    long_string_attributes = xml_element.findall('./longStringAttribute')
    array_attributes = xml_element.findall('./arrayAttribute')
    boolean_attributes = xml_element.findall('./booleanAttribute')

    # label of the element
    radio_label_element = xml_element.find('./label')
    label_attribute = radio_label_element.text if radio_label_element is not None else ""

    # disabled was not set in test data
    disabled_attribute = get_value_from_elements(boolean_attributes, 'editable').capitalize == 'True'

    # readonly was not set in test data
    readonly_attribute = get_value_from_elements(boolean_attributes, 'readOnly').capitalize == 'True'

    # required attribute was not set in test data
    required_attribute = get_value_from_elements(boolean_attributes, 'allowBlank').capitalize == 'True'

    # values from the data
    # Convert the string to a Python list
    input_str = get_value_from_elements(array_attributes, 'data')
    input_list = literal_eval(input_str)
    # Flatten the list and create the desired dictionary
    values_attribute = [{"label": val, "value": val} for sublist in input_list for val in sublist]

    # description attribute
    # Description of the element
    if get_value_from_elements(long_string_attributes, 'description') is not None:
        description_attribute = get_value_from_elements(long_string_attributes, 'description')

    result = {
        "values": values_attribute,  # should be a list [] with elements {}
        "label": label_attribute,
        "type": "taglist",
        "layout": {
            "row": row_number,
            "columns": None
        },
        "id": make_id,
        "key": make_key,
        "description": description_attribute,
        "disabled": disabled_attribute,
        "readonly": readonly_attribute,
        "validate": {
            "required": required_attribute
            }
        }
    # print(json.dumps(result, indent=4))
    return result


def translate_label(xml_element):
    name_element = xml_element.find('./name')
    if name_element is not None:  # Check if the 'name' element was found
        name = name_element.text  # Access the text content of the 'name' element
        print(name)
    else:
        print("Name element not found")
    pass


def map_element(xml_element):
    # Find the 'name' child element and get its text content
    match xml_element.find('./xtype').text:
        case 'ddtabitem':
            translate_tab_item(xml_element)
        case 'ddgroup':
            translate_group_item(xml_element)
        case 'tpl-datefield':
            translate_date(xml_element)
        case 'tpl-textarea':
            translate_textarea(xml_element)
        case 'tpl-label':
            translate_label(xml_element)
        case 'tpl-timespinner':
            translate_timespinner(xml_element)
        case 'tpl-radiobtn':
            translate_radiobutton(xml_element)
        case 'tpl-textfield':
            translate_textfield(xml_element)
        case 'tpl-booleancombo':
            translate_booleancombo(xml_element)
        case 'tpl-combo':
            translate_combo(xml_element)
        case _:
            print("Could not map element")


def process_panel(panel):
    # Check if xtype has the value "ddtabitem"
    xtype = panel.find('./xtype').text
    if xtype == 'ddtabitem':
        # Call mapElement function (to be implemented later)
        map_element(panel)
    else:
        print("panel has wrong format")

        # Iterate through FormGroup elements within the Panel
    for form_group in panel.findall('./FormGroup'):
        map_element(form_group)  # Call mapElement for each FormGroup

        # Iterate through FormField elements within the FormGroup
        for form_field in form_group.findall('./formField'):
            map_element(form_field)  # Call mapElement for each FormField


# Iterate through all Panel elements within the XML
def process_tree(xml_tree):
    for panel in xml_tree.findall('.//Panel'):
        process_panel(panel)


# Iterate through the found XML files and process each one
def main():
    for xml_file in xml_files:
        print(f"Processing file: {xml_file}")
        process_xml_file(xml_file)


if __name__ == '__main__':
    main()
