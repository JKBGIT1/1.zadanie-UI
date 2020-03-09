class Policko:
    def __init__(self, hodnotaPolicka): #hodnota policka je cislo od 1 po (n*m) - 1, prazdne miesto na hracej ploche symbolizuje 0
        self.pocetPohybov = 0
        self.hodnotaPolicka = hodnotaPolicka


hraciaPlocha = []

riadky = int(input("Zadajte pocet riadkov"))
stlpce = int(input("Zadajte pocet stlpcov"))

for i in range(riadky):
    hraciaPlocha = []
    for j in range(stlpce):
        hraciaPlocha.append(Policko(int(input("Zadaj hodnotu policka"))))