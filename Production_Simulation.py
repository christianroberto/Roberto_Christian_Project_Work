import random

# Creazione dizionario annidato per definizione dei prodotti e delle varie fasi in base al prodotto. 
# In questo modo sarà possibile modificare i tempi e le modalità di produzione necessari alle fasi comodamente, ed eventualmente aggiungere nuovi prodotti 

PRODOTTI = {
    "Limoni": {
        "tipo": "agrumi",								#Tipologia di prodotto
        "fase1_nome": "Crescita del porta innesto",  	# fase di crescita del porta innesto - limone volkameriano
        "fase1_giorni": 700,  							#Durata indicativa della fase alla quale verrà aggiunta la variabilità
        "fase2_nome": "Innesto e crescita in vaso", 	# fase durante la quale avviene l'innesto e il travaso nel vaso definitivo, in attesa della crescita e fruttificazione
        "fase2_giorni": 720  							#Durata indicativa della fase alla quale verrà aggiunta la variabilità
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
        "fase1_nome": "Propagazione per talea",			#fase di propagazione per talea - Prelevamento del ramo dall'albero madre e coltivazione in serra
        "fase1_giorni": 60,
        "fase2_nome": "Crescita e allevamento in vaso",	#Fase di travaso e crescita fino alla fruttificazione
        "fase2_giorni": 540
    }
}

#Definizione della funzione per la conversione dei giorni in anni. Prende in input il numero totale di giorni necessari al
#completamento delle fasi e restituisce in output il valore convertito in anni,mesi e giorni.
#Viene utilizzata per una corretta restituzione degli output temporali tramite semplici operazioni matematiche di divisione e modulo.

def giorni_in_anni(giorni):	
    anni = giorni // 365		    #Divisione per estrapolare il valore intero degli anni.
    giorni_restanti = giorni % 365	    #Operazione di modulo che calcola il resto della divisione dei giorni per 365. Così vengono calcolati i giorni esclusi dalla divisione intera precedente
    mesi = giorni_restanti // 30	    #I giorni rimanenti vengono a loro volta divisi per 30, calcolando in questo modo il numero di mesi
    giorni_finali = giorni_restanti % 30    #Operazione di modulo che calcola il resto della divisione dei giorni rimanenti per 30. Così vengono calcolati i giorni esclusi dalla divisione intera precedente
    return anni, mesi, giorni_finali	    #L'operazione è completa, quindi la funzione restituisce il valore iniziale dei giorni convertito in anni, mesi e giorni


# Definizione della funzione che serve a introdurre la variabilità. Prende in input il valore base da modificare, e la percentuale di variabilità richiesta.
# Restituisce come output il valore base moltiplicato per il tasso di variabilità
#Verrà utilizzata per introdurre variabilità nella durata delle fasi.

def applica_variabilita(valore_base, percentuale):
    return int(valore_base * random.uniform(1 - percentuale, 1 + percentuale))	#random.uniform è una funzione del modulo random che genera un valore reale casuale tra il primo valore e il secondo. 


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
    qualita_serra = random.uniform(0.91, 1.00)					#Istruzione che serve a calcolare il tasso qualitativo della serra, che influirà sulla sopravvivenza delle piante.		
    durata = applica_variabilita(durata_base, 0.15)				#Istruzione per il calcolo della durata della fase, comprensivo di variabilità
    tasso_base = random.uniform(0.95, 1.00)					#Istruzione per il calcolo del tasso di sopravvivenza dovuto a fattori esterni alla serra
    tasso_finale = tasso_base * qualita_serra					#Istruzione per il calcolo del tasso complessivo di sopravvivenza alla fase
    piante_pronte = int(quantita_iniziale * tasso_finale)			#Istruzione per il calcolo delle piante sopravvissute alla fase di propagazione per talea
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

    return {						    #La funzione restituisce un dizionario strutturato con i valori di output, che in alcuni casi vengono "lavorati" ancora
        "prodotto": nome_prodotto,
        "quantita_iniziale": quantita_iniziale,
        "fase1_nome": prodotto["fase1_nome"],
        "fase1_durata": giorni_in_anni(durata_fase1),				#Il valore in questo caso viene convertito tramite la funzione apposita
        "qualita_serra": qualita_serra,
        "sopravvissute_fase1": piante_post_fase1,
        "fase2_nome": prodotto["fase2_nome"],
        "fase2_durata": giorni_in_anni(durata_fase2),				#Il valore in questo caso viene convertito tramite la funzione apposita
        "piante_pronte": piante_finali,
        "durata_totale": giorni_in_anni(durata_totale)				#Il valore in questo caso viene convertito tramite la funzione apposita
    }


# La parte che segue utilizza una semplice struttura iterativa di tipo "for", richiamando poi la funzione principale di simulazione.
# Dopodiché scrive a schermo tutti gli output del programma 

for prodotto in PRODOTTI:
    r = simula_produzione(prodotto)

    print(f"\nProdotto: {r['prodotto']}")
    print(f"Quantità inizialmente prevista: {r['quantita_iniziale']} piante")

    a, m, g = r["fase1_durata"]
    print(f"  {r['fase1_nome']}: {a} anni, {m} mesi, {g} giorni")

    if r["qualita_serra"] is not None:
        print(f"  Livello di qualità della serra: {r['qualita_serra']:.2f}")

    print(f"  Piante sopravvissute dopo questa fase: {r['sopravvissute_fase1']}")

    a, m, g = r["fase2_durata"]
    print(f"  {r['fase2_nome']}: {a} anni, {m} mesi, {g} giorni")

    print(f"  Piante pronte per la commercializzazione: {r['piante_pronte']}")

    a, m, g = r["durata_totale"]
    print(f"Durata totale del processo: {a} anni, {m} mesi, {g} giorni")
