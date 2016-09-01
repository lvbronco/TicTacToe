import json

class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        # Any object can implement to_dict() function
        to_dict_func = getattr(obj, "to_dict", None)
        if callable(to_dict_func):
            return to_dict_func()
        # Any object can implement to_json() function
        to_json_func = getattr(obj, "to_json", None)
        if callable(to_json_func):
            return to_json_func()

        return json.JSONEncoder.default(self, obj)

def jsonencode(obj):
    return json.dumps(obj, cls = MyEncoder)

def json_encode(obj):
    return json.dumps(obj, cls = MyEncoder)

def json_decode(obj):
    if (obj is None) or (len(obj) == 0):
        return None
    else:
        return json.loads(obj)
