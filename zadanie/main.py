import copy

def vypisMapu(mapa):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            print(mapa[i][j], end=" ")
        print("")


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


def skusaj(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula):
    if (riadokNula - 1 >= 0):
        print("Riadok minus")
        obmena = copy.deepcopy(mapaZaciatok)
        zmenaMinusRiadok(obmena, mapaZaciatok, riadokNula, stlpecNula)
        vypisMapu(obmena)
    if (riadokNula + 1 < len(mapaZaciatok)):
        print("Riadok plus")
        obmena = copy.deepcopy(mapaZaciatok)
        zmenaPlusRiadok(obmena, mapaZaciatok, riadokNula, stlpecNula)
        vypisMapu(obmena)
    if (stlpecNula - 1 >= 0):
        print("Stlpec minus")
        obmena = copy.deepcopy(mapaZaciatok)
        zmenaMinusStlpec(obmena, mapaZaciatok, riadokNula, stlpecNula)
        vypisMapu(obmena)
    if (stlpecNula + 1 < len(mapaZaciatok[riadokNula])):
        print("Stlpec plus")
        obmena = copy.deepcopy(mapaZaciatok)
        zmenaPlusStlpec(obmena, mapaZaciatok, riadokNula, stlpecNula)
        vypisMapu(obmena)


vygenerovaneMapy = []
mapaKoniec = [[1, 2, 3],
              [4, 6, 5],
              [7, 8, 0]]
mapaZaciatok = [[1, 2, 3],
                [4, 8, 6],
                [7, 5, 0]]

stringMapy = ""
riadokNula = stlpecNula = 0
for i in range(len(mapaZaciatok)):
    for j in range(len(mapaZaciatok[i])):
        if (mapaZaciatok[i][j] is 0):
            riadokNula = i
            stlpecNula = j
        print(mapaZaciatok[i][j], end=" ")
        stringMapy = stringMapy + str(mapaZaciatok[i][j])
    print("")



pocetRoznych = 0
for i in range(len(mapaZaciatok)):
    for j in range(len(mapaZaciatok[i])):
        if (mapaKoniec[i][j] is not mapaZaciatok[i][j]):
            pocetRoznych = pocetRoznych + 1

# print(str(riadokNula) + " " + str(stlpecNula))

skusaj(mapaZaciatok, mapaKoniec, riadokNula, stlpecNula)
print("")
vypisMapu(mapaZaciatok)


