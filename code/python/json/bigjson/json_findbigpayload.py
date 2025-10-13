import json 
import heapq

def main():
    with open("CDM3_exposure_content.json", "r") as infile:
        json_data=json.load(infile)
    entities_array = json_data["value"]

    heap = []
    for e in entities_array:
       id = e["identification"]["id"]
       payload = e["payload"]
       payload_total_len = 0
       for k,v in payload.items():
           if isinstance(v, list): 
               payload_total_len += len(v)
       heapq.heappush(heap, (-payload_total_len, id, v))
    while True: 
        max_payload, max_ent, entity_payload = heapq.heappop(heap) 
        if max_payload > -3000:
            break
        print(f"max payload length {-max_payload}, entity {max_ent}, payload: {entity_payload} ")

if __name__ == "__main__":
    main()

