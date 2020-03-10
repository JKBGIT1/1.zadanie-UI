import copy


class Obmena:
    def __init__(self, mapa, pocetRoznych):
        self.mapa = mapa
        self.pocetRoznych = pocetRoznych


pocetRoznych = 0
vygenerovaneMapy = []
riadokNula = stlpecNula = 0


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


def zmenaMinusRiadok(obmena, mapaZaciatok, riadokNula, stlpecNula):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula - 1][stlpecNula]
    obmena[riadokNula - 1][stlpecNula] = 0
    return obmena


def zmenaPlusRiadok(obmena, mapaZaciatok, riadokNula, stlpecNula):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula + 1][stlpecNula]
    obmena[riadokNula + 1][stlpecNula] = 0
    return obmena


def zmenaMinusStlpec(obmena, mapaZaciatok, riadokNula, stlpecNula):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula][stlpecNula - 1]
    obmena[riadokNula][stlpecNula - 1] = 0
    return obmena


def zmenaPlusStlpec(obmena, mapaZaciatok, riadokNula, stlpecNula):
    obmena[riadokNula][stlpecNula] = mapaZaciatok[riadokNula][stlpecNula + 1]
    obmena[riadokNula][stlpecNula + 1] = 0
    return obmena


def skusMinusRiadok(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, vygenerovane):
    if (riadokNula - 1 >= 0):
        print("Riadok minus")
        obmena = copy.deepcopy(mapaZaciatok)
        obmena = zmenaMinusRiadok(obmena, mapaZaciatok, riadokNula, stlpecNula)
        if obmena == vygenerovane:
            return None
        pocetRoznychFunkcia = int(zistiPocetRoznych(obmena, mapaKoniec))
        return Obmena(obmena, pocetRoznychFunkcia)
    else:
        return None


def skusPlusRiadok(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, vygenerovane, prvaObmena):
    if (riadokNula + 1 < len(mapaZaciatok)):
        print("Riadok plus")
        obmena = copy.deepcopy(mapaZaciatok)
        obmena = zmenaPlusRiadok(obmena, mapaZaciatok, riadokNula, stlpecNula)
        if obmena == vygenerovane:
            return prvaObmena
        pocetRoznychFunkcia = zistiPocetRoznych(obmena, mapaKoniec)
        if (prvaObmena is None or pocetRoznychFunkcia < prvaObmena.pocetRoznych):
            return Obmena(obmena, pocetRoznychFunkcia)
        else:
            return prvaObmena
    else:
        return prvaObmena


def skusMinusStlpec(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, vygenerovane, druhaObmena):
    if (stlpecNula - 1 >= 0):
        print("Stlpec minus")
        obmena = copy.deepcopy(mapaZaciatok)
        obmena = zmenaMinusStlpec(obmena, mapaZaciatok, riadokNula, stlpecNula)
        if obmena == vygenerovane:
            return druhaObmena
        pocetRoznychFunkcia = zistiPocetRoznych(obmena, mapaKoniec)
        if (druhaObmena is None or pocetRoznychFunkcia < druhaObmena.pocetRoznych):
            return Obmena(obmena, pocetRoznychFunkcia)
        else:
            return druhaObmena
    else:
        return druhaObmena


def skusPlusStlpec(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, vygenerovane, tretiaObmena):
    if (stlpecNula + 1 < len(mapaZaciatok[riadokNula])):
        print("Stlpec plus")
        obmena = copy.deepcopy(mapaZaciatok)
        obmena = zmenaPlusStlpec(obmena, mapaZaciatok, riadokNula, stlpecNula)
        if obmena == vygenerovane:
            return tretiaObmena
        pocetRoznychFunkcia = zistiPocetRoznych(obmena, mapaKoniec)
        if (tretiaObmena is None or pocetRoznychFunkcia < tretiaObmena.pocetRoznych):
            return Obmena(obmena, pocetRoznychFunkcia)
        else:
            return tretiaObmena
    else:
        return tretiaObmena


def skusaj(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, vygenerovane):
    global pocetRoznych, poslednaVygenerovana
    print("PISEM MAPU DO PICE")
    vypisMapu(mapaZaciatok)
    print("VYPISAL SOM MAPU")
    prvaObmena = skusMinusRiadok(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, vygenerovane)
    druhaObmena = skusPlusRiadok(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, vygenerovane, prvaObmena)
    tretiaObmena = skusMinusStlpec(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, vygenerovane, druhaObmena)
    stvrtaObmena = skusPlusStlpec(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, vygenerovane, tretiaObmena)
    pocetRoznych = stvrtaObmena.pocetRoznych
    vygenerovaneMapy.append(mapaZaciatok)
    poslednaVygenerovana = mapaZaciatok
    zistiPoziciuNula(stvrtaObmena.mapa)
    return stvrtaObmena.mapa


mapaKoniec = [[1, 2, 3],
              [4, 6, 5],
              [7, 8, 0]]
mapaZaciatok = [[1, 2, 3],
                [4, 8, 6],
                [7, 5, 0]]

# stringMapy = ""
#
# for i in range(len(mapaZaciatok)):
#     for j in range(len(mapaZaciatok[i])):
#         if (mapaZaciatok[i][j] is 0):
#             riadokNula = i
#             stlpecNula = j
#         print(mapaZaciatok[i][j], end=" ")
#         stringMapy = stringMapy + str(mapaZaciatok[i][j])
#     print("")

poslednaVygenerovana = copy.deepcopy(mapaZaciatok)
zistiPoziciuNula(mapaZaciatok)

pocetRoznych = zistiPocetRoznych(mapaZaciatok, mapaKoniec)
while(pocetRoznych is not 0):
    mapaZaciatok = skusaj(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula, poslednaVygenerovana)

print("")
vypisMapu(mapaZaciatok)


