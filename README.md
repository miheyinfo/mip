# Zuschnittsprotokoll Dokumentation
Für die Darstellung des Zuschnittsprotokolls wird ein JSON-Format genutzt. Das "protocol" Objekt beinhaltet ein "data" Objekt, in diesem befinden sich zwei Arrays mit dem Namen "right" und "left" für die beiden Seiten des Zuschnittsprotokolls. Innerhalb dieser Arrays sind die einzelnen Schnitte als "cut" Objekte zu finden. Jedes "cut" Objekt besteht aus einem weiteren Array, das "name" Objekte enthält, die die einzelnen, im Protokoll durch Buchstaben dargestellten, Schnitte dar.

__Beispiel__:
```
{

    "protocol" : {

        "data" : {

            "right" :

            [

                {"cut":[{"name": "C", "data": ""}]},

                {"cut":[

                    {"name": "E", "data": ""},

                    {"name": "F", "data": ""}

                ]},
...
```
```
