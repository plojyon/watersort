# Watersort

Find solutions for this [App on Google Play](https://play.google.com/store/apps/details?id=com.gma.water.sort.puzzle).

Usage:
```py
level77 = "BRBL,PORI,IGPL,LLYG,IYYT,TPRR,OOBY,GGBO,PTIT,EEEE,EEEE"
conf = Configuration(level77)
G, final = solution_graph(conf)
print(final.moves) 
# Prints: [(1, 9), (1, 10), (6, 10), (0, 6), (0, 1), (6, 0), (8, 9), (5, 8), (5, 9), (1, 5), (2, 1), (4, 1), (4, 6), (8, 4), (8, 1), (4, 8), (0, 4), (3, 0), (3, 6), (2, 3), (2, 9), (7, 3), (7, 4), (7, 10), (0, 2)]
```
