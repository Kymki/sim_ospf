import heapq
import networkx as nx
import matplotlib.pyplot as plt

def dijkstra(graph, start):
    """
    Implementazione dell'algoritmo di Dijkstra per trovare il percorso più breve in una rete di router.
    
    Parametri:
    - graph: Dizionario che rappresenta il grafo della rete (router connessi e relativi pesi)
    - start: Nodo di partenza (router sorgente)
    
    Restituisce:
    - distances: Dizionario con le distanze minime dai router
    - previous_nodes: Dizionario per ricostruire il percorso minimo
    """
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    
    # Inizializza le distanze con infinito e il nodo di partenza con 0
    distances = {router: float('inf') for router in graph}
    distances[start] = 0
    
    # Dizionario per tracciare il percorso
    previous_nodes = {router: None for router in graph}
    
    while priority_queue:
        current_distance, current_router = heapq.heappop(priority_queue)
        
        # Se troviamo una distanza maggiore, ignoriamo il nodo
        if current_distance > distances[current_router]:
            continue
        
        # Esaminiamo i vicini del nodo corrente
        for neighbor, weight in graph[current_router].items():
            distance = current_distance + weight
            
            # Se il nuovo percorso è più breve, aggiorniamo la distanza e il percorso
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_router
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, previous_nodes

def shortest_path(previous_nodes, start, end):
    """
    Ricostruisce il percorso più breve dal nodo di partenza `start` al nodo di destinazione `end`.
    
    Parametri:
    - previous_nodes: Dizionario con i predecessori per ogni nodo
    - start: Nodo di partenza
    - end: Nodo di destinazione
    
    Restituisce:
    - Lista con i nodi che compongono il percorso minimo
    """
    path = []
    current = end
    
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
    
    # Se il percorso non parte dal nodo di start, significa che non è raggiungibile
    return path if path[0] == start else []

def simulate_failure(graph, failed_router):
    """
    Simula un guasto rimuovendo un router dalla rete.
    
    Parametri:
    - graph: Dizionario che rappresenta la rete
    - failed_router: Router da rimuovere
    """
    if failed_router in graph:
        del graph[failed_router]
        for router in graph:
            graph[router].pop(failed_router, None)

def draw_network(graph, path=[]):
    """
    Disegna la rete di router con il percorso più breve evidenziato in rosso.
    
    Parametri:
    - graph: Dizionario che rappresenta la rete
    - path: Lista dei nodi che compongono il percorso più breve
    """
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)  # Layout per il posizionamento dei nodi
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.show()

def main():
    """
    Funzione principale per simulare la rete di router e calcolare i percorsi più brevi.
    """
    # Definizione della rete di router con i pesi (costi)
    network = {
        'R1': {'R2': 10, 'R3': 3},
        'R2': {'R1': 10, 'R3': 1, 'R4': 2},
        'R3': {'R1': 3, 'R2': 1, 'R4': 8, 'R5': 2},
        'R4': {'R2': 2, 'R3': 8, 'R5': 4},
        'R5': {'R3': 2, 'R4': 4}
    }

    # Simulazione di un guasto (decommentare per attivarlo)
    # simulate_failure(network, 'R3')

    # Calcolo dei percorsi minimi dal router R1 verso tutti gli altri
    distances, previous_nodes = dijkstra(network, 'R1')

    # Mostrare i percorsi minimi verso i router target
    target_routers = ['R2', 'R3', 'R4', 'R5']
    for target in target_routers:
        path = shortest_path(previous_nodes, 'R1', target)
        print(f'Percorso più breve da R1 a {target}: {path} con costo {distances[target]}')
        draw_network(network, path)

if __name__ == "__main__":
    main()
