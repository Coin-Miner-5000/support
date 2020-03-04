from graph import graph_of_map
import requests
import sys
import time


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
    headers =  {'Content-Type' : 'application/json',
            'Authorization': 'Token e9ec9a2dab95a02a549eb753f6eea0b680313347'}
    r = requests.get(url=node + "/init", headers=headers)

    data = r.json()
    destination_room = sys.argv[1]
    print(destination_room)
    time.sleep(data.get('cooldown'))
    path = BFS(data.get('room_id'), int(destination_room))

    for dir in path:
        r = requests.post(url=node + "/move", json={"direction": dir, "next_room_id": str(graph_of_map[data.get('room_id')][dir])}, headers=headers)
        data = r.json()

        time.sleep(data.get('cooldown'))

    sys.exit(0)
