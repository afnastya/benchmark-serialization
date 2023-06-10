import json
import xmltodict
import msgpack
import yaml


# ---------------------- JSON -----------------------------

def from_json(json_data):
    return json.loads(json_data)

def to_json(dict_data):
    return json.dumps(dict_data)

# ----------------------- MessagePack ---------------------

def from_msgpack(msgpack_data):
    return msgpack.loads(msgpack_data)

def to_msgpack(dict_data):
    return msgpack.dumps(dict_data)

# ----------------------- XML -----------------------------

def from_xml(xml_data):
    return xmltodict.parse(xml_data)

def to_xml(dict_data):
    if len(dict_data) > 1:
        dict_data = {"root": dict_data}
    return xmltodict.unparse(dict_data)

# ----------------------- YAML ----------------------------

def from_yaml(yaml_data):
    return yaml.load(yaml_data, Loader=yaml.Loader)

def to_yaml(dict_data):
    return yaml.dump(dict_data)

test_data = {
    "int": -345,
    "float": 1.563,
    "string": "afuhqirkrjvnruhiwqufh"
}

test_functions = {
    "JSON": [from_json, to_json],
    "XML": [from_xml, to_xml],
    "MSGPACK": [from_msgpack, to_msgpack],
    "YAML": [from_yaml, to_yaml]
}