from graph import graph_of_map
# from underworld_graph import underworld_graph as graph_of_map
import requests
import sys
import time
import os

def BFS(current_room, destination_room):
    directions = [[]] # Queue of paths
    room_ids = [] # Queue
    visited = set()
    # room we are searching for

    did_find_room = False

    room_ids.append([current_room])

    while did_find_room == False and len(room_ids) > 0:
        path = room_ids.pop(0)
        node = path[-1]
        added_path = directions.pop(0)

        if node not in visited:
            visited.add(node)

            exits = []
            for dir in ["n", "s", "e", "w"]:
                if dir in graph_of_map[node]:
                    exits.append(dir)

            for dir in exits:
                next_room = graph_of_map[node][dir]
                if next_room not in visited and did_find_room == False:
                    new_path = path.copy()
                    next_added_path = added_path.copy()
                    next_added_path.append(dir)
                    new_path.append(next_room)

                    if next_room == destination_room:
                        did_find_room = True
                        print(next_added_path)
                        return next_added_path
                    else:
                        directions.append(next_added_path)
                        room_ids.append(new_path)



if __name__ == '__main__':
    node = "https://lambda-treasure-hunt.herokuapp.com/api/adv"
    KEY = os.environ.get("API_KEY")
    headers =  {'Content-Type' : 'application/json',
             'Authorization': f"Token {os.environ.get(KEY)}"}
    r = requests.get(url=node + "/init", headers=headers)

    data = r.json()
    destination_room = sys.argv[1]
    action = None

    if len(sys.argv) > 2:
        action = sys.argv[2]

    def move_to_room(room, data):
        time.sleep(data.get('cooldown'))
        path = BFS(data.get('room_id'), int(room))
        print(data.get('room_id'))
        for dir in path:
            r = requests.post(url=node + "/move", json={"direction": dir, "next_room_id": str(graph_of_map[data.get('room_id')][dir])}, headers=headers)
            data = r.json()
            print(f"You are in {data.get('room_id')}")
            time.sleep(data.get('cooldown'))


    def recall():
        r = requests.post(url=node + "/recall", headers=headers)
        data = r.json()
        print('recall data', data)
        print(f"{data.get('cooldown')} second cooldown")
        time.sleep(data.get('cooldown'))
        print('done')

        return data

    if action == None:
        move_to_room(destination_room, data)


    elif action == "mine":
        while True:
            time.sleep(data.get('cooldown'))
            data = recall()
            move_to_room(55, data)
            r = requests.post(url=node + "/examine", json={"name": "well"}, headers=headers)
            well_data = r.json()

            ls8_instructions = well_data.get('description')

            r = requests.post("https://afternoon-springs-84709.herokuapp.com/ls8", json={"description": ls8_instructions})

            ls8_data = r.json()
            r = requests.get(url=node + "/init", headers=headers)
            data = r.json()
            print(f"Moving to room {ls8_data.get('room')} to mine. ⛏")
            move_to_room(ls8_data.get('room'), data)

            os.system("python miner.py")
            print("Coin mined! Let's do it again.")
            time.sleep(20)


    sys.exit(0)
