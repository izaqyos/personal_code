import json 

def main():
    json_data_str = '{"id": "foo", "age": 45, "city": "hadera"}'
    with open("out.json", "r") as infile:
        json_data=json.load(infile)
    print(f"read json from file: {json_data}")
    json_data_assert = json.loads(json_data_str)
    assert(json_data_assert == json_data)

if __name__ == "__main__":
    main()
