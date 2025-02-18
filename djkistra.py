import heapq
import networkx as nx
import matplotlib.pyplot as plt

def dijkstra(graph, start):
    """
    Implementazione dell'algoritmo di Dijkstra per trovare il percorso più breve in una rete di router.
    Dizionario che rappresenta il grafo della rete
    Nodo di partenza (router sorgente)
    Dizionario con le distanze minime dai router e i percorsi
    """
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    
    distances = {router: float('inf') for router in graph}
    distances[start] = 0
    previous_nodes = {router: None for router in graph}
    
    while priority_queue:
        current_distance, current_router = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_router]:
            continue
        
        for neighbor, weight in graph[current_router].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_router
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, previous_nodes

def shortest_path(previous_nodes, start, end):
    """
    Ricostruisce il percorso più breve da start a end.
    """
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
    return path if path[0] == start else []

# Funzione per simulare un guasto a un router
def simulate_failure(graph, failed_router):
    """
    Rimuove un router dalla rete simulando un guasto.
    """
    if failed_router in graph:
        del graph[failed_router]
        for router in graph:
            if failed_router in graph[router]:
                del graph[router][failed_router]

# Funzione per disegnare la rete
def draw_network(graph, path=[]):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.show()

def main():
    # Simulazione della rete di router
    network = {
        'R1': {'R2': 10, 'R3': 3},
        'R2': {'R1': 10, 'R3': 1, 'R4': 2},
        'R3': {'R1': 3, 'R2': 1, 'R4': 8, 'R5': 2},
        'R4': {'R2': 2, 'R3': 8, 'R5': 4},
        'R5': {'R3': 2, 'R4': 4}
    }

    # Simulazione di un guasto (commentare questa linea se non desiderato)
    # simulate_failure(network, 'R3')

    # Simulazione del router R1 che calcola il cammino minimo verso tutti gli altri router
    distances, previous_nodes = dijkstra(network, 'R1')

    # Mostrare i percorsi minimi verso tutti i router
    target_routers = ['R2', 'R3', 'R4', 'R5']
    for target in target_routers:
        path = shortest_path(previous_nodes, 'R1', target)
        print(f'Percorso più breve da R1 a {target}: {path} con costo {distances[target]}')
        draw_network(network, path)

if __name__ == "__main__":
    main()