import copy

hashSet = set() # tento set funguje ako hash tabulka, len bez hodnotou pre kluce, z dovodu, ze sem  nebudem davat duplikaty

mapaKoniec = [[1, 2, 3],
              [4, 6, 5],
              [7, 8, 0]]
mapaZaciatok = [[1, 2, 3],
                [4, 8, 6],
                [7, 5, 0]]


# string = "Pipik"
# key = string.__hash__()
#
# hashSet.add(key)
# hashSet.add("Pipik2".__hash__())
# if "Pipik3".__hash__() in hashSet:
#     print("PICO")
# else:
#     hashSet.add("Pipik3".__hash__())
