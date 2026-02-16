import random

# Creazione dizionario annidato per definizione dei prodotti e delle varie fasi in base al prodotto. 
# In questo modo sarà possibile modificare i tempi e le modalità di produzione necessari alle fasi comodamente, ed eventualmente aggiungere nuovi prodotti

PRODOTTI = {
    "Limoni": {
        "tipo": "agrumi",				# Tipologia di prodotto
        "fase1_nome": "Crescita del porta innesto",  	# fase di crescita del porta innesto - limone volkameriano
        "fase1_giorni": 700,  				# Durata indicativa della fase alla quale verrà aggiunta la variabilità
        "fase2_nome": "Innesto e crescita in vaso", 	# fase durante la quale avviene l'innesto e il travaso nel vaso definitivo, in attesa della crescita e fruttificazione
        "fase2_giorni": 720  				# Durata indicativa della fase alla quale verrà aggiunta la variabilità
    },
    "Mandarini": {
        "tipo": "agrumi",
        "fase1_nome": "Crescita del porta innesto",
        "fase1_giorni": 700,
        "fase2_nome": "Innesto e crescita in vaso",
        "fase2_giorni": 720
    },
    "Ulivi": {
        "tipo": "ulivi",
        "fase1_nome": "Propagazione per talea",         #fase di propagazione per talea - Prelevamento del ramo dall'albero madre e coltivazione in serra
        "fase1_giorni": 60,
        "fase2_nome": "Crescita e allevamento in vaso", #Fase di travaso e crescita fino alla fruttificazione
        "fase2_giorni": 540
    }
}

#Definizione della funzione per la conversione dei giorni in anni. Prende in input il numero totale di giorni necessari al
#completamento delle fasi e restituisce in output il valore convertito in anni,mesi e giorni.
#Viene utilizzata per una corretta restituzione degli output temporali tramite semplici operazioni matematiche.

def giorni_in_anni(giorni):
    giorni_per_anno = 365                                                    # Numero di giorni standard in un anno
    giorni_per_mese = 365 / 12                                               # Istruzione che calcola il numero medio di giorni per mese

    anni = int(giorni // giorni_per_anno)                                    # Istruzione che esegue la divisione intera per ottenere il numero di anni completi
    giorni_restanti = giorni - (anni * giorni_per_anno)

    mesi = int(giorni_restanti // giorni_per_mese)
    giorni_finali = int(round(giorni_restanti - (mesi * giorni_per_mese)))

    return anni, mesi, giorni_finali                                        # Restituisce il totale convertito in anni, mesi e giorni

# Definizione della funzione che serve a introdurre la variabilità. Prende in input il valore base da modificare, e la percentuale di variabilità richiesta.
# Restituisce come output il valore base moltiplicato per il tasso di variabilità
#Verrà utilizzata per introdurre variabilità nella durata delle fasi.

def applica_variabilita(valore_base, percentuale):
    return int(valore_base * random.uniform(1 - percentuale, 1 + percentuale))                      #random.uniform è una funzione del modulo random che genera un valore reale casuale tra il primo valore e il secondo. 

# Definizione della funzione per il calcolo della durata e del numero di piante sopravvissute alla fase. 
# Questa viene utilizzata per la fase 1 degli agrumi e per la fase 2 degli agrumi e degli ulivi.
# La funzione prende in input la quantità iniziale, la durata base, la variabilità della durata, il tasso di sopravvivenza minimo e quello massimo.
# Restituisce come output la durata effettiva della fase dopo l'applicazione del tasso di variabilità e il numero di piante sopravvissute alla fase.

def simula_fase_comune(quantita, durata_base, var_durata, sopravvivenza_min, sopravvivenza_max):
    durata = applica_variabilita(durata_base, var_durata)
    tasso = random.uniform(sopravvivenza_min, sopravvivenza_max)
    piante_finali = int(quantita * tasso)
    return durata, piante_finali

# Definizione della funzione specifica per il calcolo della durata della fase di propagazione per talea, del numero di piante pronte per la fase di radicazione e del tasso qualitativo della serra.
# La funzione prende in input la quantità iniziale e la durata media della fase

def simula_fase_propagazione_talea(quantita_iniziale, durata_base):
    qualita_serra = random.uniform(0.91, 1.00)                          #Istruzione che serve a calcolare il tasso qualitativo della serra, che influirà sulla sopravvivenza delle piante.	
    durata = applica_variabilita(durata_base, 0.15)                     #Istruzione per il calcolo della durata della fase, comprensivo di variabilità
    tasso_base = random.uniform(0.95, 1.00)                             #Istruzione per il calcolo del tasso di sopravvivenza dovuto a fattori esterni alla serra
    tasso_finale = tasso_base * qualita_serra                           #Istruzione per il calcolo del tasso complessivo di sopravvivenza alla fase
    piante_pronte = int(quantita_iniziale * tasso_finale)               #Istruzione per il calcolo delle piante sopravvissute alla fase di propagazione per talea
    return durata, piante_pronte, qualita_serra

# Definizione della funzione che simula l'intero processo produttivo.
# Calcola innanzitutto il valore iniziale delle piante, e richiama le
# funzioni di gestione delle fasi al fine di calcolare gli output intermedi e finali, assegnando i valori di variabilità

def simula_produzione(nome_prodotto):					#La funzione viene definita e prende come parametro di input il nome del prodotto
    prodotto = PRODOTTI[nome_prodotto]					#Istruzione che estrae il dizionario del prodotto selezionato

    quantita_iniziale = random.randint(4000, 4100)			#Istruzione che serve a generare la quantità iniziale casuale
    if prodotto["tipo"] == "ulivi":									
        durata_fase1, piante_post_fase1, qualita_serra = simula_fase_propagazione_talea(quantita_iniziale,prodotto["fase1_giorni"])     #Istruzione che chiama la funzione di propagazione per talea utilizzata per gli ulivi e assegna i valori restituiti alle tre variabili indicate 
    else:
        durata_fase1, piante_post_fase1 = simula_fase_comune(quantita_iniziale,prodotto["fase1_giorni"],0.10,0.95,1.00)		#Istruzione che chiama la funzione di simulazione fase comune e assegna i valori restituiti alle due variabili indicate 
        qualita_serra = None
		
    durata_fase2, piante_finali = simula_fase_comune(piante_post_fase1,prodotto["fase2_giorni"],0.02,0.95,1.00)			#Istruzione che chiama la funzione di simulazione fase comune per la seconda fase e assegna i valori restituiti alle due variabili indicate 

    durata_totale = durata_fase1 + durata_fase2						#Istruzione per il calcolo totale della durata delle fasi

    return {                                            #La funzione restituisce un dizionario strutturato con i valori di output, che in alcuni casi vengono "lavorati" ancora
        "prodotto": nome_prodotto,
        "quantita_iniziale": quantita_iniziale,
        "fase1_nome": prodotto["fase1_nome"],
        "fase1_durata_giorni": durata_fase1,            #il valore in questo caso viene restituito nel suo formato "grezzo" (in giorni)
        "fase1_durata": giorni_in_anni(durata_fase1),   #Il valore in questo caso viene convertito tramite la funzione apposita
        "qualita_serra": qualita_serra,
        "sopravvissute_fase1": piante_post_fase1,
        "fase2_nome": prodotto["fase2_nome"], 
        "fase2_durata_giorni": durata_fase2,            #il valore in questo caso viene restituito nel suo formato "grezzo" (in giorni)
        "fase2_durata": giorni_in_anni(durata_fase2),   #Il valore in questo caso viene convertito tramite la funzione apposita
        "piante_pronte": piante_finali,
        "ritardo": 0,
        "durata_totale_giorni": durata_totale,          #il valore in questo caso viene restituito nel suo formato "grezzo" (in giorni)
        "durata_totale": giorni_in_anni(durata_totale)  #Il valore in questo caso viene convertito tramite la funzione apposita
    }

#Parte di esecuzione del programma. Qui vengono richiamte tutte le funzioni precedentemente create e
#eseguite alcune operazioni per i calcoli del ritardo dovuto alla manodopera e alla conversione dei giorni in anni,mesi e giorni.
#Dopodiché si passa al print degli output

risultati = []                                          #Creazione di una lista per salvare i risultati di ciascun prodotto
for prodotto in PRODOTTI:                               #Definizione di un ciclo for per l'esecuzione della simulazione su ciascun prodotto    
    risultati.append(simula_produzione(prodotto))


MANODOPERA = 30                                                                    # Creazione di una costante che definisce il numero di giorni necessari per l'esecuzione dell'innesto su circa 4000 piante da parte degli operai della serra

risultati_ordinati = sorted(risultati, key=lambda x: x["fase1_durata_giorni"])     # Ordinamento dei risultati in base alla durata della prima fase, dal più veloce al più lento
fine_manodopera = risultati_ordinati[0]["fase1_durata_giorni"] + MANODOPERA       # Calcolo della data di fine prevista per la manodopera del primo lotto di piante

for i in range(1, len(risultati_ordinati)):                                        # Ciclo per valutare ogni prodotto successivo nell'ordine della prima fase
    fase1_corrente = risultati_ordinati[i]["fase1_durata_giorni"]                  # Estrazione della durata della prima fase del prodotto corrente
    if fase1_corrente < fine_manodopera:                                           # Controllo se la fase corrente termina prima che la manodopera sia disponibile
        ritardo = fine_manodopera - fase1_corrente                                 # Calcolo del ritardo necessario per iniziare l'innesto
        risultati_ordinati[i]["ritardo"] = ritardo                                  # Assegnazione del ritardo al dizionario del prodotto
        risultati_ordinati[i]["durata_totale_giorni"] += ritardo                    # Aggiornamento della durata totale includendo il ritardo
        risultati_ordinati[i]["fase2_durata_giorni"] += ritardo                     # Aggiornamento della durata della seconda fase includendo il ritardo
        fine_manodopera += MANODOPERA                                              # Aggiornamento della data di fine manodopera per il lotto successivo
    else:
        fine_manodopera = fase1_corrente + MANODOPERA                               # Se non c'è ritardo, la fine manodopera viene aggiornata in base alla durata della fase corrente

for r in risultati:                                                                     # Ciclo per aggiornare le durate convertite in anni, mesi e giorni per tutti i prodotti
    r["fase2_durata"] = giorni_in_anni(r["fase2_durata_giorni"])                     # Conversione della durata della seconda fase in anni, mesi e giorni
    r["durata_totale"] = giorni_in_anni(r["fase1_durata_giorni"] + r["fase2_durata_giorni"])  # Conversione della durata totale in anni, mesi e giorni

for r in risultati:                                                               # Ciclo per stampare i risultati finali della simulazione per ciascun prodotto
    print(f"\nProdotto: {r['prodotto']}")                                         # Stampa del nome del prodotto
    print(f"Quantità inizialmente prevista: {r['quantita_iniziale']} piante")     # Stampa della quantità iniziale generata

    a, m, g = r["fase1_durata"]                                                   # Estrazione della durata della prima fase in anni, mesi e giorni
    print(f"  {r['fase1_nome']}: {a} anni, {m} mesi, {g} giorni")                # Stampa della durata della prima fase

    if r["qualita_serra"] is not None:                                            # Controllo se è presente il livello qualitativo della serra
        print(f"  Livello di qualità della serra: {r['qualita_serra']:.2f}")     # Stampa del livello qualitativo con due decimali

    print(f"  Piante sopravvissute dopo questa fase: {r['sopravvissute_fase1']}") # Stampa del numero di piante sopravvissute dopo la fase 1

    if r["ritardo"] > 0:                                                          # Controllo se c'è stato un ritardo dovuto alla manodopera
        print(f"  Ritardo dovuto alla manodopera per l'innesto: {r['ritardo']} giorni")  # Stampa del ritardo in giorni

    a, m, g = r["fase2_durata"]                                                   # Estrazione della durata della seconda fase in anni, mesi e giorni
    print(f"  {r['fase2_nome']}: {a} anni, {m} mesi, {g} giorni")                # Stampa della durata della seconda fase

    print(f"  Piante pronte per la commercializzazione: {r['piante_pronte']}")    # Stampa del numero di piante pronte per la vendita

    a, m, g = r["durata_totale"]                                                  # Estrazione della durata totale del processo in anni, mesi e giorni
    print(f"Durata totale del processo: {a} anni, {m} mesi, {g} giorni")         # Stampa della durata totale del processo produttivo

