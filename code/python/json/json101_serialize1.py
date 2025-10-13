import json 

def main():
    json_data_str = '{"id": "foo", "age": 45, "city": "hadera"}'
    json_data = json.loads(json_data_str)
    with open("out.json", "w") as out:
        json.dump(json_data, out)
    with open("out_indent.json", "w") as out_indent:
        json.dump(json_data,out_indent, indent=4 )

if __name__ == "__main__":
    main()
