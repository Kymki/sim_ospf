# Simulazione del Protocollo OSPF con l'Algoritmo di Dijkstra

## Introduzione
Questo progetto implementa una simulazione del protocollo OSPF (Open Shortest Path First) utilizzando l'algoritmo di Dijkstra per calcolare i percorsi minimi tra i router di una rete. Il codice permette anche di visualizzare la rete e i percorsi più brevi utilizzando la libreria NetworkX.

## Algoritmo di Dijkstra
L'algoritmo di Dijkstra viene utilizzato per trovare il percorso più breve da un nodo sorgente a tutti gli altri nodi in un grafo pesato. Il funzionamento è il seguente:
1. Inizializza le distanze di tutti i nodi a infinito, tranne il nodo sorgente che ha distanza zero.
2. Usa una coda di priorità per selezionare il nodo con la distanza minore.
3. Aggiorna le distanze dei nodi adiacenti se il nuovo percorso trovato è più breve.
4. Ripeti il processo fino a che tutti i nodi siano stati visitati.

## Implementazione
### Struttura della Rete
La rete è rappresentata come un dizionario Python dove le chiavi sono i nomi dei router e i valori sono i loro collegamenti con i relativi pesi.

Esempio:
```python
network = {
    'R1': {'R2': 10, 'R3': 3},
    'R2': {'R1': 10, 'R3': 1, 'R4': 2},
    'R3': {'R1': 3, 'R2': 1, 'R4': 8, 'R5': 2},
    'R4': {'R2': 2, 'R3': 8, 'R5': 4},
    'R5': {'R3': 2, 'R4': 4}
}
```

### Funzioni Principali
#### `dijkstra(graph, start)`
Questa funzione calcola i percorsi più brevi dal router di partenza a tutti gli altri router.

#### `shortest_path(previous_nodes, start, end)`
Ricostruisce il percorso più breve da un nodo sorgente a un nodo di destinazione.

#### `simulate_failure(graph, failed_router)`
Simula il guasto di un router rimuovendolo dalla rete.

#### `draw_network(graph, path=[])`
Genera un grafico della rete utilizzando NetworkX e evidenzia il percorso minimo calcolato.

## Simulazione
Il codice simula il router `R1` che calcola il percorso più breve verso tutti gli altri router della rete.

Esempio di output:
```
Percorso più breve da R1 a R2: ['R1', 'R3', 'R2'] con costo 4
Percorso più breve da R1 a R3: ['R1', 'R3'] con costo 3
Percorso più breve da R1 a R4: ['R1', 'R3', 'R2', 'R4'] con costo 6
Percorso più breve da R1 a R5: ['R1', 'R3', 'R5'] con costo 5
```

Inoltre, vengono generati grafici che mostrano la rete con il percorso più breve evidenziato in rosso.

##

