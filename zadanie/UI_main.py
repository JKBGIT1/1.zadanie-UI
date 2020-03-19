import copy # kopirujem 2d listy prvok po prvku, a nie adresu, potrebne aby som neprepisoval mapy, ktore nechcem
import heapq # kniznica na pouzitie heapu

class StavMapy: # classa, ktorou si reprezentuje jeden prvok heapu, prvky su usporiadane podla premenej pocetRoznych
    def __init__(self, mapa, pocetRoznych, operacia, predosli):
        self.mapa = copy.deepcopy(mapa) # 2d list reprezentuje mapu a jej aktualny stav
        self.pocetRoznych = pocetRoznych # pocet policok, ktore su na roznom mieste od koncoveho stavu
        self.operacia = operacia # operacia, ktora bola pouzita na predchadzajuci uzol, aby sme sa dostali do tohto stavu
        self.predosli = predosli # odkaz na objekt Stav mapy z ktoreho bola mapa v tomto objekte vygenerovana
    def __lt__(self, other): # potrebna funkcia na porovnovanie v heape, ficura pythonu
        return self.pocetRoznych < other.pocetRoznych


minHeap1 = [] # halda, do ktorej vhadzujem vsetky stavy mapy, ktore som vygeneroval a neboli pouzite, usporiadanie podla hodnoty pocetRoznych v classe StavMapy, heuristika1
minHeap2 = [] # halda, do ktorej vhadzujem vsetky stavy mapy, ktore som vygeneroval a neboli pouzite, usporiadanie podla hodnoty pocetRoznych v classe StavMapy, heuristika2
hashSet = set() # tento set funguje ako hash tabulka, len bez hodnotou pre kluce, z dovodu, ze sem  nebudem davat duplikaty
riadokNula = stlpecNula = 0 # globalne premenne, ktore mi drzia suradnice, kde sa nachadza 0, teda prazdne policko
pocetSpracovanychUzlov = pocetVytvorenychUzlov = int(0) # premena pocetSpracovanychUzlov mi drzi pocet vygenerovanych a spracovanych uzlov, pocetVytvorenychUzlov mi drzi hodnotu poctu vsetkych vygenerovych uzlov

# funkcia, ktorou si vypisujem mapu, pouzival som hlavne pri debugovani
def vypisMapu(mapa):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            print(mapa[i][j], end=" ")
        print("")

# funkcia mi zisti pocet policok, ktore v aktualnom stave nie su na tom mieste ako maju byt v koncovom
def zistiPocetRoznych(obmena, mapaKoniec):
    pocetRoznychFunkcia = 0
    for i in range(len(mapaKoniec)):
        for j in range(len(mapaKoniec[i])):
            if (mapaKoniec[i][j] is not obmena[i][j]):
                pocetRoznychFunkcia = pocetRoznychFunkcia + 1

    return pocetRoznychFunkcia

# tato funkcia zisti ako ďaleko sa nachadzaju jednotlive policka aktualneho stavu od svojej koncovej pozicie
def zistiPocetRoznychVzdialenost(obmena, mapaKoniec):
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

# z mapy mi tato funkcia vytvori string, ktory potom hashujem a vhladam do hashSetu aby som vedel, ktore mapy uz boli vygenerovane
def vytvorStringMapa(mapa):
    string = ""
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            string = string + str(mapa[i][j])

    return string

# funkcia na vykonanie operacie DOLE
def zmenaMinusRiadok(obmena, mapaZaciatok):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula - 1][stlpecNula]
    obmena[riadokNula - 1][stlpecNula] = 0
    return obmena

# funkcia na vykonanie operacie HORE
def zmenaPlusRiadok(obmena, mapaZaciatok):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula + 1][stlpecNula]
    obmena[riadokNula + 1][stlpecNula] = 0
    return obmena

# funkcia na vykonanie operacie VPRAVO
def zmenaMinusStlpec(obmena, mapaZaciatok):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula][stlpecNula - 1]
    obmena[riadokNula][stlpecNula - 1] = 0
    return obmena

# funkcia na vykonanie operacie VLAVO
def zmenaPlusStlpec(obmena, mapaZaciatok):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula][stlpecNula + 1]
    obmena[riadokNula][stlpecNula + 1] = 0
    return obmena

# funkcia vyskusa, ci sa nad prazdnym polickom nachadza este dalsie, ak ano, tak vykona operaciu DOLE
def skusMinusRiadok(vytiahnuteHeap, mapaKoniec, heuristika2):
    global pocetVytvorenychUzlov
    if (riadokNula - 1 >= 0): # je mozne vykonat operaciu DOLE
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa) # prekopirujem mapu, aby som mohol vykonat operaciu
        obmenaMapy = zmenaMinusRiadok(obmenaMapy, vytiahnuteHeap.mapa) # vykonam operaciu DOLE
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__() # vygenerujem hash pre vzniknutu obmenu
        if hashObmeny not in hashSet: # ak vygenerovany hash z obmeny nie je v hashSete, tak ho mozem hodit do heapu
            pocetVytvorenychUzlov = pocetVytvorenychUzlov + 1
            if heuristika2: # riesim podla druhej heuristiky, zistim vzdialenost jednotlivych policok ku koncu a nasledne ich scita, vytvorim uzol a hodim do heapu
                hashSet.add(hashObmeny) # vygenerovany hash dam do hashSetu, aby som ho znovu nehodil do haldy, ak ho nahodou vygenerujem
                heapq.heappush(minHeap2, StavMapy(obmenaMapy, int(zistiPocetRoznychVzdialenost(obmenaMapy, mapaKoniec)), "DOLE", vytiahnuteHeap))
            else: # resim podla prvej heuristiky, zistim pocet policok, ktore nie su na svojom mieste, vytvorim uzol a hodim do heapu
                hashSet.add(hashObmeny) # vygenerovany hash dam do hashSetu, aby som ho znovu nehodil do haldy, ak ho nahodou vygenerujem
                heapq.heappush(minHeap1, StavMapy(obmenaMapy, int(zistiPocetRoznych(obmenaMapy, mapaKoniec)), "DOLE", vytiahnuteHeap))

# funkcia vyskusa, ci sa pod prazdnym polickom nachadza este dalsie, ak ano, tak vykona operaciu HORE
def skusPlusRiadok(vytiahnuteHeap, mapaKoniec, heuristika2):
    global pocetVytvorenychUzlov
    if (riadokNula + 1 < len(vytiahnuteHeap.mapa)): # je mozne vykonat operaciu HORE
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa) # prekopirujem mapu, aby som mohol vykonat operaciu
        obmenaMapy = zmenaPlusRiadok(obmenaMapy, vytiahnuteHeap.mapa) # vykonam operaciu HORE
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__() # vygenerujem hash pre vzniknutu obmenu
        if hashObmeny not in hashSet: # ak vygenerovany hash z obmeny nie je v hashSete, tak ho mozem hodit do heapu
            pocetVytvorenychUzlov = pocetVytvorenychUzlov + 1
            if heuristika2: # riesim podla druhej heuristiky, zistim vzdialenost jednotlivych policok ku koncu a nasledne ich scita, vytvorim uzol a hodim do heapu
                hashSet.add(hashObmeny) # vygenerovany hash dam do hashSetu, aby som ho znovu nehodil do haldy, ak ho nahodou vygenerujem
                heapq.heappush(minHeap2, StavMapy(obmenaMapy, int(zistiPocetRoznychVzdialenost(obmenaMapy, mapaKoniec)), "HORE", vytiahnuteHeap))
            else: # resim podla prvej heuristiky, zistim pocet policok, ktore nie su na svojom mieste, vytvorim uzol a hodim do heapu
                hashSet.add(hashObmeny) # vygenerovany hash dam do hashSetu, aby som ho znovu nehodil do haldy, ak ho nahodou vygenerujem
                heapq.heappush(minHeap1, StavMapy(obmenaMapy, int(zistiPocetRoznych(obmenaMapy, mapaKoniec)), "HORE", vytiahnuteHeap))

# funkcia vyskusa, ci sa na lavo od prazdneho policka nachazda este dalsie, ak ano, tak vykona operaciu VPRAVO
def skusMinusStlpec(vytiahnuteHeap, mapaKoniec, heuristika2):
    global pocetVytvorenychUzlov
    if (stlpecNula - 1 >= 0): # je mozne vykonat operaciu VPRAVO
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa) # preokopirujem mapu, aby som mohol vykonat operaciu
        obmenaMapy = zmenaMinusStlpec(obmenaMapy, vytiahnuteHeap.mapa) # vykonam operaciu VPRAVO
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__() # vygenerujem hash pre vzniknutu obmenu
        if hashObmeny not in hashSet: # ak vygenerovany hash z obmeny nie je v hashSete, tak ho mozem hodit do heapu
            pocetVytvorenychUzlov = pocetVytvorenychUzlov + 1
            if heuristika2: # riesim podla druhej heuristiky, zistim vzdialenost jednotlivych policok ku koncu a nasledne ich scita, vytvorim uzol a hodim do heapu
                hashSet.add(hashObmeny) # vygenerovany hash dam do hashSetu, aby som ho znovu nehodil do haldy, ak ho nahodou vygenerujem
                heapq.heappush(minHeap2, StavMapy(obmenaMapy, int(zistiPocetRoznychVzdialenost(obmenaMapy, mapaKoniec)), "VPRAVO", vytiahnuteHeap))
            else: # resim podla prvej heuristiky, zistim pocet policok, ktore nie su na svojom mieste, vytvorim uzol a hodim do heapu
                hashSet.add(hashObmeny) # vygenerovany hash dam do hashSetu, aby som ho znovu nehodil do haldy, ak ho nahodou vygenerujem
                heapq.heappush(minHeap1, StavMapy(obmenaMapy, int(zistiPocetRoznych(obmenaMapy, mapaKoniec)), "VPRAVO", vytiahnuteHeap))

# funkcia vyskusa, ci sa na pravo od prazdneho policka nachadza este dalsie, ak ano, tak vykona operaciu VLAVO
def skusPlusStlpec(vytiahnuteHeap, mapaKoniec, heuristika2):
    global pocetVytvorenychUzlov
    if (stlpecNula + 1 < len(vytiahnuteHeap.mapa[riadokNula])): # je mozne vykonat opraciu VLAVO
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa) # preokopirujem mapu, aby som mohol vykonat operaciu
        obmenaMapy = zmenaPlusStlpec(obmenaMapy, vytiahnuteHeap.mapa) # vykonam operaciu VLAVO
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__() # vygenerujem hash pre vzniknutu obmenu
        if hashObmeny not in hashSet: # ak vygenerovany hash z obmeny nie je v hashSete, tak ho mozem hodit do heapu
            pocetVytvorenychUzlov = pocetVytvorenychUzlov + 1
            if heuristika2: # riesim podla druhej heuristiky, zistim vzdialenost jednotlivych policok ku koncu a nasledne ich scita, vytvorim uzol a hodim do heapu
                hashSet.add(hashObmeny) # vygenerovany hash dam do hashSetu, aby som ho znovu nehodil do haldy, ak ho nahodou vygenerujem
                heapq.heappush(minHeap2, StavMapy(obmenaMapy, int(zistiPocetRoznychVzdialenost(obmenaMapy, mapaKoniec)), "VLAVO", vytiahnuteHeap))
            else: # resim podla prvej heuristiky, zistim pocet policok, ktore nie su na svojom mieste, vytvorim uzol a hodim do heapu
                hashSet.add(hashObmeny) # vygenerovany hash dam do hashSetu, aby som ho znovu nehodil do haldy, ak ho nahodou vygenerujem
                heapq.heappush(minHeap1, StavMapy(obmenaMapy, int(zistiPocetRoznych(obmenaMapy, mapaKoniec)), "VLAVO", vytiahnuteHeap))

# funkcia najprv vytiahne uzol z heapu, kde je najmensi pocet roznych prvkov na mape od koncoveho stavu
# ak je heap prazdny, tak taketo zadanie nema riesenie
# ked heap nie je prazdny, tak funkcia skontroluje, ci uz nahodou nie sme v koncovom uzle, ak ano, tak skonci a vrati posledny uzol
# ak nie sme v koncovom uzle, tak zisti poziciu 0 a skusa vsetky 4 operacie
# na konci vrati prvok, ktory bol vytiahnuty z heapu aby si cyklus v ktorom sa spusta vedel urcit, ci ma skoncit alebo nie
def skusaj(mapaKoniec, heuristika2):
    global pocetSpracovanychUzlov
    if heuristika2: # ak sa riesi zadanie podla druhej heuristiky, tak program vytahuje uzol z heapu, ktory je urceny pre druhu heuristiku
        try:
            vytiahnuteHeap = heapq.heappop(minHeap2)
            pocetSpracovanychUzlov = pocetSpracovanychUzlov + 1
        except IndexError: # tento error vyhodi, ked je prazdny heap
            return None
        vytiahnuteRozne = zistiPocetRoznychVzdialenost(vytiahnuteHeap.mapa, mapaKoniec) # zisti vzdialenost jednotlivych policok ku koncu a nasledne ich scita
    else: # inak vytahuje uzol z heapu, ktory je urceny pre prvu heuristiku
        try:
            vytiahnuteHeap = heapq.heappop(minHeap1)
            pocetSpracovanychUzlov = pocetSpracovanychUzlov + 1
        except IndexError: # tento error vyhodi, ked je prazdny heap
            return None
        vytiahnuteRozne = zistiPocetRoznych(vytiahnuteHeap.mapa, mapaKoniec) # zisti pocet policok, ktore este nie su na svojom mieste
    if vytiahnuteRozne is 0: # vytiahnuty uzol je koncovy
        return vytiahnuteHeap
    zistiPoziciuNula(vytiahnuteHeap.mapa) # zistim poziciu na ktorom je medzera (reprezentovane cislom 0)
    skusMinusRiadok(vytiahnuteHeap, mapaKoniec, heuristika2) # zavolam funkciu, ktora vyskusa operaciu DOLE
    skusPlusRiadok(vytiahnuteHeap, mapaKoniec, heuristika2) # zavolam funkciu, ktora vyskusa operaciu HORE
    skusMinusStlpec(vytiahnuteHeap, mapaKoniec, heuristika2) # zavolam funkciu, ktora vyskusa operaciu VPRAVO
    skusPlusStlpec(vytiahnuteHeap, mapaKoniec, heuristika2) # zavolam funkciu, ktora vyskusa operaciu VLAVO
    return vytiahnuteHeap # vratim vytiahnuty uzol z haldy


def vypisPostupu(poslednyVytiahnuty):
    rovnake = True
    pocetKrokov = 0
    if poslednyVytiahnuty is not None: # tato podmienka skusa, ci existuje pre dane uzle riesenie
        if poslednyVytiahnuty.predosli is not None: # ak nie je uzol, z ktoreho vysiel poslednyVytiahnuty None, tak zaciatocny uzol nie je koncovym
            rovnake = False
            postupnost2 = []
            print("Ukoncena postupnost:")
            while poslednyVytiahnuty is not None: # od posledneho vygenerovaneho uzla prechazdam ku zaciatocnemu, podla toho ako bola vygenerovana postupnost
                pocetKrokov = pocetKrokov + 1 # zvysujem pocet krokov, ktore je potrebne vykonat, aby sa dostal zaciatocny uzol na koncovy
                postupnost2.append(poslednyVytiahnuty.operacia) # operacie, ktore som vykonaval si davam do listu, aby som ich potom vypisal
                poslednyVytiahnuty = poslednyVytiahnuty.predosli # tymto prechodom sa dostanem od konecneho uzla na zaciatocny
            for prvok2 in reversed(postupnost2): # vypisem operacie ako boli generovane pri prechodoch v uzloch
                print(prvok2)
            print("")
    else: # ak nema riesenie
        rovnake = False
        print("Nema riesenie.")
    # vypisem udaje na zistenie efektivnosti
    if pocetKrokov is not 0: # -1, pretoze tam mam aj zaciatok
        pocetKrokov = pocetKrokov - 1
    print("Pocet krokov: " + str(pocetKrokov))
    print("Pocet spracovanych uzlov: " + str(pocetSpracovanychUzlov))
    print("Pocet vygenerovanych uzlov: " + str(pocetVytvorenychUzlov))

    if rovnake:
        print("Zaciatocny stav je koncovy.")

mapaKoniec = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]
mapaZaciatok = [[7, 8, 6],
                [5, 4, 3],
                [2, 0, 1]]
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
# mapaZaciatok = [[1, 2, 3, 4],
#                 [5, 6, 7, 8],
#                 [9, 10, 11, 12],
#                 [13, 14, 15, 0]]
# mapaKoniec = [[1, 2, 3, 4],
#               [5, 6, 7, 8],
#               [9, 10, 12, 15],
#               [13, 14, 11, 0]]
# mapaZaciatok = [[2, 3, 4],
#                 [5, 1, 6],
#                 [7, 8, 0]]
# mapaKoniec = [[1, 2, 3],
#               [4, 5, 6],
#               [7, 8, 0]]

heuristika2 = koniec = False
while(koniec is False):
    if heuristika2 is False:
        print("Riesim heuristika 1.")
        pocetRoznych = zistiPocetRoznych(mapaZaciatok, mapaKoniec) # zisti pocet policok, ktore nie su na svojom mieste
        poslednyVytiahnuty = StavMapy(mapaZaciatok, pocetRoznych, "Zaciatok", None) # vytvorim pociatocny uzol pre prvu heuristiku
        hashSet.add(vytvorStringMapa(mapaZaciatok).__hash__())  # pociatocnu mapu pridam do hashSetu
        heapq.heappush(minHeap1, poslednyVytiahnuty)  # vlozenim zaciatocny uzol do heapu, ktory mi riadi cely algoritmus
        while(pocetRoznych is not 0): # pokial nie su vsetky policka na svojej pozicii, tak cyklus pokracuje
            poslednyVytiahnuty = skusaj(mapaKoniec, heuristika2) # funkcia vytiahne uzol z heapu a vyskusa vsetky mozne operacie (max 4)
            if poslednyVytiahnuty is None: # ak bol heap prazdny, tak neexistuje riesenie
                break
            pocetRoznych = poslednyVytiahnuty.pocetRoznych # menim hodnotu, podla vytiahnuteho uzla z heapu
        hashSet.clear() # musim vycistit set, pretoze pojdem generovat uzle pre druhu heuristiku a niektore sa mozu opakovat
        heuristika2 = True
        vypisPostupu(poslednyVytiahnuty) # vypise postupnost operacii, pocet krokov, pocet spracovanych uzlov, pocet vygenerovanych uzlov
        pocetSpracovanychUzlov = pocetVytvorenychUzlov = 0 # musim anulovat hodnoty tychto premennych, pretoze ich znova vyuzijem pri rieseni druhej heuristiky
    else:
        print("\nRiesim heuristika 2")
        pocetRoznych = zistiPocetRoznychVzdialenost(mapaZaciatok, mapaKoniec) # zisti vzdialenost jednotlivych policok ku koncu a nasledne ich scita
        poslednyVytiahnuty = StavMapy(mapaZaciatok, pocetRoznych, "Zaciatok", None) # vytvorim pociatocny uzol pre druhu heuristiku
        hashSet.add(vytvorStringMapa(mapaZaciatok).__hash__())  # pociatocnu mapu pridam do hashSetu, pretoze algoritmus zacina riesit podla druhej heuristiky
        heapq.heappush(minHeap2, poslednyVytiahnuty) # vlozim zaciatocny uzol do heapu, ktory mi riadi cely algoritmus
        while(pocetRoznych is not 0): # pokial nie su vsetky policka na svojej pozicii, tak cyklus pokracuje
            poslednyVytiahnuty = skusaj(mapaKoniec, heuristika2) # funkcia vytiahne uzol z heapu a vyskusa vsetky mozne operacie (max 4)
            if poslednyVytiahnuty is None: # ak bol heap prazdny, tak neexistuje riesenie
                break
            pocetRoznych = poslednyVytiahnuty.pocetRoznych # menim hodnotu, podla vytiahnuteho uzly z heapu
        vypisPostupu(poslednyVytiahnuty) # vypise postupnost operacii, pocet krokov, pocet spracovanych uzlov, pocet vygenerovanych uzlov
        koniec = True # program sa skonci
