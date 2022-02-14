# Three

## Indice

1. [Introduzione](#1-introduzione)
2. [Struttura Progetto](#2-struttura-progetto)
3. [Requisiti Per Eseguire Il Progetto](#3-requisiti-per-eseguire-il-progetto)
4. [Sviluppi Futuri](#4-sviluppi-futuri)

## 1. Introduzione

Il seguente progetto è stato creato dal seguente gruppo chiamato *Three*:

- Vittoria Stella
- Simone Cocozza
- Giacomo Mauro


Il progetto è stato creato per sostenere l'esame di *Ingegneria Della Conoscenza*.

## 2. Struttura Progetto

Il progetto è strutturato nel seguente modo:

```
|–– bike 
|    |–– BikePrice.py
|    |-- BikePrices.csv
|    |–– createKB.py
|    |-- knowledgeBase.pl
|    |–– useKb.py
|-- documentazione.pdf
|–– README.md
|–– requirements.txt
```

Nel seguito si dettagliano i ruoli dei diversi componenti:

- **bike**: la cartella principale del progetto, in cui è scritto tutto il codice dell’applicazione:
  - **BikePrice.py**: file sorgente utilizzato per eseguire le predizioni del prezzo di una moto;
  - **createKB.py**: file sorgente utilizzato per costruire la *KB* che si trova nel percorso `../bike/knowledgeBase.pl`;
  - **useKb.py** file sorgente utilizzato per interfacciarsi con la *KB*, in particolar modo questo file utilizza la base di conoscenza che si trova nel percorso `data/knowledgeBase.pl` per rispondere alle domande dell'utente;
- **documentazione.pdf**: documentazione del caso di studio;
- **requirements.txt**: file utilizzato per specificare le librerie necessarie per costruire il `virtual enviroment (venv)` per poter eseguire il progetto.

## 3. Requisiti Per Eseguire Il Progetto

Per eseguire il progetto è necessario installare i seguenti programmi:

- `Python 3.9.1`
- `SWI-Prolog 8.2.4`

Una volta scaricato il progetto dal sistema di controllo versione, per poterlo eseguire è necessario aprire il `terminale`, spostarsi sulla `cartella del progetto` e digitare i seguenti comandi:

- `$ python -m venv venv`
- `$ venv\Scripts\activate`
- `$ pip freeze > requirements.txt'
- `$ pip install -r requirements.txt`

## 4. Sviluppi Futuri

In futuro, il nostro progetto potrebbe essere utilizzato da aziende motociclistiche per facilitare e velocizzare la ricerca del prezzo (predetto) della moto a cui l'utente aspira, tenendo conto delle caratteristiche che questo voglia che la sua moto abbia.
