import json 
import heapq

def main():
    with open("CDM3_exposure_content.json", "r") as infile:
        json_data=json.load(infile)
    entities_array = json_data["value"]
    #print(f"read json from file: {json_data}")
    #print(f"read entities from json file: {entities_array}")

    heap = []
    for e in entities_array:
       id = e["identification"]["id"]
       print(f"processing {id}")
       payload = e["payload"]
       payload_total_len = 0
       for k,v in payload.items():
           if isinstance(v, list): 
               payload_total_len += len(v)
       print(f"enity {id}, payload length {payload_total_len}")
       heapq.heappush(heap, (-payload_total_len, id))
       #print(f"entity {id}")
       if payload_total_len > 3000: 
           print(f"entity {id}, payload length {payload_total_len}")
    while True: 
        max_payload, max_ent = heapq.heappop(heap) 
        if max_payload > -3000:
            break
        print(f"max payload length {-max_payload}, entity {max_ent}")

if __name__ == "__main__":
    main()
