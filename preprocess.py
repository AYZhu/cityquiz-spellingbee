import pandas as pd

# Input file from https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/export/?flg=en-us&disjunctive.cou_name_en&sort=name
df = pd.read_json("geonames-all-cities-with-a-population-1000.json")
del df["alternate_names"]

cutoff = 1000

used_df = df[(df["population"] > cutoff) & (df["country_code"] == "US")]
used_df.to_json("cities.json", orient='records')

cities = [str(x).upper() for x in used_df["ascii_name"].to_list()]
cities = sorted(set(cities))

name_to_set = lambda x: set(x) - set((' ', '-',"'",'"'))
name_to_tup = lambda x: tuple(sorted(name_to_set(x)))

letters = [name_to_tup(x) for x in cities]

pangrams = dict()
for s in letters:
  if len(s) == 7:
    pangrams[s] = pangrams.get(s, 0) + 1

with open("pangrams.txt", "w") as f:
  print(list(list(x) for x in pangrams.keys()), file=f)