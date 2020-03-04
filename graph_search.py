from graph import graph_of_map

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


BFS(0, 22)

