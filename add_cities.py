#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

cities = {}
cities["mecklenburg-vorpommern"] = ["Rostock", "Schwerin", "Neubrandenburg", "Stralsund", "Greifswald", "Wismar",
                                    "Güstrow", "Waren (Müritz)", "Neustrelitz"]
cities["hamburg"] = ["Hamburg"]
cities["schleswig-holstein"] = ["Kiel", "Lübeck", "Flensburg", "Neumünster", "Norderstedt", "Elmshorn", "Pinneberg",
                                "Wedel", "Ahrensburg", "Itzehoe", "Geesthacht", "Rendsburg", "Henstedt-Ulzburg(*)",
                                "Reinbek", "Bad Oldesloe", "Schleswig", "Husum  25.055", "Eckernförde", "Heide  22.950",
                                "Kaltenkirchen", "Quickborn", "Bad Schwartau"]
cities["niedersachsen"] = ["Hannover", "Braunschweig", "Oldenburg", "Osnabrück", "Wolfsburg", "Göttingen", "Salzgitter",
                           "Hildesheim", "Delmenhorst", "Wilhelmshaven", "Lüneburg", "Celle", "Garbsen", "Hameln",
                           "Lingen (Ems)", "Langenhagen", "Nordhorn", "Wolfenbüttel", "Goslar", "Emden", "Peine",
                           "Cuxhaven", "Stade", "Melle", "Neustadt am Rübenberge", "Lehrte", "Gifhorn", "Aurich",
                           "Wunstorf", "Laatzen", "Seevetal(*)", "Buxtehude", "Buchholz in der Nordheide", "Papenburg",
                           "Meppen", "Winsen (Luhe)", "Cloppenburg", "Leer", "Barsinghausen", "Seelze", "Uelzen",
                           "Stuhr(*)", "Vechta", "Georgsmarienhütte", "Achim", "Nienburg/Weser", "Ganderkesee(*)",
                           "Bramsche", "Einbeck", "Geestland19", "Weyhe(*)", "Osterholz-Scharmbeck", "Burgdorf",
                           "Wedemark(*)", "Northeim", "Springe", "Bad Zwischenahn(*)", "Verden (Aller)",
                           "Lohne (Oldenburg)", "Nordenham", "Rinteln", "Norden", "Syke", "Ronnenberg", "Isernhagen(*)",
                           "Varel", "Hann. Münden", "Haren (Ems)", "Sehnde", "Helmstedt", "Moormerland(*)", "Walsrode",
                           "Wallenhorst(*)", "Westerstede", "Rastede(*)", "Stadthagen", "Friesoythe", "Edewecht(*)",
                           "Osterode am Harz", "Bad Harzburg", "Rotenburg (Wümme)", "Ilsede(*)", "Soltau",
                           "Neu Wulmstorf(*)", "Westoverledingen(*)", "Duderstadt", "Burgwedel32", "Wittmund",
                           "Schortens", "Holzminden", "Uetze(*)", "Schwanewede(*)"]
with open("cities.json", "w") as file:
    json.dump(cities, file, indent=2, ensure_ascii=False)
