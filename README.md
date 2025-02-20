# Algoritmo di Dijkstra con heapq

## Descrizione
Questo codice implementa l'algoritmo di **Dijkstra** per trovare il **cammino minimo** da un nodo sorgente a tutti gli altri nodi in un **grafo pesato**.

Utilizza la libreria `heapq` per gestire una **coda di priorità** in modo efficiente.

---

## Funzioni principali
- **`dijkstra(graph, start)`**: Implementa l'algoritmo di Dijkstra.
  - Inizializza le distanze con infinito.
  - Usa una coda di priorità (`heapq`) per estrarre il nodo con distanza minima.
  - Aggiorna le distanze dei vicini se trova un percorso più breve.
  - Restituisce un dizionario con le distanze minime dal nodo sorgente.

- **`heapq.heappush(heap, item)`**: Inserisce un elemento nella heap.
- **`heapq.heappop(heap)`**: Estrae l'elemento con valore minimo.

---

## Struttura del codice
1. **Definizione del grafo**: Utilizza un dizionario di dizionari per rappresentare i nodi e i pesi degli archi.
2. **Applicazione dell'algoritmo**: Viene chiamata la funzione `dijkstra()` con un nodo di partenza.
3. **Stampa dei risultati**: Mostra le distanze minime calcolate.

---

## Utilizzo
Per eseguire il codice, basta definire un grafo e chiamare la funzione `dijkstra()` con il nodo di partenza desiderato. 

Esempio di output:
```
{'A': 0, 'B': 1, 'C': 3, 'D': 4}
```

Il risultato indica le distanze minime dal nodo `A` a tutti gli altri nodi del grafo.

## Failures
E' stata inserita la possibilità di simulare il guasto di un router (nodo), basta decommentare le parti relative alla funzione "simulate_failure".

---