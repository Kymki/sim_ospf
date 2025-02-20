import heapq
"""La libreria heapq in Python fornisce una coda di priorità basata su un min-heap, 
che è una struttura dati dove il valore minimo sta in cima. Serve per estrarre il nodo con il costo minore a ogni iterazione.
Le operazioni principali di heapq sono:
heappush(heap, item) → Inserisce un elemento nella heap in O(log n)
heappop(heap) → Estrae l'elemento minimo in O(log n) ottimizzando l'algoritmo di Djkistra che altrimenti sarebbe O(n) lineare
heapify(iterable) → Trasforma una lista in una heap in O(n)
"""
import networkx as nx
"""La libreria networkx ci servià per implementare la visualizzazione
grafica del grafo, in particolare per disegnare i nodi e gli archi del grafo."""
import matplotlib.pyplot as plt
"""La libreria matplotlib.pyplot ci servirà per visualizzare il grafo."""
import json
"""La libreria json ci servirà per caricare la topologia della rete da un file JSON."""
from collections import defaultdict
"""La libreria collections ci servirà per creare un dizionario con valori di default."""



# Implementa l'algoritmo di Dijkstra per trovare il percorso più breve da un nodo sorgente a tutti gli altri nodi della rete

def dijkstra(graph, start):
    # Creiamo una coda con priorità (min-heap) per gestire i nodi da esplorare
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # Inseriamo il nodo iniziale con distanza 0
    
    # Dizionario per memorizzare le distanze minime da start a ogni altro nodo, inizializzate a +infinito
    distances = {router: float('inf') for router in graph}
    distances[start] = 0  # La distanza del nodo di partenza è zero 0
    
    # Dizionario per memorizzare il predecessore di ciascun nodo nel percorso più breve
    previous_nodes = {router: None for router in graph}
    
    while priority_queue:
        # Estrai il nodo con la distanza minore dalla coda con priorità (heap min-heap)
        current_distance, current_router = heapq.heappop(priority_queue)
        
        # Esplora i vicini del nodo corrente
        for neighbor, weight in graph[current_router].items():
            distance = current_distance + weight  # Calcola la nuova distanza provvisoria
            
            # Se il nuovo percorso è più breve, aggiorna la distanza e il predecessore
            if distance < distances[neighbor]:
                distances[neighbor] = distance 
                previous_nodes[neighbor] = current_router
                heapq.heappush(priority_queue, (distance, neighbor))  # Aggiunge il nodo con priorità aggiornata
    
    return distances, previous_nodes

# Ricostruisce il percorso più breve tra due nodi utilizzando le informazioni sui nodi precedenti

def shortest_path(previous_nodes, start, end): # Funzione che restituisce il percorso più breve tra due nodi
    path = [] # Inizializzazione della lista del percorso
    current = end 
    
    # Si parte dal nodo di destinazione e si risale fino al nodo di partenza perche il dizionario previous_nodes contiene i nodi precedenti.
    while current is not None:
        path.insert(0, current)  # Inserisce il nodo all'inizio della lista per mantenere l'ordine corretto
        current = previous_nodes[current] # Si sposta al nodo precedente
    
    """ Verifica che il percorso sia valido (ovvero che inizi dal nodo di partenza) importante 
    perchè se il nodo di destinazione non è raggiungibile da start, il percorso sarà vuoto!! """

    return path if path[0] == start else []

# Funzione per la simulazione di guasti di un router, da utilizzare facoltativamente (aggiornata).

def simulate_failure(graph, failed_router):
    if failed_router in graph:
        del graph[failed_router]  # Serve a simulare il guasto di un router, se lo desideriamo
        for router in graph:
            graph[router].pop(failed_router, None)  # Poppa eventuali riferimenti al router guasto dalla topologia.
    

# Visualizza la rete e il percorso più breve utilizzando networkx e matplotlib
def draw_network(graph, path=[]):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    
    # Posizionamento automatico dei nodi 
    pos = nx.spring_layout(G) 
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    
    # Disegna la rete con i nodi e gli archi
    plt.figure(figsize=(8, 6)) 
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10) 
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) 
    
    # Evidenzia il percorso più breve trovato
    if path:
        path_edges = list(zip(path, path[1:])) 
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.show()

# Carica la topologia della rete da un file JSON

def load_network_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Funzione principale che avvia l'algoritmo, gestisce la simulazione di guasti e visualizza i risultati

def main():
    start = 'R1'  # Nodo di partenza per l'algoritmo di Dijkstra
    
    # Carica la rete da un file JSON, se disponibile, altrimenti prosegui con quello di default, usato nei test.
    try:
        network = load_network_from_json('network.json')
    except FileNotFoundError:
        print("File di rete non trovato. Usando la rete di default.")
        network = {
            'R1': {'R2': 10, 'R3': 3},
            'R2': {'R1': 10, 'R3': 1, 'R4': 2},
            'R3': {'R1': 3, 'R2': 1, 'R4': 8, 'R5': 2},
            'R4': {'R2': 2, 'R3': 8, 'R5': 4},
            'R5': {'R3': 2, 'R4': 4}
        } 
    
    """ Simula il guasto del router specificato, da commentare se non è necessario."""
    #failure = 'R4'  # Simula il guasto del router
    #simulate_failure(network, failure)
    #""" Se il router guasto è il nodo di partenza, l'algoritmo non può essere eseguito e termina."""
    #if failure == start:
    #    print(f"❌❌❌❌❌❌ {failure} è guasto, il responsabile della rete non ha previsto un failover e verrà licenziato 🚀 .")
    #    return   
    
    # Esegue l'algoritmo di Dijkstra per trovare i percorsi più brevi 
    distances, previous_nodes = dijkstra(network, start) 
    
    # Stampa i percorsi più brevi e li visualizza 
    for target in network:
        if target != start: 
            if distances[target] == float('inf'): # Se la distanza è infinita, il nodo non è raggiungibile (inserita solo per scopi didattici)
                print(f"Il router {target} non è raggiungibile da {start}.")
            else:
                path = shortest_path(previous_nodes, start, target)
                print(f"Percorso più breve da {start} a {target}: {path} con costo {distances[target]}") # Stampa il percorso più breve
                draw_network(network, path)

# Here we go! 🚀
if __name__ == "__main__":
    main() 
