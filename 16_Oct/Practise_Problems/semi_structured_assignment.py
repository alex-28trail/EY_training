import pandas as pd
import json
import numpy as np
with open("semi_structured_data.json")as file:
    pra= json.load(file)

print(pra)

# 1
df=pd.read_json("semi_structured_data.json")
print(df)
# 2
print(df[["incident_id"]])

# 3
print(df[["incident_id","location"]])

#4 incidents where severity is High .
print(df[df.severity=="High"])
# 5. Display incidents where category is Safety .
print(df[df.category=="Safety"])
# 6. Some incidents do not contain actions . Print:
# No actions recorded
for i in pra:
    print(f"{i['incident_id']}")

    actions = i.get("actions")

    if actions:
        for j in actions:
            print(j)
    else:
        print("No actions recorded")
# when the field is missing.
# 7. Count how many incidents belong to each severity level.

# 8
for i in pra:
    i["status"]="Open"

# 9

