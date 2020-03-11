import copy
import heapq

class StavMapy:
    def __init__(self, mapa, pocetRoznych, predosli):
        self.mapa = copy.deepcopy(mapa)
        self.pocetRoznych = pocetRoznych
        self.predosli = predosli
    def __lt__(self, other):
        return self.pocetRoznych < other.pocetRoznych


# class Prosim:
#     def __init__(self, hodnota):
#         self.hodnota = hodnota
#     def __lt__(self, other):
#         return self.hodnota < other.hodnota

minHeap = [] # halda, do ktorej vhadzujem vsetky stavy mapy, ktore som vygeneroval a neboli pouzite, usporiadanie podla hodnoty pocetRoznych v classe StavMapy
hashSet = set() # tento set funguje ako hash tabulka, len bez hodnotou pre kluce, z dovodu, ze sem  nebudem davat duplikaty
riadokNula = stlpecNula = 0 # globalne premenne, ktore mi drzia suradnice, kde sa nachadza 0, teda prazdne policko


def vypisMapu(mapa):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            print(mapa[i][j], end=" ")
        print("")


def zistiPocetRoznych(obmena, mapaKoniec):
    pocetRoznychFunkcia = 0
    for i in range(len(mapaKoniec)):
        for j in range(len(mapaKoniec[i])):
            if (mapaKoniec[i][j] is not obmena[i][j]):
                pocetRoznychFunkcia = pocetRoznychFunkcia + 1

    return pocetRoznychFunkcia


def zistiPoziciuNula(mapaZaciatok):
    global riadokNula, stlpecNula
    for i in range(len(mapaZaciatok)):
        for j in range(len(mapaZaciatok[i])):
            if (mapaZaciatok[i][j] is 0):
                riadokNula = i
                stlpecNula = j


def vytvorStringMapa(mapa):
    string = ""
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            string = string + str(mapa[i][j])

    return string


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


def skusMinusRiadok(vytiahnuteHeap, mapaKoniec):
    if (riadokNula - 1 >= 0):
        print("Riadok minus")
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa)
        obmenaMapy = zmenaMinusRiadok(obmenaMapy, vytiahnuteHeap.mapa)
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__()
        if hashObmeny not in hashSet:
            pocetRoznychFunkcia = int(zistiPocetRoznych(obmenaMapy, mapaKoniec))
            heapq.heappush(minHeap, StavMapy(obmenaMapy, pocetRoznychFunkcia, vytiahnuteHeap))


def skusPlusRiadok(vytiahnuteHeap, mapaKoniec):
    if (riadokNula + 1 < len(vytiahnuteHeap.mapa)):
        print("Riadok plus")
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa)
        obmenaMapy = zmenaPlusRiadok(obmenaMapy, vytiahnuteHeap.mapa)
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__()
        if hashObmeny not in hashSet:
            pocetRoznychFunkcia = int(zistiPocetRoznych(obmenaMapy, mapaKoniec))
            heapq.heappush(minHeap, StavMapy(obmenaMapy, pocetRoznychFunkcia, vytiahnuteHeap))


def skusMinusStlpec(vytiahnuteHeap, mapaKoniec):
    if (stlpecNula - 1 >= 0):
        print("Stlpec minus")
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa)
        obmenaMapy = zmenaMinusStlpec(obmenaMapy, vytiahnuteHeap.mapa)
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__()
        if hashObmeny not in hashSet:
            pocetRoznychFunkcia = int(zistiPocetRoznych(obmenaMapy, mapaKoniec))
            heapq.heappush(minHeap, StavMapy(obmenaMapy, pocetRoznychFunkcia, vytiahnuteHeap))


def skusPlusStlpec(vytiahnuteHeap, mapaKoniec):
    if (stlpecNula + 1 < len(vytiahnuteHeap.mapa[riadokNula])):
        print("Stlpec plus")
        obmenaMapy = copy.deepcopy(vytiahnuteHeap.mapa)
        obmenaMapy = zmenaPlusStlpec(obmenaMapy, vytiahnuteHeap.mapa)
        hashObmeny = vytvorStringMapa(obmenaMapy).__hash__()
        if hashObmeny not in hashSet:
            pocetRoznychFunkcia = zistiPocetRoznych(obmenaMapy, mapaKoniec)
            heapq.heappush(minHeap, StavMapy(obmenaMapy, pocetRoznychFunkcia, vytiahnuteHeap))


def skusaj(mapaKoniec):
    try:
        vytiahnuteHeap = heapq.heappop(minHeap)
    except IndexError:
        return None
    vytiahnuteRozne = zistiPocetRoznych(vytiahnuteHeap.mapa, mapaKoniec)
    # print("PISEM MAPU") # toto potom za podmienku
    # vypisMapu(vytiahnuteHeap.mapa)
    # print("VYPISAL SOM MAPU")
    if vytiahnuteRozne is 0:
        return vytiahnuteHeap
    hashSet.add(vytvorStringMapa(vytiahnuteHeap.mapa).__hash__())
    zistiPoziciuNula(vytiahnuteHeap.mapa)
    skusMinusRiadok(vytiahnuteHeap, mapaKoniec)
    skusPlusRiadok(vytiahnuteHeap, mapaKoniec)
    skusMinusStlpec(vytiahnuteHeap, mapaKoniec)
    skusPlusStlpec(vytiahnuteHeap, mapaKoniec)
    return vytiahnuteHeap

# [[2, 1, 3],
#               [4, 6, 5],
#               [7, 8, 0]]
# mapaZaciatok = [[1, 2, 3],
#                 [4, 8, 6],
#                 [7, 5, 0]]

mapaKoniec = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]
mapaZaciatok = [[7, 8, 6],
                [5, 4, 3],
                [2, 0, 1]]

pocetRoznych = zistiPocetRoznych(mapaZaciatok, mapaKoniec)
poslednyVytiahnuty = StavMapy(mapaZaciatok, pocetRoznych, None)
heapq.heappush(minHeap, poslednyVytiahnuty)

while(pocetRoznych is not 0):
    poslednyVytiahnuty = skusaj(mapaKoniec)
    if poslednyVytiahnuty is None:
        break
    pocetRoznych = poslednyVytiahnuty.pocetRoznych

if poslednyVytiahnuty is not None:
    print("Ukoncena postupnost:")
    while poslednyVytiahnuty is not None:
        vypisMapu(poslednyVytiahnuty.mapa)
        poslednyVytiahnuty = poslednyVytiahnuty.predosli
        print("")
else:
    print("Nema riesenie.")


# heapq.heappush(list, Prosim(1))
# for i in list:
#     print(i.hodnota)
# print("")
# print(heapq.heappop(list).hodnota)
# string = "Pipik"
# key = string.__hash__()
#
# hashSet.add(key)
# hashSet.add("Pipik2".__hash__())
# if "Pipik3".__hash__() in hashSet:
#     print("PICO")
# else:
#     hashSet.add("Pipik3".__hash__())
