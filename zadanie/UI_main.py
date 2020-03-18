import copy # kopirujem 2d listy prvok po prvku, a nie adresu, potrebne aby som neprepisoval mapy, ktore nechcem
import heapq # kniznica na pouzitie heapu

class StavMapy: # classa, ktorou si reprezentuje jedne prvok heapu, prvky su usporiadane podla premenej pocetRoznych
    def __init__(self, mapa, pocetRoznych, operacia, predosli):
        self.mapa = copy.deepcopy(mapa) # 2d list reprezentuje mapu a jej aktualny stav
        self.pocetRoznych = pocetRoznych # pocet policok, ktore su na roznom mieste od koncoveho stavu
        self.operacia = operacia # slovo operacie, ktora sa vykonala na prazdne policko
        self.predosli = predosli # odkaz na objekt Stav mapy z ktoreho bola mapa v tomto objekte vygenerovana
    def __lt__(self, other): # potrebna funkcia na porovnovanie v heape. ficura pythonu
        return self.pocetRoznych < other.pocetRoznych


minHeap1 = [] # halda, do ktorej vhadzujem vsetky stavy mapy, ktore som vygeneroval a neboli pouzite, usporiadanie podla hodnoty pocetRoznych v classe StavMapy, heuristika1
minHeap2 = [] # halda, do ktorej vhadzujem vsetky stavy mapy, ktore som vygeneroval a neboli pouzite, usporiadanie podla hodnoty pocetRoznych v classe StavMapy, heuristika2
hashSet = set() # tento set funguje ako hash tabulka, len bez hodnotou pre kluce, z dovodu, ze sem  nebudem davat duplikaty
riadokNula = stlpecNula = 0 # globalne premenne, ktore mi drzia suradnice, kde sa nachadza 0, teda prazdne policko
pocetSpracovanychUzlov = pocetVytvorenychUzlov = int(0)


def vypisMapu(mapa): # funkcia, ktorou si vypisujem mapu, pouzival som hlavne pri debugovani
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            print(mapa[i][j], end=" ")
        print("")


def zistiPocetRoznych(obmena, mapaKoniec): # funkcia mi zisti pocet policok, ktore v aktualnom stave nie su na tom mieste ako maju byt v koncovom
    pocetRoznychFunkcia = 0
    for i in range(len(mapaKoniec)):
        for j in range(len(mapaKoniec[i])):
            if (mapaKoniec[i][j] is not obmena[i][j]):
                pocetRoznychFunkcia = pocetRoznychFunkcia + 1

    return pocetRoznychFunkcia

# tato funkcia zisti ako ďaleko sa nachadzaju jednotlive policka aktualneho stavu od svojej koncovej pozicie
def zistiPocetRoznychVzdialenost(obmena, mapaKoniec):
    zhoda = False
    vzdialenost = 0
    for i in range(len(obmena)):
        for j in range(len(obmena[i])):
            zhoda = False
            for k in range(len(mapaKoniec)):
                for l in range(len(mapaKoniec[k])):
                    if obmena[i][j] == mapaKoniec[k][l]:
                        zhoda = True
                        vzdialenostX = vzdialenostY = 0
                        if i - k < 0:
                            vzdialenostX = (i - k) * (-1)
                        else:
                            vzdialenostX = (i - k)
                        if j - l < 0:
                            vzdialenostY = (j - l) * (-1)
                        else:
                            vzdialenostY = (j - l)
                        vzdialenost = vzdialenost + vzdialenostX + vzdialenostY
                if zhoda:
                    break

    return vzdialenost

# funkcia zisti, na ktorom mieste v mape sa nachadza 0, teda prazdne policko a zmeni hodnoty globalnym premenam, ktore maju ulohu drzat jej suradnice
def zistiPoziciuNula(mapaZaciatok):
    global riadokNula, stlpecNula
    for i in range(len(mapaZaciatok)):
        for j in range(len(mapaZaciatok[i])):
            if (mapaZaciatok[i][j] is 0):
                riadokNula = i
                stlpecNula = j


def vytvorStringMapa(mapa): # z mapy mi tato funkcia vytvori string, ktory potom hashujem a vhladam do hashSetu aby som vedel, ktore mapy uz boli vygenerovane a pouzite
    string = ""
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            string = string + str(mapa[i][j])

    return string

#
# tieto 4 funkcie sluzia na posuvanie neprazdneho policka na prazdne aby sa vygenerovala nova mapa
#
def zmenaMinusRiadok(obmena, mapaZaciatok):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula - 1][stlpecNula]
    obmena[riadokNula - 1][stlpecNula] = 0
    return obmena


def zmenaPlusRiadok(obmena, mapaZaciatok):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula + 1][stlpecNula]
    obmena[riadokNula + 1][stlpecNula] = 0
    return obmena


def zmenaMinusStlpec(obmena, mapaZaciatok):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula][stlpecNula - 1]
    obmena[riadokNula][stlpecNula - 1] = 0
    return obmena


def zmenaPlusStlpec(obmena, mapaZaciatok):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula][stlpecNula + 1]
    obmena[riadokNula][stlpecNula + 1] = 0
    return obmena

# funkcia vyskusa, ci je mozne posunut prazdne policko o 1 vyssie v riadku
# pocitac reprezentuje maticu od vrchu, takze sa vymeni prazdne policko s tym nad nim, ale iba ak to je mozne a nepojde prazdne policko mimo maticu
# v hre sa takato akcia reprezentuje ako posun neprazdneho policka na prazdne
def skusMinusRiadok(vytiahnuteHeap, mapaKoniec, heuristika2):
    global pocetVytvorenychUzlov
    if (riadokNula - 1 >= 0):
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa)
        obmenaMapy = zmenaMinusRiadok(obmenaMapy, vytiahnuteHeap.mapa)
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__()
        if hashObmeny not in hashSet:
            pocetVytvorenychUzlov = pocetVytvorenychUzlov + 1
            if heuristika2:
                pocetRoznychFunkcia = int(zistiPocetRoznychVzdialenost(obmenaMapy, mapaKoniec))
                heapq.heappush(minHeap2, StavMapy(obmenaMapy, pocetRoznychFunkcia, "DOLE", vytiahnuteHeap))
            else:
                pocetRoznychFunkcia = int(zistiPocetRoznych(obmenaMapy, mapaKoniec))
                heapq.heappush(minHeap1, StavMapy(obmenaMapy, pocetRoznychFunkcia, "DOLE", vytiahnuteHeap))

# funkcia vyskusa, ci je mozne posunut prazdne policko o 1 nizsie v riadku
# pocitac reprezentuje maticu od vrchu, takze sa vymeni prazdne policko s tym pod nim, ale iba ak to je mozne a nepojde prazdne policko mimo maticu
# v hre sa takato akcia reprezentuje ako posun neprazdneho policka na prazdne
def skusPlusRiadok(vytiahnuteHeap, mapaKoniec, heuristika2):
    global pocetVytvorenychUzlov
    if (riadokNula + 1 < len(vytiahnuteHeap.mapa)):
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa)
        obmenaMapy = zmenaPlusRiadok(obmenaMapy, vytiahnuteHeap.mapa)
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__()
        if hashObmeny not in hashSet:
            pocetVytvorenychUzlov = pocetVytvorenychUzlov + 1
            if heuristika2:
                pocetRoznychFunkcia = int(zistiPocetRoznychVzdialenost(obmenaMapy, mapaKoniec))
                heapq.heappush(minHeap2, StavMapy(obmenaMapy, pocetRoznychFunkcia, "HORE", vytiahnuteHeap))
            else:
                pocetRoznychFunkcia = int(zistiPocetRoznych(obmenaMapy, mapaKoniec))
                heapq.heappush(minHeap1, StavMapy(obmenaMapy, pocetRoznychFunkcia, "HORE", vytiahnuteHeap))

# funkcia vyskusa, ci je mozne posunut prazdne policko o 1 do lava v stlpci, musi skontrolovat, ci nejde mimo maticu
# v hre sa takato akcia reprezentuje ako posun neprazdneho policka na prazdne
def skusMinusStlpec(vytiahnuteHeap, mapaKoniec, heuristika2):
    global pocetVytvorenychUzlov
    if (stlpecNula - 1 >= 0):
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa)
        obmenaMapy = zmenaMinusStlpec(obmenaMapy, vytiahnuteHeap.mapa)
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__()
        if hashObmeny not in hashSet:
            pocetVytvorenychUzlov = pocetVytvorenychUzlov + 1
            if heuristika2:
                pocetRoznychFunkcia = int(zistiPocetRoznychVzdialenost(obmenaMapy, mapaKoniec))
                heapq.heappush(minHeap2, StavMapy(obmenaMapy, pocetRoznychFunkcia, "VPRAVO", vytiahnuteHeap))
            else:
                pocetRoznychFunkcia = int(zistiPocetRoznych(obmenaMapy, mapaKoniec))
                heapq.heappush(minHeap1, StavMapy(obmenaMapy, pocetRoznychFunkcia, "VPRAVO", vytiahnuteHeap))

# funkcia vyskusa, ci je mozne posunut prazdne policko o 1 do prava v stlpci, musi skontrolovat, ci nejde mimo maticu
# v hre sa takato akcia reprezentuje ako posun neprazdneho policka na prazdne
def skusPlusStlpec(vytiahnuteHeap, mapaKoniec, heuristika2):
    global pocetVytvorenychUzlov
    if (stlpecNula + 1 < len(vytiahnuteHeap.mapa[riadokNula])):
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa)
        obmenaMapy = zmenaPlusStlpec(obmenaMapy, vytiahnuteHeap.mapa)
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__()
        if hashObmeny not in hashSet:
            pocetVytvorenychUzlov = pocetVytvorenychUzlov + 1
            if heuristika2:
                pocetRoznychFunkcia = int(zistiPocetRoznychVzdialenost(obmenaMapy, mapaKoniec))
                heapq.heappush(minHeap2, StavMapy(obmenaMapy, pocetRoznychFunkcia, "VLAVO", vytiahnuteHeap))
            else:
                pocetRoznychFunkcia = zistiPocetRoznych(obmenaMapy, mapaKoniec)
                heapq.heappush(minHeap1, StavMapy(obmenaMapy, pocetRoznychFunkcia, "VLAVO", vytiahnuteHeap))

# funkcia najprv vytiahne prvok z heapu, kde je najmensi pocet roznych prvkov na mape od koncoveho stavu
# ak je heap prazdny, tak taketo zadanie nema riesenie
# ked heap nie je prazdny, tak funkcia skontroluje, ci uz nahodou nie sme v koncovom stave, ak ano, tak skonci a vrati posledny stav
# ak nie sme v koncovom stave, tak tento stav prida do hashSetu, aby sa uz dalej nevkladal do heapu ak nahodou vznikne
# nasledne zisti poziciu 0 a skusa vsetky 4 mozne posuny prazdneho policka v mape
# na konci vrati prvok, ktory bol vytiahnuty z heapu aby si cyklus v ktorom sa spusta vedel urcit, ci ma skoncit alebo nie
def skusaj(mapaKoniec, heuristika2):
    global pocetSpracovanychUzlov
    if heuristika2:
        try:
            vytiahnuteHeap = heapq.heappop(minHeap2)
            pocetSpracovanychUzlov = pocetSpracovanychUzlov + 1
        except IndexError: # tento error vyhodi, ked je prazdny heap
            return None
        vytiahnuteRozne = zistiPocetRoznychVzdialenost(vytiahnuteHeap.mapa, mapaKoniec)
    else:
        try:
            vytiahnuteHeap = heapq.heappop(minHeap1)
            pocetSpracovanychUzlov = pocetSpracovanychUzlov + 1
        except IndexError: # tento error vyhodi, ked je prazdny heap
            return None
        vytiahnuteRozne = zistiPocetRoznych(vytiahnuteHeap.mapa, mapaKoniec)
    if vytiahnuteRozne is 0:
        return vytiahnuteHeap
    hashSet.add(vytvorStringMapa(vytiahnuteHeap.mapa).__hash__())
    zistiPoziciuNula(vytiahnuteHeap.mapa)
    skusMinusRiadok(vytiahnuteHeap, mapaKoniec, heuristika2)
    skusPlusRiadok(vytiahnuteHeap, mapaKoniec, heuristika2)
    skusMinusStlpec(vytiahnuteHeap, mapaKoniec, heuristika2)
    skusPlusStlpec(vytiahnuteHeap, mapaKoniec, heuristika2)
    return vytiahnuteHeap


def vypisPostupu(poslednyVytiahnuty):
    rovnake = True
    pocetKrokov = 0
    if poslednyVytiahnuty is not None:
        rovnake = False
        postupnost2 = []
        print("Ukoncena postupnost:")
        while poslednyVytiahnuty is not None:
            pocetKrokov = pocetKrokov + 1
            postupnost2.append(poslednyVytiahnuty.operacia)
            poslednyVytiahnuty = poslednyVytiahnuty.predosli
        for prvok2 in reversed(postupnost2):
            print(prvok2)
        print("")
    else:
        rovnake = False
        print("Nema riesenie.")

    print("Pocet krokov: " + str(pocetKrokov))
    print("Pocet spracovanych uzlov " + str(pocetSpracovanychUzlov))
    print("Pocet vygenerovanych uzlov " + str(pocetVytvorenychUzlov))

    if rovnake:
        print("Zaciatocny stav je koncovy.")
        vypisMapu(mapaZaciatok)

# mapaKoniec = [[1, 2, 3],
#               [4, 5, 6],
#               [7, 8, 0]]
# mapaZaciatok = [[7, 8, 6],
#                 [5, 4, 3],
#                 [2, 0, 1]]
# mapaKoniec = [[1, 2, 3],
#               [4, 6, 5],
#               [7, 8, 0]]
# mapaZaciatok = [[1, 3, 6],
#                 [4, 8, 0],
#                 [7, 5, 2]]
# mapaZaciatok = [[1, 2, 3],
#                 [0, 4, 5],
#                 [6, 7, 8]]
# mapaKoniec = [[1, 2, 3],
#               [4, 5, 6],
#               [7, 8, 0]]
# mapaZaciatok = [[1, 2, 5],
#                 [3, 4, 6],
#                 [7, 8, 0]]
# mapaKoniec = [[1, 2, 3],
#               [4, 5, 6],
#               [7, 8, 0]]
mapaZaciatok = [[2, 3, 4],
                [5, 1, 6],
                [7, 8, 0]]
mapaKoniec = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

heuristika2 = koniec = False
while(koniec is False):
    if heuristika2 is False:
        print("Riesim heuristika 1.")
        pocetRoznych = zistiPocetRoznych(mapaZaciatok, mapaKoniec)
        poslednyVytiahnuty = StavMapy(mapaZaciatok, pocetRoznych, "Zaciatok", None)
        heapq.heappush(minHeap1, poslednyVytiahnuty)  # vlozenie heapu na zaciatok
        while(pocetRoznych is not 0):
            poslednyVytiahnuty = skusaj(mapaKoniec, heuristika2)
            if poslednyVytiahnuty is None:
                break
            pocetRoznych = poslednyVytiahnuty.pocetRoznych
        hashSet.clear()
        heuristika2 = True
        vypisPostupu(poslednyVytiahnuty)
        pocetSpracovanychUzlov = pocetVytvorenychUzlov = 0
    else:
        print("\nRiesim heuristika 2")
        pocetRoznych = zistiPocetRoznychVzdialenost(mapaZaciatok, mapaKoniec)
        poslednyVytiahnuty = StavMapy(mapaZaciatok, pocetRoznych, "Zaciatok", None)
        heapq.heappush(minHeap2, poslednyVytiahnuty)
        while(pocetRoznych is not 0):
            poslednyVytiahnuty = skusaj(mapaKoniec, heuristika2)
            if poslednyVytiahnuty is None:
                break
            pocetRoznych = poslednyVytiahnuty.pocetRoznych
        vypisPostupu(poslednyVytiahnuty)
        koniec = True
