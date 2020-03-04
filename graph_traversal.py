import hashlib
import requests
import time

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-treasure-hunt.herokuapp.com/api/adv"

    opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    path = []
    graph = {}
    last_room = None
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token 50f83144a74d87d4dbe9230f7714c1ceb54d55b0'}
    r = requests.get(url=node + "/init", headers=headers)

    while True:
        print('\n')
        print('Graph: ', graph)
        print('\n')
        data = r.json()
        
        time.sleep(data.get('cooldown'))
        exits = data.get('exits')
        room_id = data.get('room_id')
        room_name = data.get('title')
        print('Room ID: ', room_id)
        print('Room Name: ', room_name)
        
        # if data.get('room_id') == 555:
        #     print("Welcome to your room!")
        #     break
        # if data.get('title') == "Sandofsky's Sanctum":
        #     print("Welcome to your room!")
        #     break
        # if len(data.get('items')) > 0 or data.get('title') == "Sandofsky's Sanctum":
        #     print("Welcome to your room!")
        #     break

        if room_id not in graph:
            graph[room_id] = {"title": data.get('title'), "description": data.get('description'), "terrain": data.get(
                'terrain'), "coordinates": data.get('coordinates'), "elevation": data.get('elevation')}
            for dir in exits:
                graph[room_id][dir] = "?"
        if last_room != None:
            graph[last_room][path[-1]] = room_id
            graph[room_id][opposites[path[-1]]] = last_room
        unexploredExits = [dir for dir in exits if graph[room_id][dir] is "?"]
        print('unexplored exits', unexploredExits)
        if not len(unexploredExits):
            if len(path) is 0:
                print('Final graph')
                print(graph)
                break
            wayBack = opposites[path.pop()]
            r = requests.post(url=node + "/move", json={
                              "direction": wayBack, "next_room_id": str(graph[room_id][wayBack])}, headers=headers)

            print("Used Wise Explorer")
            last_room = None
        else:
            wayForward = unexploredExits[0]
            path.append(wayForward)
            last_room = room_id
            r = requests.post(url=node + "/move",
                              json={"direction": wayForward}, headers=headers)
