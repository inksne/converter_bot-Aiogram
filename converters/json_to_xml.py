import json
import xmltodict


def json_to_xml(json_string: str):
    json_data = json.loads(json_string)
    xml_string = xmltodict.unparse(json_data, pretty=True)
    
    if xml_string.startswith("<?xml"):
        xml_string = xml_string.split("\n", 1)[1]
    
    return xml_string


def xml_to_json(xml_string: str):
    xml_data = xmltodict.parse(xml_string)
    json_data = json.dumps(xml_data, indent=4)
    return json_data