import heapq
from math import sqrt

# Helper: euklideszi tavolsag szamitasa ket pont kozott
def euclidean_distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# A* Algorithm
def a_star_route_optimization(addresses, start_index):
    open_list = []
    heapq.heappush(open_list, (0, start_index, [], 0))  # (f_score, current_node, path, distance_travelled)
    closed_list = set()
    optimal_route = []
    step_by_step_info = []

    while open_list:
        f_score, current_index, path, distance_travelled = heapq.heappop(open_list)

        if current_index in closed_list:
            continue

        path = path + [addresses[current_index]]
        closed_list.add(current_index)

        if len(path) == len(addresses):  # eddigi helyek
            optimal_route = path
            break

        step_info = {
            'current': addresses[current_index]['address'],
            'options': [],
            'chosen': None,
            'distance': 0,
            'total_distance': 0
        }

        # legkozelebbi olyan helyek, amik hianyoznak
        valid_neighbors = []
        for neighbor_index, neighbor in enumerate(addresses):
            if neighbor_index != current_index and neighbor_index not in closed_list:
                g_score = distance_travelled + euclidean_distance(
                    (addresses[current_index]['lat'], addresses[current_index]['lon']),
                    (neighbor['lat'], neighbor['lon'])
                )
                step_info['options'].append({
                    'address': neighbor['address'],
                    'distance': g_score
                })
                valid_neighbors.append((g_score, neighbor_index, neighbor))

        # validalasa a legkozelebbi helyeknek
        if valid_neighbors:
            # legkozelebbi kivalasztasa
            chosen_option = min(step_info['options'], key=lambda x: x['distance'])
            step_info['chosen'] = chosen_option['address']
            step_info['distance'] = chosen_option['distance']
            step_info['total_distance'] = distance_travelled + chosen_option['distance']

            chosen_neighbor = min(valid_neighbors, key=lambda x: x[0])
            heapq.heappush(open_list, (chosen_neighbor[0], chosen_neighbor[1], path, chosen_neighbor[0]))
        else:
            break

        step_by_step_info.append(step_info)

    return optimal_route, step_by_step_info

# ut optimalizalas a vizualizaciohoz
def get_simulation_data(addresses):
    optimal_route, step_info = a_star_route_optimization(addresses, start_index=0)
    simulation_data = {
        'addresses': addresses,
        'optimal_route': optimal_route,
        'steps': step_info
    }
    return simulation_data
