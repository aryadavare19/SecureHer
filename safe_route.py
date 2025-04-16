import webbrowser
from db import get_connection


def get_location_graph():
    connection = get_connection()
    cursor = connection.cursor()

    base_graph = {
        1: {2: 10, 3: 15}, 2: {3: 25}, 3: {4: 30}, 4: {5: 5}, 5: {6: 20},
        6: {7: 35}, 7: {8: 10}, 8: {9: 15}, 9: {10: 40}, 10: {11: 10},
        11: {12: 25}, 12: {13: 5}, 13: {14: 20}, 14: {15: 15}, 15: {16: 25},
        16: {17: 30}, 17: {18: 10}, 18: {19: 20}, 19: {20: 15}, 20: {21: 25},
        21: {22: 20}, 22: {23: 10}, 23: {24: 25}, 24: {25: 30}, 25: {26: 5},
        26: {27: 15}, 27: {28: 35}, 28: {29: 10}, 29: {30: 40}
    }

    cursor.execute("SELECT location_id, danger_score FROM location_danger")
    danger_scores = dict(cursor.fetchall())

    danger_penalty = 10

    # Make graph robust by ensuring all involved node IDs are initialized
    all_node_ids = set(base_graph.keys())
    for neighbors in base_graph.values():
        all_node_ids.update(neighbors.keys())

    graph = {node: {} for node in all_node_ids}

    for node, neighbors in base_graph.items():
        for neighbor, base_weight in neighbors.items():
            penalty = danger_scores.get(node, 0) * danger_penalty
            graph[node][neighbor] = max(base_weight - penalty, 1)

    cursor.close()
    connection.close()
    return graph

def dijkstra(graph, start, destination):
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    visited = set()
    distances[start] = 0

    while len(visited) < len(graph):
        min_node = None
        min_distance = float('inf')
        for node in graph:
            if node not in visited and distances[node] < min_distance:
                min_distance = distances[node]
                min_node = node
        if min_node is None:
            break
        visited.add(min_node)
        for neighbor, weight in graph[min_node].items():
            if neighbor in visited:
                continue
            new_dist = distances[min_node] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = min_node

    path = []
    current = destination
    while current is not None:
        path.insert(0, current)
        current = previous[current]

    if distances[destination] == float('inf'):
        return None, float('inf')
    
    return path, distances[destination]

def get_safe_route(start_name, destination_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, latitude, longitude FROM locations WHERE name = %s", (start_name,))
    start_row = cursor.fetchone()
    if not start_row:
        print(f"❌ Start location '{start_name}' not found.")
        return
    start_id, start_lat, start_lon = start_row

    cursor.execute("SELECT id, latitude, longitude FROM locations WHERE name = %s", (destination_name,))
    dest_row = cursor.fetchone()
    if not dest_row:
        print(f"❌ Destination location '{destination_name}' not found.")
        return
    dest_id, dest_lat, dest_lon = dest_row

    graph = get_location_graph()
    path_ids, total_distance = dijkstra(graph, start_id, dest_id)

    if not path_ids:
        print("⚠️ No route found.")
        return

    coordinates = []
    for loc_id in path_ids:
        cursor.execute("SELECT latitude, longitude FROM locations WHERE id = %s", (loc_id,))
        lat, lon = cursor.fetchone()
        coordinates.append(f"{lat},{lon}")

    base_url = "https://www.google.com/maps/dir/?api=1"
    origin = f"{start_lat},{start_lon}"
    destination = f"{dest_lat},{dest_lon}"
    maps_link = f"{base_url}&origin={origin}&destination={destination}"
    
    print(f"Google Maps: {maps_link}")
    webbrowser.open(maps_link)
    cursor.close()
    connection.close()
