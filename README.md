# UI-2.zadanie
Prve zadanie UI - greedy algorithms

Programovací jazyk Python.

Využité knižnice copy a heapq.

Zadanie funguje na princípe greedy algoritmoch. Ak má daný problém riešenie, tak ho dokáže vytvoriť dvomi heuristikami. 

Prvá heuristika sa pozerá na počet políčok na mape, ktoré nie sú na svojom mieste. 

Druhá najprv zistí ako ďaleko sa nachádzajú jednotlivé políčka od svojej koncovej pozície, následne tieto vzdialenosti sčíta a podľa výsledku súčtu sa riadi algoritmus.

Celý algoritmus je riadeny pomocou heapov, z ktorých vždy popuje uzol s najmenej rozdielmi oproti koncovému uzlu. Vygenerované a použité uzle si dávam do setu(python fičúra), aby som predišiel duplikáciam pri chode algoritmu. Vždy keď vygenerujem nový prvok, tak pozriem, či sa už náhodou nenachádza v sete ak áno, tak ho nevhodím do heapu. 

Nové uzle sa generujú pomocou operácií DOLE, HORE, VPRAVO, VLAVO, pričom vždy musím vyskúšať, či daná operácia nezachádza mimo mapu.

Program sa dokáže prispôsobiť rôznym veľkostiam mapy, len musí byť dostatok pamäte.
