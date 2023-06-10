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

# ----------------------- NATIVE ----------------------------

def from_native(str_data):
    return eval(str_data)

def to_native(dict_data):
    return str(dict_data)

test_data = {
    "bool": False,
    "int": -345,
    "float": 1.563,
    "string": "afuhq11i1rkr234jv:-(nr6s43--};fuhi23wquff[NdGI==-49[Rh",
    "dictionary": {"hello" : [-43], "world" : [-222, 5, 10098], "qwerty": [-78, 930842]},
    "list": [-435.352, 90.0, 4.34, -3.0, 9.755]
}

test_functions = {
    "JSON": [from_json, to_json],
    "XML": [from_xml, to_xml],
    "MSGPACK": [from_msgpack, to_msgpack],
    "YAML": [from_yaml, to_yaml],
    "NATIVE": [from_native, to_native],
}