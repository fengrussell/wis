import json


# 程序入口
if __name__ == '__main__':
    json_input = '{ "one": 1, "two": { "list": [ {"item":"A"},{"item":"B"} ] } }'

    json_input1 = '[{"name":"软件部", "path":"Department_Software"}, {"name":"合肥中心", "path":"Department_HeFei"}]'

    try:
        decoded = json.loads(json_input1)

        # pretty printing of json-formatted string
        print(json.dumps(decoded, sort_keys=True, indent=4))

        print("JSON parsing example: ", decoded['one'])
        print("Complex JSON parsing example: ", decoded['two']['list'][1]['item'])

    except (ValueError, KeyError, TypeError):
        print("JSON format error")